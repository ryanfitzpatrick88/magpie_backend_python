"""0.0.6

Revision ID: 62abafcfc3ff
Revises: 4236000a2389
Create Date: 2023-05-14 11:35:21.539121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62abafcfc3ff'
down_revision = '4236000a2389'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('import_batches') as batch_op:
        batch_op.alter_column('user_id',
                              existing_type=sa.INTEGER(),
                              nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('import_batches', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
