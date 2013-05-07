import datetime

import sqlalchemy as sa
from alembic import op


def upgrade(engine):

    meta = sa.MetaData(bind=engine)
    meta.reflect()

    services = sa.Table('services', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
    )
    services.create()

    components = sa.Table('service_components', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('service_id', sa.Integer, sa.ForeignKey('services.id'), nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('cron_spec', sa.String)
    )
    components.create()

    heartbeats = sa.Table('heartbeats', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('component_id', sa.Integer, sa.ForeignKey('service_components.id')),
        sa.Column('time', sa.DateTime, nullable=False),
        sa.Column('remote_addr', sa.String, nullable=False),
        sa.Column('remote_name', sa.String, nullable=False),
    )
    heartbeats.create()

    agents = sa.Table('agents', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('service_name', sa.String, nullable=False),
        sa.Column('component_name', sa.String, nullable=False),
        sa.Column('cron_spec', sa.String, nullable=False),
        sa.Column('type', sa.String, nullable=False),
        sa.Column('job', sa.String, nullable=False),
    )
    agents.create()



