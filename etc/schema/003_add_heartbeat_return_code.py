import datetime

import sqlalchemy as sa
from alembic import op


def upgrade(engine):
    op.add_column('heartbeats', sa.Column('return_code', sa.Integer))

