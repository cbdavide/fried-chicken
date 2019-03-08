import json
import requests
from base64 import b64encode

from django.conf import settings


def authenticated(func):

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
        print(kwargs)

        return func(*args, **kwargs)

    return wrapper


@authenticated
def post_request(api_endpoint, payload, *args, **kwargs):

    url = f'{settings.TPAGA_API_BASE_URL}/{api_endpoint}'

    try:
        return requests.post(
            url,
            data=json.dumps(payload),
            headers=kwargs['headers']
        )
    except requests.Timeout:
        raise Exception("Couldn't create the request")


def create_payment_request(sale, payment):

    payload = dict(
        terminal_id=1,
        cost=sale.total,
        order_id=str(sale.order),
        user_ip_address=payment.user_ip_address,
        expires_at=payment.expires_at.isoformat(),
        purchase_details_url='https://google.com',
        idempotency_token=str(payment.idempotency_token),
        purchase_description="Payment of fried chicken.",
    )

    # purchase_details_url=sale.get_absolute_url(),
    response = post_request(
        settings.PAYMENT_REQUEST_ENDPOINT,
        payload
    )

    if response.status_code == 201:
        return response.json()

    raise Exception("The request wasn't created.")
