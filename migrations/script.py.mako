"""${message}

Revision ID: ${up_revision}
<<<<<<< HEAD
Revises: ${down_revision}
Create Date: ${create_date}

"""
=======
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}
>>>>>>> 17-app-1

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
<<<<<<< HEAD

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}
=======
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

>>>>>>> 17-app-1

def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
    ${downgrades if downgrades else "pass"}
