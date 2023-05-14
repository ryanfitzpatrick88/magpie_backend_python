"""0.0.2

Revision ID: 8f686b101427
Revises: aec5d8a844cb
Create Date: 2023-05-12 20:17:49.895322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f686b101427'
down_revision = 'aec5d8a844cb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('import_batches',
    sa.Column('imported_at', sa.DateTime(), nullable=False),
    sa.Column('source', sa.String(length=255), nullable=False),
    sa.Column('file_name', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    # sa.ForeignKeyConstraint(['user_id'], ['users.id'], ), really bad idea to have without a name
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_import_batches_id'), 'import_batches', ['id'], unique=False)
    op.add_column('transactions', sa.Column('batch_id', sa.Integer(), nullable=True))
    #this failed, had to use the below
    #op.create_foreign_key(None, 'transactions', 'import_batches', ['batch_id'], ['id'])
    # ### end Alembic commands ###
    with op.batch_alter_table("transactions") as batch_op:
        batch_op.add_column(sa.Column('batch_id', sa.Integer,
                                      sa.ForeignKey('import_batches.id', name='fk_transactions_import_batches')))


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_column('transactions', 'batch_id')
    op.drop_index(op.f('ix_import_batches_id'), table_name='import_batches')
    op.drop_table('import_batches')
    # ### end Alembic commands ###
