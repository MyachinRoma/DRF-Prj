import stripe
from django.conf import settings

# Инициализация Stripe с секретным ключом
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(product_name):
    """Создает продукт в stripe"""

    return stripe.Product.create(
        name=product_name,
    )


def create_stripe_price(payment_amount, prod):
    """Создает цену в stripe"""

    return stripe.Price.create(
        currency="rub",
        unit_amount=int(payment_amount * 100),
        product_data=prod,
    )


def create_stripe_checkout_sessions(price):
    """Создает сессию на оплату в stripe"""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
