import sqlalchemy as sa
from sqlalchemy.sql import select, func

from web.app.config import config

metadata = sa.MetaData(schema=config.DB_SCHEMA)

user = sa.Table(
    'user',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column('name', sa.String(255), nullable=False)
)

wallet = sa.Table(
    'wallet',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column('code', sa.String(32), nullable=False, index=True, unique=True),
    sa.Column('user_id', sa.ForeignKey('user.id'), index=True, nullable=False)
)

reason = sa.Table(
    'reason',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column('code', sa.String(255), nullable=False, index=True, unique=True),
    sa.Column('name', sa.String(255), nullable=False)
)

currency = sa.Table(
    'currency',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column('alias', sa.String(255), nullable=False, index=True, unique=True),
    sa.Column('name', sa.String(255), nullable=False)
)

operation = sa.Table(
    'operation',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column('reason_id', sa.ForeignKey('reason.id'), index=True, nullable=False),
    sa.Column('wallet_id', sa.ForeignKey('wallet.id'), index=True, nullable=False),
    sa.Column('connected_wallet_id', sa.ForeignKey('wallet.id'), index=True, nullable=True),
    sa.Column('amount', sa.Float, nullable=False),
    sa.Column('opdate', sa.DateTime(timezone=True), nullable=False, index=True, server_default=func.now())
)

