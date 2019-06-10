from django.urls import path

from .views import (
    TicketListView,
    TicketDetailView,
)

app_name = 'tickets'

urlpatterns = [
    path('', TicketListView.as_view(), name='ticket-list'),
    path('<int:id>/', TicketDetailView.as_view(), name='ticket-detail'),
]
