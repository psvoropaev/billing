from billing.app.celery import celery_app
from billing.api.v1.controllers.operations import payment_procces
from billing.api.v1.controllers.retry import autoretry


@autoretry()
@celery_app.task(name='payment_task', bind=True)
async def payment_task(self, correlation_id: str, amount: float, reason_code: str, bill_number: str,
                       currency_code: str = 'USD',
                       bill_number_sender: str = None):
    await payment_procces(
        correlation_id=correlation_id,
        amount=amount,
        reason_code=reason_code,
        bill_number=bill_number,
        currency_code=currency_code,
        bill_number_sender=bill_number_sender
    )