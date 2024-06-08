from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import product

@receiver(post_save, sender=product)
def alert_admin_on_product_out_of_stock(sender, product, **kwargs):
    if product.quantity == 0 and not product.alert_sent:
        # Send an email to the admin
        send_mail(
            'Product out of stock',
            f'The product "{product.quantity}" is out of stock!',
            'from@example.com',
            ['admin@example.com'],
            fail_silently=False,
        )
        product.alert_sent = True
        product.save()
    elif product.quantity > 0 and product.alert_sent:
        # Reset the alert_sent field if the quantity is no longer 0
        product.alert_sent = False
        product.save()
