# magpie_backend_python

## alembic commands

### before running commands
ensure __ init__.py in db.models is updated with new model
<br/>
ensure alembic.ini has the correct sqlalchemy.url

### check for upgrade operations

```alembic check```

### to create next revision for database

```alembic revision --autogenerate -m "0.0.x"```

### sqllite3 fix fk creation to use batching
transactions is the table name<br/>
batch_id is the column name<br/>
import_batches is the fk table name<br/>
fk_transactions_import_batches is the fk name
```python
    with op.batch_alter_table("transactions") as batch_op:
        batch_op.add_column(sa.Column('batch_id', sa.Integer,
                            sa.ForeignKey('import_batches.id', name='fk_transactions_import_batches')))
```

### upgrade the database

```alembic upgrade head```

### check the current revision

```alembic current```




## roadmap

done --pluggable accounts that contain the database connection.

--bulk delete of transactions based on batch

done --duplicate analysis, before or after import?

--live real-time view when importing data?

--live real-time view for maintaining the account balance, adjust when transactions are posted, transaction pending by default

done --implement categories and refacto transaction to use category object.

--mapping page for assigning categories to transactions

--weekly calendar view

--monthly calendar view

--daily at a glace view

--heatmap for purchases

--pivot table for purchases

--google auth login

--firebase auth login?

--budgets duh

--forecasting

done --transaction import from csv (done)

--mobile support

--sub users for accounts tied to matrix user access system

--ndb datastore support

--toast notifications



