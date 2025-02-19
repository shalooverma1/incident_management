from django.urls import path
from .views import IncidentListCreateView, IncidentRetrieveUpdateView, ImportIncidentsView, IncidentListView, DeleteIncidentView, DeleteAllIncidentView

urlpatterns = [
    path('incidents/create/', IncidentListCreateView.as_view(), name='incident-list-create'),
    path('incidents/', IncidentListView.as_view(), name='incident-list'), 
    path('incidents/<int:pk>/', IncidentRetrieveUpdateView.as_view(), name='incident-details'),
    path('incidents/<int:incident_id>/delete/', DeleteIncidentView.as_view(), name='delete-incident'),
    path('incidents/delete/', DeleteAllIncidentView.as_view(), name='delete-all-incident'),
    path('import-incidents/', ImportIncidentsView.as_view(), name='incident-details'),
]