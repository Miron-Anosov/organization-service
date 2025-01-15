import asyncio
import platform
import random
from typing import AsyncGenerator, Generator, List

import pytest
import pytest_asyncio
from factory_schemas import (
    CHILD_ACTIVITIES,
    GRANDCHILD_ACTIVITIES,
    ROOT_ACTIVITIES,
    ActivityFakeFactory,
    BuildingsFakeFactory,
    OrganizationFakeFactory,
    PhoneNumberFakeFactory,
)
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.configs.env import settings
from src.core.infrastructure.database.schemas.activity import Activity
from src.core.infrastructure.database.schemas.base import BaseModel
from src.core.infrastructure.database.schemas.buildings import Building
from src.core.infrastructure.database.schemas.organizations import Organization


# Database validation
class DatabaseTestModeException(Exception):
    """Database test mode exception."""

    pass


try:
    assert settings.db.MODE == "test", "Database Mode isn't 'test'."
except AssertionError as e:
    raise DatabaseTestModeException(e)

# Event loop setup
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore # noqa E501
else:
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())


@pytest_asyncio.fixture(scope="session", autouse=True)
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop=loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def connection() -> AsyncGenerator[AsyncConnection, None]:
    """Create database connection."""
    engine = create_async_engine(
        settings.db.get_url_database,
        echo=False,
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    async with engine.connect() as connection:
        yield connection


@pytest_asyncio.fixture(scope="session")
async def async_session(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncSession, None]:
    """Create a database session."""
    async_session_maker = async_sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest_asyncio.fixture(scope="session")
async def setup_buildings(async_session: AsyncSession) -> List[Building]:
    """Create test buildings."""
    buildings = [BuildingsFakeFactory.build() for _ in range(10)]
    async_session.add_all(buildings)
    await async_session.commit()
    return buildings


@pytest_asyncio.fixture(scope="session")
async def setup_base_activities(async_session: AsyncSession) -> List[Activity]:
    """Создание базовых активностей трех уровней."""
    all_activities = []

    # Создаем корневые активности (уровень 1)
    for root_name in ROOT_ACTIVITIES:
        root = ActivityFakeFactory.build(name=root_name)
        async_session.add(root)
        await async_session.flush()
        all_activities.append(root)

        # Создаем активности второго уровня
        child_names = CHILD_ACTIVITIES[root_name]
        for child_name in child_names:
            child = ActivityFakeFactory.build(
                name=child_name, parent=root, level=2
            )
            async_session.add(child)
            await async_session.flush()
            all_activities.append(child)

            # Создаем активности третьего уровня
            if child_name in GRANDCHILD_ACTIVITIES:
                grandchild_names = GRANDCHILD_ACTIVITIES[child_name]
                for grandchild_name in grandchild_names:
                    grandchild = ActivityFakeFactory.build(
                        name=grandchild_name, parent=child, level=3
                    )
                    async_session.add(grandchild)
                    await async_session.flush()
                    all_activities.append(grandchild)

    await async_session.commit()
    return all_activities


@pytest_asyncio.fixture(scope="function")
async def setup_organizations(
    async_session: AsyncSession,
    setup_buildings: List[Building],
    setup_base_activities: List[Activity],
) -> List[Organization]:
    """Создание 50 тестовых организаций со случайными зданиями и активностями разных уровней."""
    organizations = []

    # Группируем активности по уровням
    level1_activities = [a for a in setup_base_activities if a.level == 1]
    level2_activities = [a for a in setup_base_activities if a.level == 2]
    level3_activities = [a for a in setup_base_activities if a.level == 3]
    all_activities = level1_activities + level2_activities + level3_activities

    for _ in range(50):
        building = random.choice(setup_buildings)
        org = OrganizationFakeFactory.build(building_id=building.id)

        strategy = random.choice(["root", "mixed", "deep"])

        if strategy == "root":
            activities = random.sample(
                level1_activities, k=random.randint(1, 2)
            )
        elif strategy == "deep":
            activities = random.sample(
                level3_activities, k=random.randint(1, 3)
            )
        else:
            activities = random.sample(all_activities, k=random.randint(1, 4))

        org.activities = activities
        organizations.append(org)

    async_session.add_all(organizations)
    await async_session.commit()
    return organizations


@pytest_asyncio.fixture(scope="function")
async def setup_phone_numbers(
    async_session: AsyncSession, setup_organizations: List[Organization]
) -> List[PhoneNumberFakeFactory]:
    """Create phone numbers and link them to organizations."""
    phone_numbers = []

    for org in setup_organizations:
        for _ in range(random.randint(1, 3)):
            phone_number = PhoneNumberFakeFactory.build(organization_id=org.id)
            phone_numbers.append(phone_number)

    async_session.add_all(phone_numbers)
    await async_session.commit()
    return phone_numbers
