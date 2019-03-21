from collections.abc import (
    Iterable,
    Sequence,
)

from .base import (  # noqa: F401
    BaseSedes,
    FixedSizedSedes,
    LengthPrefixedSedes,
)
from .boolean import (  # noqa: F401
    Boolean,
    boolean,
)
from .bytes import (  # noqa: F401
    Bytes,
    bytes_sedes,
)
from .bytes_n import (  # noqa: F401
    BytesN,
    bytes32,
    bytes48,
    bytes96,
)
from .container import (  # noqa: F401
    Container,
)
from .list import (  # noqa: F401
    List,
    empty_list,
)
from .serializable import (  # noqa: F401
    Serializable,
)
from .uint import (  # noqa: F401
    UInt,
    uint8,
    uint16,
    uint32,
    uint64,
    uint128,
    uint256,
)

sedes_by_name = {
    "boolean": boolean,
    "bytes_sedes": bytes_sedes,
    "bytes32": bytes32,
    "bytes48": bytes48,
    "bytes96": bytes96,
    "empty_list": empty_list,

    "uint8": uint8,
    "uint16": uint16,
    "uint32": uint32,
    "uint64": uint64,
    "uint128": uint128,
    "uint256": uint256,
}


def infer_list_sedes(value):
    if len(value) == 0:
        return empty_list
    else:
        try:
            element_sedes = infer_sedes(value[0])
        except TypeError:
            raise TypeError("Could not infer sedes for list elements")
        else:
            return List(element_sedes)


def infer_sedes(value):
    """
    Try to find a sedes objects suitable for a given Python object.
    """
    if isinstance(value.__class__, BaseSedes):
        # Mainly used for `Serializable` Classes
        return value.__class__

    elif isinstance(value, bool):
        return boolean

    elif isinstance(value, int):
        raise TypeError("uint sedes object or uint string needs to be specified for ints")

    elif isinstance(value, (bytes, bytearray)):
        return bytes_sedes

    elif isinstance(value, Sequence):
        return infer_list_sedes(value)

    elif isinstance(value, Iterable):
        raise TypeError("Cannot infer list sedes for iterables that are not sequences")

    else:
        raise TypeError(f"Did not find sedes handling type {type(value).__name__}")
