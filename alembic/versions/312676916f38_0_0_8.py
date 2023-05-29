"""0.0.8

Revision ID: 312676916f38
Revises: 004ec3ee751c
Create Date: 2023-05-27 13:24:34.359928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '312676916f38'
down_revision = '004ec3ee751c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('budgets', 'category_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('budgets', 'category_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
