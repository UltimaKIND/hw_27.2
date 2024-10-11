import stripe
from forex_python.converter import CurrencyRates

from config import settings

stripe.api_key = settings.STRIPE_API_KEY


def convert_rub_to_usd(amount):
    """
    конвертирует рубли в доллары
    """
    c = CurrencyRates()
    rate = c.get_rate(base_cur="RUB", dest_cur="USD")
    return float(amount * rate)


def create_stripe_price(amount):
    """
    создает цену в страйпе
    """
    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product_data={"name": "Payment"},
    )


def create_stripe_session(price):
    """
    создает сессию на оплату в страйпе
    """
    session = stripe.checkout.Session.create(
        success_url="https://localhost:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
