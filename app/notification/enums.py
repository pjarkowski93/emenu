import enum

from notification.email import EmailSender


class NotificationTypes(enum.Enum):
    EMAIL = enum.auto()

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(i.name, i.name) for i in cls]


class NotificationStatuses(enum.Enum):
    CREATED = enum.auto()
    SENT = enum.auto()
    FAILED = enum.auto()

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(i.name, i.name) for i in cls]


class NotificationSenderEnum(enum.Enum):
    EMAIL = EmailSender
