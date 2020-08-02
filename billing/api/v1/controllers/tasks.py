from billing.api.v1.controllers.operations import payment_procces
from billing.api.v1.controllers.retry import autoretry


@autoretry()
async def payment_task(correlation_id: str, amount: float, reason_code: str, bill_number: str,
                       bill_number_sender: str = None):
    """
    Auto retry task
    :param correlation_id: unique code to prevent repeated operations
    :param amount: amount of money
    :param reason_code: reason for crediting funds
    :param bill_num_recipient: recipient
    :param bill_num_sender: sender
    :return:
    """
    await payment_procces(
        correlation_id=correlation_id,
        amount=amount,
        reason_code=reason_code,
        bill_number=bill_number,
        bill_number_sender=bill_number_sender
    )