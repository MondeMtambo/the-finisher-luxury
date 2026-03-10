from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Contact, Deal, Notification
from .utils import OWNER_ADMIN_USERNAME


def _get_owner_admin() -> User | None:
    try:
        return User.objects.get(username__iexact=OWNER_ADMIN_USERNAME)
    except User.DoesNotExist:
        return None


@receiver(post_save, sender=Contact)
def notify_on_contact_created(sender, instance: Contact, created: bool, **kwargs):
    if not created:
        return
    admin_user = _get_owner_admin()
    title = 'New Contact Created'
    msg = f"{instance.user.username} created contact: {instance.first_name} {instance.last_name}"

    if admin_user:
        Notification.objects.create(
            recipient=admin_user,
            title=title,
            message=msg,
            entity_type='contact',
            entity_id=instance.id,
            meta={'email': instance.email}
        )

    Notification.objects.create(
        recipient=instance.user,
        title=title,
        message=f"Contact captured: {instance.first_name} {instance.last_name}",
        entity_type='contact',
        entity_id=instance.id,
        meta={'email': instance.email}
    )


@receiver(post_save, sender=Deal)
def notify_on_deal_created(sender, instance: Deal, created: bool, **kwargs):
    if not created:
        return
    admin_user = _get_owner_admin()
    title = 'New Deal Created'
    msg = f"{instance.user.username} created deal: {instance.title} (R{instance.value})"
    if admin_user:
        Notification.objects.create(
            recipient=admin_user,
            title=title,
            message=msg,
            entity_type='deal',
            entity_id=instance.id,
            meta={'stage': instance.stage}
        )
    Notification.objects.create(
        recipient=instance.user,
        title=title,
        message=f"Deal captured: {instance.title}",
        entity_type='deal',
        entity_id=instance.id,
        meta={'stage': instance.stage}
    )
