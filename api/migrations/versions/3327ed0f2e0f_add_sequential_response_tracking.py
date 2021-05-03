"""ADD sequential response tracking

Revision ID: 3327ed0f2e0f
Revises: 24999cac49d5
Create Date: 2021-04-01 00:30:31.115702

"""
from hashlib import sha256
from os import urandom

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "3327ed0f2e0f"
down_revision = "24999cac49d5"
branch_labels = None
depends_on = None


def move_responses_up():
    conn = op.get_bind()
    with conn.begin():
        responses = conn.execute(
            'select owner_id, id, response, created, last_updated from assigned_student_question;'
        ).fetchall()

        block = urandom(32)
        for owner_id, assigned_question_id, response, created, last_updated in responses:
            print(f'moving response {owner_id} {assigned_question_id}')
            block = sha256(block).digest()
            conn.execute(
                'insert into assigned_student_response values (%s, %s, %s, %s, %s);',
                (sha256(block).hexdigest()[:32], assigned_question_id, response, created, last_updated),
            )


def move_responses_down():
    conn = op.get_bind()
    with conn.begin():
        responses = conn.execute(
            'select id, assigned_question_id, response, last_updated from assigned_student_response;'
        ).fetchall()

        block = urandom(32)
        for response_id, assigned_question_id, response, last_updated in responses:
            print(f'moving response {assigned_question_id}')
            block = sha256(block).digest()
            conn.execute(
                'update assigned_student_question set response = %s, last_updated = %s  where id = %s;',
                (response, last_updated, assigned_question_id),
            )
            conn.execute(
                'delete from asigned_student_response where id = %s;', (response_id,)
            )


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "assigned_student_response",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column(
            "assigned_question_id", sa.String(length=128), nullable=False
        ),
        sa.Column("response", sa.TEXT(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["assigned_question_id"],
            ["assigned_student_question.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_assigned_student_response_assigned_question_id"),
        "assigned_student_response",
        ["assigned_question_id"],
        unique=False,
    )
    move_responses_up()
    op.drop_column("assigned_student_question", "response")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "assigned_student_question",
        sa.Column("response", mysql.TEXT(), nullable=False),
    )
    op.drop_index(
        op.f("ix_assigned_student_response_question_id"),
        table_name="assigned_student_response",
    )
    move_responses_down()
    op.drop_table("assigned_student_response")
    # ### end Alembic commands ###
