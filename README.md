# magpie_backend_python

#alembic commands

#to create next revision for database

alembic revision --autogenerate -m "0.0.x"

#upgrade the database

alembic upgrade head

#check the current revision

alembic current

#check for upgrade operations

alembic check


--roadmap

--pluggable accounts that contain the database connection.

--bulk delete of transactions based on batch

--duplicate analysis, before or after import?

--live real-time view when importing data?

--live real-time view for maintaining the account balance, adjust when transactions are posted, transaction pending by default

--implement categories and refacto transaction to use category object.

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

--transaction import from csv (done)

--mobile support

--sub users for accounts tied to matrix user access system

--ndb datastore support

--toast notifications



