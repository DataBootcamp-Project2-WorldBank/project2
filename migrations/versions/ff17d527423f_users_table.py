"""users table

Revision ID: ff17d527423f
Revises: 
Create Date: 2021-04-18 22:13:11.395380

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ff17d527423f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('logon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip_address', sa.String(length=32), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_logon_timestamp'), 'logon', ['timestamp'], unique=False)
    op.drop_table('project_info_summary1')
    op.drop_table('countries')
    op.drop_table('country_regions')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('country_regions',
    sa.Column('region_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('region_name', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('parent_region', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('region_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('countries',
    sa.Column('country_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('region_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('country_name', mysql.VARCHAR(length=60), nullable=True),
    sa.Column('country_code', mysql.VARCHAR(length=10), nullable=False),
    sa.PrimaryKeyConstraint('country_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('project_info_summary1',
    sa.Column('country_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('year', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('total_projects', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('satisfactory_projects', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('unsatistafcory_projects', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('country_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_index(op.f('ix_logon_timestamp'), table_name='logon')
    op.drop_table('logon')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
