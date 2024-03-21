from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import mailtrap as mt

from .models import *


def send_notification_email(user_email, subject, context, template_name):
    message = render_to_string(f'email/{template_name}.html', context)

    mail = mt.Mail(
        sender=mt.Address(email="no-reply@roy-meyer.de", name="EmergencyTrack"),
        to=[mt.Address(email=user_email)],
        subject=subject,
        html=message
    )

    client = mt.MailtrapClient(token="318b10a05e1d99674b60e465dc11c80f")
    client.send(mail)


@receiver(post_save, sender=BlockedRoads)
def notify_blocked_roads_subscribers(sender, instance, created, **kwargs):
    if created:
        department = Departments.objects.get(department_type=2, county_id=instance.county.county_id)
        subscribers = Subscriptions.objects.filter(department=department)

        subject = f"EmergencyTrack - NEW BLOCKED ROAD IN {instance.county.county_name}!"
        context = {'blocked_road': instance}

        for subscriber in subscribers:
            send_notification_email(subscriber.user.email, subject, context, 'blocked_road_notification')


@receiver(post_save, sender=SecurityConcerns)
def notify_security_concern_subscribers(sender, instance, created, **kwargs):
    if created:
        department = Departments.objects.get(department_type=2, county_id=instance.county.county_id)
        subscribers = Subscriptions.objects.filter(department=department)

        subject = f"EmergencyTrack - NEW SECURITY CONCERN IN {instance.county.county_name}!"
        context = {'security_concern': instance}

        for subscriber in subscribers:
            send_notification_email(subscriber.user.email, subject, context, 'security_concern_notification')


@receiver(post_save, sender=WeatherEvents)
def notify_weather_event_subscribers(sender, instance, created, **kwargs):
    if created:
        department = Departments.objects.get(department_type=3, county_id=instance.county.county_id)
        subscribers = Subscriptions.objects.filter(department=department)

        subject = f"EmergencyTrack - NEW EXTREM WEATHER EVENT IN {instance.county.county_name}!"
        context = {'weather_event': instance}

        for subscriber in subscribers:
            send_notification_email(subscriber.user.email, subject, context, 'weather_event_notification')


@receiver(post_save, sender=Wildfires)
def notify_wildfires_subscribers(sender, instance, created, **kwargs):
    if created:
        department = Departments.objects.get(department_type=4, county_id=instance.county.county_id)
        subscribers = Subscriptions.objects.filter(department=department)

        subject = f"EmergencyTrack - NEW WILDFIRE IN {instance.county.county_name}!"
        context = {'wildfire': instance}

        for subscriber in subscribers:
            send_notification_email(subscriber.user.email, subject, context, 'wildfire_notification')

