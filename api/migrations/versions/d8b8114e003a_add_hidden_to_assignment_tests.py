"""ADD hidden to assignment tests

Revision ID: d8b8114e003a
Revises: 3327ed0f2e0f
Create Date: 2021-04-13 11:44:17.221824

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d8b8114e003a"
down_revision = "3327ed0f2e0f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "assignment_test", sa.Column("hidden", sa.Boolean(), default=False)
    )
    conn = op.get_bind()
    with conn.begin():
        conn.execute('update assignment_test set hidden = 0;')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("assignment_test", "hidden")
    # ### end Alembic commands ###
