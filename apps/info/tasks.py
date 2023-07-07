from celery import shared_task
from celery.signals import worker_ready

from apps.info.services import update_covid, update_currency


@shared_task
def update_covid_task():
    update_covid()


@shared_task
def update_currency_task():
    update_currency()


@worker_ready.connect
def at_start(sender, **kwargs):
    """Startup task for update decentraland sale data."""

    with sender.app.connection() as conn:
        sender.app.send_task("apps.info.tasks.update_covid_task", connection=conn)
        sender.app.send_task("apps.info.tasks.update_currency_task", connection=conn)
