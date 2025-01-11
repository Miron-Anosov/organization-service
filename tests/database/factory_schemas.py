# type: ignore
import random

import factory
from mimesis import Address, Finance, Generic, Person
from mimesis.locales import Locale

from src.core.infrastructure.database.schemas.activity import Activity
from src.core.infrastructure.database.schemas.buildings import Building
from src.core.infrastructure.database.schemas.organizations import Organization
from src.core.infrastructure.database.schemas.phones import PhoneNumber

generic = Generic(locale=Locale.RU)
address = Address(locale=Locale.RU)
person = Person(locale=Locale.RU)
business = Finance(locale=Locale.RU)


class BuildingsFakeFactory(factory.Factory):
    class Meta:
        model = Building

    address = factory.Iterator(
        [
            f"{address.city()}, {address.street_name()},"
            f" д. {generic.random.randint(1, 100)}"
            for _ in range(5)
        ]
    )

    @factory.lazy_attribute
    def location(self) -> str:
        return f"SRID=4326;POINT({address.longitude()} {address.latitude()})"


class OrganizationFakeFactory(factory.Factory):
    class Meta:
        model = Organization

    name = factory.LazyAttribute(
        lambda _: f"{business.company()} {business.company_type()}"
    )
    building_id = factory.SubFactory(BuildingsFakeFactory)


class PhoneNumberFakeFactory(factory.Factory):
    class Meta:
        model = PhoneNumber

    number = factory.LazyAttribute(
        lambda _: person.telephone(mask="+7 (###) ###-##-##")
    )
    organization_id = factory.SubFactory(OrganizationFakeFactory)


ROOT_ACTIVITIES = ["Еда", "Автомобили", "Услуги"]
CHILD_ACTIVITIES = {
    "Еда": ["Мясная продукция", "Молочная продукция", "Кондитерские изделия"],
    "Автомобили": ["Грузовые", "Легковые", "Запчасти"],
    "Услуги": ["Ремонт", "Доставка", "Аксессуары"],
}


class ActivityFakeFactory(factory.Factory):
    class Meta:
        model = Activity

    name = factory.LazyAttribute(
        lambda obj: (
            random.choice(ROOT_ACTIVITIES)
            if not obj.parent
            else random.choice(CHILD_ACTIVITIES[obj.parent.name])
        )
    )
    parent_id = None
    level = factory.LazyAttribute(
        lambda obj: 1 if not obj.parent_id else min(obj.parent.level + 1, 3)
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        parent = kwargs.pop("parent", None)
        if parent:
            kwargs["parent_id"] = parent.id  # noqa
            kwargs["level"] = min(parent.level + 1, 3)  # noqa
        return super()._create(model_class, *args, **kwargs)  # noqa
