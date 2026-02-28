import os

services = {
    'auth-service': 'from app.models.user import User',
    'account-service': 'from app.models.account import Account',
    'transaction-service': 'from app.models.transaction import Transaction\nfrom app.models.account import Account',
    'loan-service': 'from app.models.loan import Loan',
}

env_template = """from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import DATABASE_URL
from app.core.database import Base
{imports}

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""

mako_content = """\"\"\"${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

\"\"\"
from alembic import op
import sqlalchemy as sa

revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
"""

for service, imports in services.items():
    os.makedirs(f'{service}/alembic/versions', exist_ok=True)
    with open(f'{service}/alembic/env.py', 'w') as f:
        f.write(env_template.replace('{imports}', imports))
    with open(f'{service}/alembic/script.py.mako', 'w') as f:
        f.write(mako_content)
    print(f'Fixed {service}/alembic/env.py and script.py.mako')

print('All done!')