from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from social_core import exceptions as social_exceptions

from social_core.exceptions import AuthAlreadyAssociated
from social_django.middleware import SocialAuthExceptionMiddleware


class GoogleAuthAlreadyAssociatedMiddleware(SocialAuthExceptionMiddleware):
    """Redirect users to desired-url when AuthAlreadyAssociated exception occurs."""

    def process_exception(self, request, exception):
        if hasattr(social_exceptions, exception.__class__.__name__):
            # Here you can handle the exception as you wish
            if exception.__class__.__name__ == 'AuthAlreadyAssociated':
                return HttpResponse('This social account already exists.')
            return HttpResponse("Exception %s while processing your social account." % exception)
        else:
            return super(GoogleAuthAlreadyAssociatedMiddleware, self).process_exception(request, exception)
