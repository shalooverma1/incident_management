from django.contrib import admin
from .models import Incident

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'severity', 'status', 'reported_by','created_at')
    list_filter = ('status', 'severity')
    search_fields = ('id','title')

# Register your models here.
