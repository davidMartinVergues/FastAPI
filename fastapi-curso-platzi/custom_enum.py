from enum import Enum


class CustomEnum(str, Enum):
    @classmethod
    def choices(cls) -> tuple[tuple[str, str],...]:
        return tuple([(enum_item.name, enum_item.value) for enum_item in cls])

    @classmethod
    def values(cls):
        return [e.value for e in cls]
