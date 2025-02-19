from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from .models import Incident
from .serializers import IncidentSerializer
from .utils import fetch_and_store_incidents
import logging

logger = logging.getLogger(__name__)

class IncidentListCreateView(generics.ListCreateAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

class IncidentRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

class IncidentListView(generics.ListAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

class ImportIncidentsView(APIView):
    def post(self, request):
        api_url = request.data.get("api_url")
        if not api_url:
            return Response({"error": "API URL is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = fetch_and_store_incidents(api_url)
            return Response(result)
        except Exception as e:
            logger.error(f"Error fetching incidents: {e}")
            return Response({"error": "Error fetching incidents."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class DeleteIncidentView(APIView):
    def delete(self, request, incident_id):
        try:
            incident = Incident.objects.get(id = incident_id)
            incident.delete()
            return Response({"message": "Incident deleted successfully."}, status=status.HTTP_200_OK)
        except Incident.DoesNotExist:
            return Response({"error": "Incident not found"}, status=status.HTTP_404_NOT_FOUND)
        
class DeleteAllIncidentView(APIView):
    def delete(self, request):
        count , _ = Incident.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='incidents_incident';")

        return Response({"message": f"{count} incidents deleted successfully."}, status=status.HTTP_200_OK)
    
