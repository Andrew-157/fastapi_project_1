"""Create Recommendation table

Revision ID: 5a6e5e8d8abe
Revises: 50e08dd093c7
Create Date: 2023-08-01 11:59:29.254819

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '5a6e5e8d8abe'
down_revision = '50e08dd093c7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recommendation',
    sa.Column('type_of_fiction', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('short_description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('opinion', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type_of_fiction')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recommendation')
    # ### end Alembic commands ###
