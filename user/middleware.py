from django.http import HttpResponseForbidden
from rest_framework_simplejwt.authentication import JWTAuthentication

class TokenValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        authentication = JWTAuthentication()
        try:
            user, token = authentication.authenticate(request)
            # Vérification supplémentaire du payload du token
            # Accès au payload : token.payload
        except Exception as e:
            return HttpResponseForbidden("Token invalide")

        response = self.get_response(request)
        return response