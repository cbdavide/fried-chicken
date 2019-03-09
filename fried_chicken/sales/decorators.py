import requests
from base64 import b64encode

from django.conf import settings


def tpaga_request(func):
    """
    Injects the authentication credentials, and some other headers,
    also, prepends the TPAGA_API_BASE_URL to the given endpoint.
    """
    def wrapper(*args, **kwargs):

        headers = kwargs.get('headers', {})

        user = settings.TPAGA_API_USER
        password = settings.TPAGA_API_PASSWORD

        bytes_credentials = f'{user}:{password}'.encode('utf-8')
        credentials = b64encode(bytes_credentials)
        credentials = credentials.decode("utf-8")

        headers.update({
            'Authorization': f'Basic {credentials}',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json'
        })

        kwargs.update(headers=headers)

        # Prepend the TPAGA_API_BASE_URL
        api_endpoint = f'{settings.TPAGA_API_BASE_URL}/{args[0]}'
        args = args[1:]

        try:
            return func(api_endpoint, *args, **kwargs)
        except requests.Timeout:
            raise Exception("Couldn't make the request")

    return wrapper
