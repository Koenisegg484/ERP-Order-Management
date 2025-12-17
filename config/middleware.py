import logging
from django.http import JsonResponse


logger = logging.getLogger(__name__)

class ExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            logger.exception(f"Unhandled error : {str(e)}")
            return JsonResponse(
                {"detail" : "Internal server error"},status = 500
            )
        return response