"""init schemas

Revision ID: 5f63b3fc0613
Revises: 
Create Date: 2025-01-10 14:27:24.256606

"""

from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5f63b3fc0613"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "activity",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.CheckConstraint("level <= 3", name="check_max_level"),
        sa.ForeignKeyConstraint(
            ["parent_id"], ["activity.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "building",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column(
            "location",
            geoalchemy2.types.Geometry(
                geometry_type="POINT",
                srid=4326,
                from_text="ST_GeomFromEWKT",
                name="geometry",
                nullable=False,
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_building_location",
        "building",
        ["location"],
        unique=False,
        postgresql_using="gist",
    )
    op.create_index(
        op.f("ix_building_address"), "building", ["address"], unique=False
    )
    op.create_table(
        "organization",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("building_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["building_id"], ["building.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_organization_name"), "organization", ["name"], unique=False
    )
    op.create_table(
        "organization_activity",
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("activity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["activity_id"], ["activity.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"], ["organization.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("organization_id", "activity_id"),
    )
    op.create_table(
        "phone_number",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("number", sa.String(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"], ["organization.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("phone_number")
    op.drop_table("organization_activity")
    op.drop_index(op.f("ix_organization_name"), table_name="organization")
    op.drop_table("organization")
    op.drop_index(op.f("ix_building_address"), table_name="building")
    op.drop_index(
        "idx_building_location", table_name="building", postgresql_using="gist"
    )
    op.drop_table("building")
    op.drop_table("activity")
    # ### end Alembic commands ###
