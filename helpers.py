from typing import Any, Type
from random import randrange
from datetime import timedelta

from objects.cores import BaseManager, OOPObject


def define_field_type(
        field_type,
        *,
        primary_key: bool = False,
        unique: bool = False,
        auto_increment: bool = False,
        foreign_key: Type[OOPObject] = None,
        default: Any = None,
) -> dict:
    assert field_type
    result = {"field_type": field_type}
    if primary_key:
        result["primary_key"] = True
        if auto_increment:
            result["auto_increment"] = True
    if not primary_key and unique:
        result["unique"] = True
    if foreign_key:
        result["foreign_key"] = foreign_key
    if default:
        result["default"] = default
    return result


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
