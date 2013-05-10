import datetime

import sqlalchemy as sa
from alembic import op


def upgrade(engine):
    op.add_column('heartbeats', sa.Column('description', sa.String))

