from billing.api.v1.controllers.operations import check_possibility_payment, payment
from billing.app.pg import transaction


@transaction
async def payment_task(connection, correlation_id: str, amount: float, reason_code: str, bill_number: str,
                       bill_number_sender: str = None):
    if await check_possibility_payment(correlation_id, connection):
        await payment(connection, correlation_id, amount, reason_code, bill_number, bill_number_sender)
