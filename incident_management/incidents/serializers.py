from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Incident
import logging

logger = logging.getLogger(__name__)

class IncidentSerializer(serializers.ModelSerializer):
    reported_by = serializers.SlugRelatedField(
        queryset = User.objects.all(),
        slug_field = "username"
    )

    class Meta:
        model = Incident
        fields = "__all__"

class ExternalIncidentSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    severity = serializers.ChoiceField(choices=Incident.SEVERITY_CHOICE)
    status = serializers.ChoiceField(choices=Incident.STATUS_CHOICE)
    reported_by = serializers.CharField()
    created_at = serializers.DateTimeField()

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(username=validated_data["reported_by"])

        incident = Incident.objects.filter(external_id=validated_data["id"])
        if incident.exists(): 
            existing_incident = incident.first()
            logger.info(f"Incident with external_id {validated_data['id']} already exists. Skip creation.")
            return existing_incident, False
        
        incident = Incident.objects.create(
            external_id=validated_data["id"],
            title=validated_data["title"],
            description=validated_data["description"],
            severity=validated_data["severity"],
            status=validated_data["status"],
            reported_by=user,
            created_at=validated_data["created_at"]
        )
        return incident, True
