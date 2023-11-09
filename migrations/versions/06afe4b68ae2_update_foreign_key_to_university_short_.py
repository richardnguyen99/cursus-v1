"""update foreign key to university short name

Revision ID: 06afe4b68ae2
Revises: 9227a1eb4d2b
Create Date: 2023-11-04 23:33:15.597424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "06afe4b68ae2"
down_revision = "9227a1eb4d2b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("university_campuses", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "school_short_name", sa.String(length=32), nullable=False
            )
        )
        batch_op.drop_index("ix_university_campuses_school_id")
        batch_op.drop_constraint(
            "university_campuses_address_number_address_street_country_c_key",
            type_="unique",
        )
        batch_op.create_unique_constraint(
            None,
            [
                "address_number",
                "address_street",
                "country_code",
                "school_short_name",
            ],
        )
        batch_op.drop_constraint(
            "university_campuses_school_id_fkey", type_="foreignkey"
        )
        batch_op.create_foreign_key(
            None, "universities", ["school_short_name"], ["short_name"]
        )
        batch_op.drop_column("school_id")

    with op.batch_alter_table("university_domains", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "school_short_name", sa.String(length=32), nullable=False
            )
        )
        batch_op.drop_constraint(
            "university_domains_domain_name_school_id_key", type_="unique"
        )
        batch_op.create_unique_constraint(
            None, ["domain_name", "school_short_name"]
        )
        batch_op.drop_constraint(
            "university_domains_school_id_fkey", type_="foreignkey"
        )
        batch_op.create_foreign_key(
            None, "universities", ["school_short_name"], ["short_name"]
        )
        batch_op.drop_column("school_id")

    with op.batch_alter_table("university_founders", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "school_short_name", sa.String(length=32), nullable=False
            )
        )
        batch_op.drop_constraint(
            "university_founders_founder_name_school_id_key", type_="unique"
        )
        batch_op.create_unique_constraint(
            None, ["founder_name", "school_short_name"]
        )
        batch_op.drop_constraint(
            "university_founders_school_id_fkey", type_="foreignkey"
        )
        batch_op.create_foreign_key(
            None, "universities", ["school_short_name"], ["short_name"]
        )
        batch_op.drop_column("school_id")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("university_founders", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "school_id", sa.INTEGER(), autoincrement=False, nullable=False
            )
        )
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.create_foreign_key(
            "university_founders_school_id_fkey",
            "universities",
            ["school_id"],
            ["id"],
        )
        batch_op.drop_constraint(None, type_="unique")
        batch_op.create_unique_constraint(
            "university_founders_founder_name_school_id_key",
            ["founder_name", "school_id"],
        )
        batch_op.drop_column("school_short_name")

    with op.batch_alter_table("university_domains", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "school_id", sa.INTEGER(), autoincrement=False, nullable=False
            )
        )
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.create_foreign_key(
            "university_domains_school_id_fkey",
            "universities",
            ["school_id"],
            ["id"],
        )
        batch_op.drop_constraint(None, type_="unique")
        batch_op.create_unique_constraint(
            "university_domains_domain_name_school_id_key",
            ["domain_name", "school_id"],
        )
        batch_op.drop_column("school_short_name")

    with op.batch_alter_table("university_campuses", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "school_id", sa.INTEGER(), autoincrement=False, nullable=False
            )
        )
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.create_foreign_key(
            "university_campuses_school_id_fkey",
            "universities",
            ["school_id"],
            ["id"],
        )
        batch_op.drop_constraint(None, type_="unique")
        batch_op.create_unique_constraint(
            "university_campuses_address_number_address_street_country_c_key",
            ["address_number", "address_street", "country_code", "school_id"],
        )
        batch_op.create_index(
            "ix_university_campuses_school_id", ["school_id"], unique=False
        )
        batch_op.drop_column("school_short_name")

    # ### end Alembic commands ###