from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.db.models import Q, Count
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from .models import User, Contact, SpamMark
from .serializers import UserSerializer, ContactSerializer, SpamMarkSerializer
from phoneopedia.settings import SPAM_THRESHOLD

def api_response(status, message, data=None):
    return Response({
        "status": status,
        "message": message,
        "data": data
    })
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return api_response(HTTP_201_CREATED, "User registered successfully.", response.data)
        except ValidationError as e:
            return api_response(HTTP_400_BAD_REQUEST, "Validation error occurred.", {"errors": e.message_dict})
        except Exception as e:
            return api_response(HTTP_400_BAD_REQUEST, "An unexpected error occurred.", {"error": str(e)})


class MarkSpamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            phone_number = request.data.get('phone_number')
            if not phone_number:
                return api_response(HTTP_400_BAD_REQUEST, "Phone number is required.", None)

            contact = Contact.objects.filter(phone_number=phone_number).first()
            if not contact:
                return api_response(HTTP_404_NOT_FOUND, "Phone number does not exist in the database.", None)

            spam_mark, created = SpamMark.objects.get_or_create(contact=contact, marked_by=request.user)
            if not created:
                return api_response(HTTP_400_BAD_REQUEST, "Phone number already marked as spam by the user.", None)

            return api_response(HTTP_201_CREATED, f"Phone number {phone_number} marked as spam.", {
                "id": spam_mark.id,
                "contact": contact.phone_number
            })
        except Exception as e:
            return api_response(HTTP_400_BAD_REQUEST, "An unexpected error occurred.", {"error": str(e)})


class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Extract filter parameters
            name_filter = request.query_params.get('name', None)
            phone_filter = request.query_params.get('phone', None)
            email_filter = request.query_params.get('email', None)
            spam_filter = request.query_params.get('spam', None)

            if not any([name_filter, phone_filter, email_filter, spam_filter]):
                return api_response(HTTP_400_BAD_REQUEST, "At least one filter (name, phone, email, spam) is required.", None)

            results = Contact.objects.all()

            if name_filter:
                results = results.filter(Q(name__icontains=name_filter))

            if phone_filter:
                results = results.filter(phone_number=phone_filter)

            if email_filter:
                results = results.filter(email__icontains=email_filter)

            if spam_filter is not None:
                try:
                    spam_filter = int(spam_filter)
                    results = results.annotate(spam_count=Count('spammark')).filter(spam_count__gte=spam_filter)
                except ValueError:
                    return api_response(HTTP_400_BAD_REQUEST, "Invalid spam filter value. It must be an integer.", None)

            results = results.annotate(spam_count=Count('spammark'))

            data = [
                {
                    "name": result.name,
                    "phone_number": result.phone_number,
                    "email": result.email,
                    "spam_likelihood": result.spam_count >= SPAM_THRESHOLD,
                }
                for result in results
            ]

            return api_response(HTTP_200_OK, "Search results fetched successfully.", data)
        except ObjectDoesNotExist:
            return api_response(HTTP_404_NOT_FOUND, "Requested resource not found.", None)
        except Exception as e:
            return api_response(HTTP_400_BAD_REQUEST, "An unexpected error occurred.", {"error": str(e)})
