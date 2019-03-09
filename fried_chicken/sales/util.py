import json
import requests
from base64 import b64encode

from django.conf import settings
from django.urls import reverse

from .decorators import tpaga_request


@tpaga_request
def post_request(api_endpoint, payload, *args, **kwargs):
    return requests.post(
        api_endpoint,
        data=json.dumps(payload),
        headers=kwargs['headers']
    )


@tpaga_request
def get_request(api_endpoint, *args, **kwargs):
    return requests.get(
        api_endpoint,
        headers=kwargs['headers']
    )


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

    # purchase_details_url=reverse(
    #     'sales:tpaga_payment_details',
    #     args[str(sale.order)]
    # )

    response = post_request(
        f"{settings.PAYMENT_REQUEST_ENDPOINT}/create",
        payload
    )

    if response.status_code == 201:
        return response.json()

    raise Exception("The request wasn't created.")


def confirm_payment_request(payment):

    response = get_request(
        f"{settings.PAYMENT_REQUEST_ENDPOINT}/{payment.tpaga_token}/info"
    )

    if response.status_code == 200:
        return response.json()

    raise Exception("Someting went wrong")


def confirm_delivery(payment):

    payload = dict(
        payment_request_token=payment.tpaga_token
    )

    response = post_request(
        f"{settings.PAYMENT_REQUEST_ENDPOINT}/confirm_delivery",
        payload
    )

    if response.status_code == 200:
        return response.json()

    raise Exception("Someting went wrong")
