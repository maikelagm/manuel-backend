"""create_connections_table

Revision ID: 5771a016fc99
Revises: 
Create Date: 2023-12-01 06:47:59.179307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import UUIDType


# revision identifiers, used by Alembic.
revision: str = '5771a016fc99'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('connections',
    sa.Column('id', UUIDType(binary=False), nullable=False),
    sa.Column('db_engine', sa.String(), nullable=False),
    sa.Column('db_user', sa.String(), nullable=False),
    sa.Column('db_password', sa.String(), nullable=False),
    sa.Column('db_host', sa.String(), nullable=False),
    sa.Column('db_port', sa.String(), nullable=False),
    sa.Column('db_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('connections')
    # ### end Alembic commands ###
