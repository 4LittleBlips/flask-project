"""added replies

Revision ID: ed8883482870
Revises: d6dae5e9ed9f
Create Date: 2020-05-28 17:40:20.114588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed8883482870'
down_revision = 'd6dae5e9ed9f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('reply_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'comment', 'comment', ['reply_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_column('comment', 'reply_id')
    # ### end Alembic commands ###
