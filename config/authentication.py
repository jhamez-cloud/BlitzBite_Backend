# core/authentication.py
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user.models import User


class FirebaseAuthentication(BaseAuthentication):
    """Real authentication — verifies a Firebase ID token."""

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        id_token = auth_header.split('Bearer ')[1]

        from firebase_admin import auth as firebase_auth
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
        except Exception:
            raise AuthenticationFailed('Invalid or expired Firebase token.')

        firebase_uid = decoded_token['uid']
        user, _ = User.objects.get_or_create(
            firebase_uid=firebase_uid,
            defaults={'email': decoded_token.get('email', ''), 'name': decoded_token.get('name', '')}
        )
        return (user, None)


class DevAuthentication(BaseAuthentication):
    """TESTING ONLY — simulates a logged-in user without a real Firebase token.
    Enabled only when settings.USE_DEV_AUTH is True. Never enable this in
    any environment reachable by real users."""

    def authenticate(self, request):
        if not getattr(settings, 'USE_DEV_AUTH', False):
            return None

        dev_uid = request.headers.get('X-Dev-User-Id')
        if not dev_uid:
            return None

        user, _ = User.objects.get_or_create(
            firebase_uid=dev_uid,
            defaults={'email': f'{dev_uid}@test.local', 'name': f'Test User {dev_uid}'}
        )
        return (user, None)