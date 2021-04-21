"""logons table

Revision ID: 78146da5ec62
Revises: b71759537ac1
Create Date: 2021-04-18 13:08:29.056069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78146da5ec62'
down_revision = 'b71759537ac1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip_address', sa.String(length=32), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_logon_timestamp'), 'logon', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_logon_timestamp'), table_name='logon')
    op.drop_table('logon')
    # ### end Alembic commands ###