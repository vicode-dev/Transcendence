from django.utils import translation
from django.conf import settings
import logging

logger = logging.getLogger('app')
class LanguageCookieMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        self.process_response(request, response)
        return response

    def process_request(self, request):
        """
        Sets language from the cookie value.
        """
        if settings.LANGUAGE_COOKIE_NAME in request.COOKIES:
            language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
            if language in dict(settings.LANGUAGES).keys():
                translation.activate(language)
                request.LANGUAGE_CODE = language

    def process_response(self, request, response):
        """
        Create cookie if not there already.

        Also deactivates language.
        """
        if settings.LANGUAGE_COOKIE_NAME not in request.COOKIES:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME,'en')
        translation.deactivate()
        return response
