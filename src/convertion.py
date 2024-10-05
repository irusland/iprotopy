# pylint:disable=no-name-in-module
import dataclasses
from abc import ABC
from typing import (
    Any,
    Optional,
    Tuple,
)

from convertion_fix import PLACEHOLDER

# Proto 3 data types
TYPE_ENUM = 'enum'
TYPE_BOOL = 'bool'
TYPE_INT32 = 'int32'
TYPE_INT64 = 'int64'
TYPE_UINT32 = 'uint32'
TYPE_UINT64 = 'uint64'
TYPE_SINT32 = 'sint32'
TYPE_SINT64 = 'sint64'
TYPE_FLOAT = 'float'
TYPE_DOUBLE = 'double'
TYPE_FIXED32 = 'fixed32'
TYPE_SFIXED32 = 'sfixed32'
TYPE_FIXED64 = 'fixed64'
TYPE_SFIXED64 = 'sfixed64'
TYPE_STRING = 'string'
TYPE_BYTES = 'bytes'
TYPE_MESSAGE = 'message'
TYPE_MAP = 'map'


@dataclasses.dataclass(frozen=True)
class FieldMetadata:
    """Stores internal metadata used for parsing & serialization."""

    # Protobuf field number
    number: int
    # Protobuf type name
    proto_type: str
    # Map information if the proto_type is a map
    map_types: Optional[Tuple[str, str]] = None
    # Groups several "one-of" fields together
    group: Optional[str] = None
    # Describes the wrapped type (e.g. when using google.protobuf.BoolValue)
    wraps: Optional[str] = None
    # Is the field optional
    optional: Optional[bool] = False

    @staticmethod
    def get(field: dataclasses.Field) -> 'FieldMetadata':
        """Return the field metadata for a dataclass field."""
        return field.metadata['proto']


def dataclass_field(
    number: int,
    proto_type: str,
    *,
    map_types: Optional[Tuple[str, str]] = None,
    group: Optional[str] = None,
    wraps: Optional[str] = None,
    optional: bool = False,
) -> dataclasses.Field:
    """Create a dataclass field with attached protobuf metadata."""
    return dataclasses.field(
        default=None if optional else PLACEHOLDER,  # type:ignore
        metadata={
            'proto': FieldMetadata(
                number, proto_type, map_types, group, wraps, optional
            )
        },
    )


def enum_field(number: int, group: Optional[str] = None, optional: bool = False) -> Any:
    return dataclass_field(number, TYPE_ENUM, group=group, optional=optional)


def bool_field(number: int, group: Optional[str] = None, optional: bool = False) -> Any:
    return dataclass_field(number, TYPE_BOOL, group=group, optional=optional)


def int32_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_INT32, group=group, optional=optional)


def int64_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_INT64, group=group, optional=optional)


def uint32_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_UINT32, group=group, optional=optional)


def uint64_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_UINT64, group=group, optional=optional)


def sint32_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_SINT32, group=group, optional=optional)


def sint64_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_SINT64, group=group, optional=optional)


def float_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_FLOAT, group=group, optional=optional)


def double_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_DOUBLE, group=group, optional=optional)


def fixed32_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_FIXED32, group=group, optional=optional)


def fixed64_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_FIXED64, group=group, optional=optional)


def sfixed32_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_SFIXED32, group=group, optional=optional)


def sfixed64_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_SFIXED64, group=group, optional=optional)


def string_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_STRING, group=group, optional=optional)


def bytes_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_BYTES, group=group, optional=optional)


def message_field(
    number: int,
    group: Optional[str] = None,
    wraps: Optional[str] = None,
    optional: bool = False,
) -> Any:
    return dataclass_field(
        number, TYPE_MESSAGE, group=group, wraps=wraps, optional=optional
    )


def map_field(
    number: int, key_type: str, value_type: str, group: Optional[str] = None
) -> Any:
    return dataclass_field(
        number, TYPE_MAP, map_types=(key_type, value_type), group=group
    )


class Message: ...


class Service(ABC):
    _stub_factory: Any

    def __init__(self, channel, metadata):
        self.stub = self._stub_factory(channel)
        self.metadata = metadata


_UNKNOWN: Any = object()

# pylint:disable=too-many-nested-blocks
# pylint:disable=too-many-branches
# pylint:disable=too-many-locals
# pylint:disable=too-many-nested-blocks
# pylint:disable=too-many-statements
