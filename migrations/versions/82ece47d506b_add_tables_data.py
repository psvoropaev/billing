"""add tables data

Revision ID: 82ece47d506b
Revises: 871ffc85aff2
Create Date: 2020-07-30 22:30:52.930152

"""
from alembic import op

from billing.app.config import config
from billing.models import metadata

# revision identifiers, used by Alembic.
revision = '82ece47d506b'
down_revision = '260c68d35a2c'
branch_labels = None
depends_on = None


def upgrade():
    op.bulk_insert(
        metadata.tables[f'{config.DB_SCHEMA}.currency'], [
            {'alias': 'USD', 'name': 'Dollar'}
        ]
    )

    op.bulk_insert(
        metadata.tables[f'{config.DB_SCHEMA}.reason'], [
            {
                'code': 'TRANSFER', 
                'name': 'Перевод денежных средств с одного кошелька на другой', 
                'using_second_bill_number': True
            },
            {
                'code': 'TOPUP',
                'name': 'Зачисление денежных средств на кошелек клиента',
                'using_second_bill_number': False
            }
        ]
    )


def downgrade():
    op.execute(f'DELETE FROM {config.DB_SCHEMA}.operation')
    op.execute(f'DELETE FROM {config.DB_SCHEMA}.currency')
    op.execute(f'DELETE FROM {config.DB_SCHEMA}.reason')
