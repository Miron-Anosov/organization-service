from typing import List

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing_extensions import TypeVar

from src.core.infrastructure.database.schemas.activity import Activity
from src.core.infrastructure.database.schemas.organizations import Organization
from tests.database.factory_schemas import PhoneNumberFakeFactory

CallableType = TypeVar("CallableType")
ReturnType = TypeVar("ReturnType")


@pytest.mark.asyncio
async def test_organization_phones(
    async_session: AsyncSession,
    setup_phone_numbers: List[PhoneNumberFakeFactory],
) -> None:
    """Test organization phone numbers."""
    assert isinstance(async_session, AsyncSession)

    stmt = select(Organization).options(
        selectinload(Organization.phone_numbers)
    )

    result = await async_session.execute(stmt)
    organizations = result.unique().scalars().all()

    for org in organizations:
        print(org.phone_numbers)
        phones_count = len(org.phone_numbers)
        assert 1 <= phones_count <= 3, (
            f"Organization "
            f"ID:{org.id} "
            f" has {phones_count}"
            f" phones: {org.phone_numbers}"
            f" orgs: {organizations}"
        )


@pytest.mark.asyncio
async def test_organization_creation(
    async_session: AsyncSession,
    # setup_organizations: List[Organization]
) -> None:
    """Test organization creation with relations."""
    # Проверяем создание организаций
    stmt = select(Organization)
    result = await async_session.execute(stmt)
    organizations = result.scalars().all()

    assert (
        len(organizations) == 50
    ), "test_organization_creation count organizations not equally"

    # Проверяем, что у каждой организации есть здание
    for org in organizations:
        assert org.building is not None, "Organization should have a building"
        assert (
            org.building_id is not None
        ), "Organization should have building_id"
        assert len(org.activities) > 0, "Organization should have activities"


@pytest.mark.asyncio
async def test_activity_tree(
    async_session: AsyncSession,
    # setup_activities: List[ActivityFakeFactory]
) -> None:
    """Test activity tree structure."""
    assert isinstance(async_session, AsyncSession)

    # Проверяем структуру дерева активностей

    stmt = select(Activity).where(Activity.level == 1)
    result = await async_session.execute(stmt)
    root_activities = result.scalars().all()

    # Проверяем корневые активности
    assert len(root_activities) == 3

    # Проверяем, что нет активностей глубже 3-го уровня
    stmt = select(Activity).where(Activity.level > 3)
    result = await async_session.execute(stmt)
    deep_activities = result.scalars().all()
    assert len(deep_activities) == 0
