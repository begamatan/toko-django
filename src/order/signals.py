from django.db.models.signals import post_save
from django.dispatch import receiver

from toko.utils import send_email
from .models import Order

@receiver(post_save, sender=Order)
def send_mail_to_admin(sender, instance, created, **kwargs):
    if created == False and instance.status == 'settlement':
        send_email(
                f'Pembayaran Order {instance.id} Berhasil',
                f'Order ID {instance.id} telah dibayar, silahkan lakukan pengiriman',
                'no-reply@toko.test',
                ['admin@toko.test']
            )