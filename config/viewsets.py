import uuid
from datetime import datetime,timezone
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

class StandardViewset(viewsets.ModelViewSet):
    """
    A standard viewset that provides custom API Response wrapper for status code levels.
    Author: James Kekeli
    """
    use_standard_response = True

    def _is_already_wrapped(self, data):
        """
        Check if the response data is already wrapped in the standard format.
        """

        if isinstance(data,dict):
            return "status" in data and "data" in data and "meta" in data
        return False
    

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Override the `finalize_response` method to wrap the response data in a standard format.
        """
        response = super().finalize_response(request, response, *args, **kwargs)

        if not getattr(self,'use_standard_response', False):
            return response
        
        if self._is_already_wrapped(response.data):
            return response
        
        if isinstance(response.data, (dict,list)):
            if 200 <= response.status_code < 300:
                pagination_data = {}
                payload_data = response.data

                if isinstance(response.data,dict) and "results" in response.data:
                    try:
                        current_page = int(request.query_params.get('page',1))
                    except ValueError:
                        current_page = 1

                    pagination_data = {
                        "current_page": current_page,
                        "total_count": response.data.get("count",0),
                        "next_page_url": response.data.get("next"),
                        "previous_page_url": response.data.get("previous"),
                    }

                    payload_data = response.data.get("results")

                response.data = {
                    "status":"success",
                    "data":payload_data,
                    "pagination": pagination_data,
                    "meta":{
                        "request_id": str(uuid.uuid4()),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "version": "1.0.0"
                    }
                }
            elif 400 <= response.status_code <= 500:
                error_data = response.data

                if response.status_code == 400:
                    response.data = {
                        "status": "error",
                        "error": "VALIDATION ERROR",
                        "errors": [{
                            "message": "Request Validation Failed",
                            "details": error_data
                        }]
                    }
                elif response.status_code == 401:
                    response.data = {
                        "status": "error",
                        "error": "UNAUTHENTICATED",
                        "errors": [{
                            "message": "Missing or Invalid Token",
                            "details": error_data
                        }]
                    }
                elif response.status_code == 403:
                    response.data = {
                        "status": "error",
                        "error": "FORBIDDEN",
                        "errors": [{
                            "message": "Provide Firebase Token in Authorization Header",
                            "details": error_data
                        }]
                    }
                elif response.status_code == 404:
                    response.data = {
                        "status": "error",
                        "error": "NOT FOUND",
                        "errors": [{
                            "message": "Resource Not Found",
                            "details": error_data
                        }]
                    }
                elif response.status_code == 500:
                    response.data = {
                        "status": "error",
                        "error": "SERVER ERROR",
                        "errors": [{
                            "message": "Internal Server Error",
                            "details": error_data
                        }]
                    }
                else:
                    response.data = {
                        "status": "error",
                        "error": {
                            "code":"NOT_FOUND",
                            "message":"Resource or Service not found"
                        },
                    }

        return response