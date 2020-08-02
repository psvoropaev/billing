import pytest
from unittest.mock import patch

from billing.api.v1.controllers.tasks import payment_task


async def test_autoretry():
    payment_task.delay(1,2,3,4,5)