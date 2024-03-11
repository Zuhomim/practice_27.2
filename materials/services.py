import stripe
import os


stripe_api_key = os.getenv("STRIPE_API_KEY")


def get_session(payment):
    product = stripe.Product.create(name=f"{payment.name}")

    price = stripe.Price.create(
        currency="usd",
        unit_amount=payment.price,
        product=product.id,
        # recurring={"interval": "month"},
    )

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": f"{price.id}", "quantity": 1}],
        mode="payment",
    )

    return session.url
