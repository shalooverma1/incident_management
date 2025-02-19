import logging
import requests
from .serializers import ExternalIncidentSerializer

logger = logging.getLogger(__name__)

def fetch_and_store_incidents(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return {"error": "Failed to fetch data", "status_code": response.status_code}

        incidents_data = response.json()
        created_count = 0
        skipped_count = 0

        for incidents in incidents_data:
            serializer = ExternalIncidentSerializer(data=incidents)
            if serializer.is_valid():
                new_incident, is_new = serializer.save()
                if is_new:
                    created_count += 1
                else:
                    skipped_count += 1
            else:
                logger.error(f"Incident validation failed: {serializer.errors}")

        return {
            "message": f"{created_count} incidents imported successfully.",
            "skipped": f"{skipped_count} incidents already existed and were skipped."
            }
    
    except requests.exceptions.HTTPError as http_err:
        # Specific handling for HTTP errors
        logger.error(f"HTTP error occurred: {http_err}")
        return {"error": "HTTP error occurred", "details": str(http_err)}
    
    except requests.exceptions.RequestException as req_err:
        # Catch other request-related errors
        logger.error(f"Request error occurred: {req_err}")
        return {"error": "Request error occurred", "details": str(req_err)}
    
    except Exception as e:
        # Catch any other unexpected errors
        logger.error(f"An unexpected error occurred: {e}")
        return {"error": "An unexpected error occurred", "details": str(e)}
