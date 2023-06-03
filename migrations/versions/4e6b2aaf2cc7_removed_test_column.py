"""removed test column

Revision ID: 4e6b2aaf2cc7
Revises: bc254782d8b2
Create Date: 2023-04-21 21:13:27.923092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e6b2aaf2cc7'
down_revision = 'bc254782d8b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('test')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('test', sa.VARCHAR(), nullable=True))

    # ### end Alembic commands ###