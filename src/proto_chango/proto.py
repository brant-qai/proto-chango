import logging
from typing import cast, Any
from datetime import datetime, UTC

from proto_chango import models_pb2
from uuid import UUID
from .models import Node, Object

LOG = logging.getLogger(__name__)


def convert_pb_datetime_to_datetime(dt_pb: Any) -> datetime:
    """Convert a protobuf datetime to a datetime instance."""
    return datetime.fromisoformat(dt_pb.value)


def write_datetime_to_pb_datetime(dt: datetime, dt_pb: Any) -> None:
    """Write datetime data to a protobuf datetime."""
    if (tzinfo := dt.tzinfo) is None:
        dt = dt.replace(tzinfo=UTC)
    elif tzinfo.utcoffset(dt) is None:
        dt = dt.replace(tzinfo=UTC)
    as_str = dt.isoformat("T")
    dt_pb.value = as_str


def encode_datetime(dt: datetime) -> bytes:
    """Encode an Object instance in protobuf format."""
    pb_dt = models_pb2.DateTime()  # type: ignore
    write_datetime_to_pb_datetime(dt, pb_dt)
    as_bytes = pb_dt.SerializeToString()
    return cast(bytes, as_bytes)


def decode_datetime(encoded_object: bytes) -> datetime:
    """Decode a protobuf Object value into an Object instance."""
    dt_pb = models_pb2.DateTime()  # type: ignore
    dt_pb.ParseFromString(encoded_object)
    return datetime.fromisoformat(dt_pb.value)


def write_node_to_pb_node(node: Node, pb_node: Any) -> None:
    """Write data from a Node instance into a protobuf node object."""
    pb_node.id = node.id.hex
    for n in node.nodes:
        to_add = pb_node.nodes.add()
        write_node_to_pb_node(n, to_add)


def convert_node_to_pb_node(node: Node) -> Any:
    """Convert a Node instance to a protobuf node."""
    pb_node = models_pb2.Node()  # type: ignore
    write_node_to_pb_node(node, pb_node)
    return pb_node


def encode_node(node: Node) -> bytes:
    """Encode a Node instance in protobuf format."""
    pb_node = convert_node_to_pb_node(node)
    as_bytes = pb_node.SerializeToString()
    return cast(bytes, as_bytes)


def convert_pb_node_to_node(pb_node: Any) -> Node:
    """Convert a protobuf node to a Node instance."""
    n = Node(id=UUID(pb_node.id), nodes=[convert_pb_node_to_node(n) for n in pb_node.nodes])
    return n


def decode_node(encoded_node: bytes) -> Node:
    """Given a protobuf message in bytes, decodes into a Node instance."""
    pb_node = models_pb2.Node()  # type: ignore
    pb_node.ParseFromString(encoded_node)
    return convert_pb_node_to_node(pb_node)


def serialize_datetime(dt: datetime) -> str:
    """Serialize a datetime object as a string."""
    if (tzinfo := dt.tzinfo) is None:
        dt = dt.replace(tzinfo=UTC)
    elif tzinfo.utcoffset(dt) is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.isoformat("T")


def deserialize_datetime(dt_str: str) -> datetime:
    """Deserialize a datetime object from an ISO formatted string."""
    return datetime.fromisoformat(dt_str)


def encode_object(obj: Object) -> bytes:
    """Encode an Object instance in protobuf format."""
    pb_obj = models_pb2.Object()  # type: ignore
    pb_obj.name = obj.name
    pb_obj.created_at = serialize_datetime(obj.created_at)

    write_node_to_pb_node(obj.node, pb_obj.node)
    write_datetime_to_pb_datetime(obj.updated_at, pb_obj.updated_at)
    as_bytes = pb_obj.SerializeToString()
    return cast(bytes, as_bytes)


def decode_object(encoded_object: bytes) -> Object:
    """Decode a protobuf Object value into an Object instance."""
    pb_obj = models_pb2.Object()  # type: ignore
    pb_obj.ParseFromString(encoded_object)
    obj = Object(
        name=pb_obj.name,
        created_at=deserialize_datetime(pb_obj.created_at),
        updated_at=convert_pb_datetime_to_datetime(pb_obj.updated_at),
        node=convert_pb_node_to_node(pb_obj.node),
    )
    return obj
