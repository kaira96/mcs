from time import time

from django.utils.deprecation import MiddlewareMixin
from loguru import logger


class StatsMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        "Start time at request coming in"
        request.start_time = time()
        
    def process_response(self, request, response):
        # Calculate work duration
        duration = time() - request.start_time
        
        info = {
            'duration': str(int(duration * 1000)),
            'urls_path': str(request.get_full_path()),
            'method': str(request.method.upper()),
            'user': str(request.user.login) if hasattr(request.user, 'login') else 'Guest'
        }
        
        logger.info("user action", extra=info)
        # response['X-page-generation-duration'] = int(duration * 1000)
        return response
    