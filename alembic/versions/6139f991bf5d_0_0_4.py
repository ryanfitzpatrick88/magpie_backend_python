"""0.0.4

Revision ID: 6139f991bf5d
Revises: 79dfb32e683b
Create Date: 2023-05-14 10:06:50.436603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6139f991bf5d'
down_revision = '79dfb32e683b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    #op.create_foreign_key(None, 'users', 'user_accounts', ['user_account_id'], ['id'])
    #op.add_column('users', sa.Column('user_account_id', sa.Integer(), nullable=True))
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column('user_account_id', sa.Integer, nullable=True))
        batch_op.create_foreign_key('fk_user_account_id', 'user_accounts', ['user_account_id'], ['id'])

    # ### end Alembic commands ###


def downgrade() -> None:
    pass
    # ### commands auto generated by Alembic - please adjust! ###
    #op.drop_constraint(None, 'users', type_='foreignkey')
    # ### end Alembic commands ###
