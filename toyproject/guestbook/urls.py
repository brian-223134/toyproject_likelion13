from django.urls import path
from guestbook.views import *

urlpatterns = [
    path('', guestbook_view, name='guestbook-list-create'),   # GET + POST
    path('<int:pk>/', guestbook_delete, name='guestbook-delete'),  # DELETE
]