from django.urls import path
from .views import RegisterView, MarkSpamView, SearchView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('mark-spam/', MarkSpamView.as_view(), name='mark-spam'),
    path('search/', SearchView.as_view(), name='search'),
]