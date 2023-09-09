from enum import Enum
from typing import Optional


class Status(Enum):
    SUCCESS = 'success'
    ERROR = 'error'


def create_response(
        message: str,
        data: Optional[dict | None] = None,
        warnings: Optional[list | None] = None,
        status=Status.SUCCESS,
) -> dict:
    """
    Генерує відповідь у вигляді словника

    :param message:
    :param data:
    :param warnings:
    :param status:
    :return:
    """
    return {
        'status': status.value,
        'warnings': [] if warnings is None else warnings,
        'data': dict() if data is None else data,

        'message': message
    }

