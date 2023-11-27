<%!
import re

%>"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def _upgrade_schema() -> None:
    ${context.get("dev_upgrades")}


def _upgrade_data() -> None:
    pass


def _upgrade() -> None:
    _upgrade_schema()
    _upgrade_data()


def _downgrade() -> None:
    ${context.get("dev_downgrades")}
<%
    db_names = config.get_main_option("databases")
%>
## generate an "upgrade_<xyz>() / downgrade_<xyz>()" function
## for each database name in the ini file.
% for db_name in re.split(r',\s*', db_names):

def upgrade_${db_name}() -> None:
    _upgrade()


def downgrade_${db_name}() -> None:
    _downgrade()

% endfor
