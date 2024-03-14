import stripe
import os


stripe_api_key = os.getenv("STRIPE_API_KEY")


def create_product(payment):
    product = stripe.Product.create(name=f"{payment.course}")
    return product


def create_price(payment, product):
    price = stripe.Price.create(
        currency="usd",
        unit_amount=payment.amount,
        product=product.id,
        # recurring={"interval": "month"},
    )
    return price


def get_session(price):

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": f"{price.id}", "quantity": 1}],
        mode="payment",
    )
    return session.url
