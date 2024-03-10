import typing as t
from collections.abc import Iterable, Sequence

T = t.TypeVar("T")
K = t.TypeVar("K")
DEFAULT_ID_ATTR_NAME: t.Final = "id"


def chunker(seq: Sequence[T], size: int) -> list[Sequence[T]]:
    """Splits provided iterable into list of chunks of given size"""
    return [seq[pos : pos + size] for pos in range(0, len(seq), size)]


def idfy(
    obj: T | Iterable[T] | dict[t.Any, t.Any], id_field_name: str = DEFAULT_ID_ATTR_NAME
) -> dict[t.Any, T | dict[t.Any, t.Any]]:
    """Converts given object into dict with <id_field_name> values as a key
    and actual object as a value.

    If given object is a dict this function uses to get value of
    <id_field_name> key. If any other object - looks for <id_field_name>
    attribute.

    Raises ValueError if there's no appropriate id value found.

    Applied recursively if Iterable is given as an input.

    Args:
        obj: object to convert to dictionary
        id_field_name: name of the field/attribute to use to get
    """
    if isinstance(obj, dict):
        try:
            return {obj[id_field_name]: obj}
        except KeyError as err:
            raise ValueError(f"Can't get '{id_field_name}' key from {obj} dict") from err
    if isinstance(obj, Iterable):
        return {k: v for d in obj for k, v in idfy(d, id_field_name).items()}
    if hasattr(obj, id_field_name):
        return {getattr(obj, id_field_name): obj}
    raise ValueError(f"Can't get {id_field_name} attribute from {obj}")
