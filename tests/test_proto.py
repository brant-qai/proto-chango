from unittest import TestCase
from uuid import UUID
from datetime import datetime, UTC
from zoneinfo import ZoneInfo

from proto_chango.proto import encode_node, decode_node, encode_object, decode_object, encode_datetime, decode_datetime
from proto_chango.models import Node, Object


class TestProto(TestCase):
    def test_encode_node(self):
        """A Node instance can be encoded in protobuf format."""
        expected = b"\n 8298948dc66b43edaa221cff9178ae85"
        actual = encode_node(Node(id=UUID("8298948dc66b43edaa221cff9178ae85")))
        self.assertEqual(expected, actual)

    def test_dencode_node(self):
        """A Node instance can be decoded from a protobuf value."""
        protobuf_value = b"\n 4c76df84639c44f6b9cf3b2a0798d8a3"
        expected = Node(id=UUID("4c76df84-639c-44f6-b9cf-3b2a0798d8a3"))
        actual = decode_node(protobuf_value)
        self.assertEqual(expected, actual)

    def test_node_roundtrip(self):
        """A node instance survives a roundtrip through protobuf."""
        original = Node(
            id=UUID("63966bf7d2bf4b65b997571d9d51398c"),
            nodes=[
                Node(id=UUID("1f616d205bec4b2e9ab96d4579411410")),
                Node(id=UUID("e65465bccf684efbb61c9a00b838a966")),
                Node(
                    id=UUID("bfc7fc1c99d244ec98f5a5d040d2db91"),
                    nodes=[Node(id=UUID("3d62e1bef81c476a9c508a5cd4cfcf44"))],
                ),
            ],
        )
        output = encode_node(original)
        restored = decode_node(output)
        self.assertEqual(original, restored)

    def test_encode_object(self):
        """An object instance can be encoded in protobuf format."""
        instance = Object(
            name="test",
            node=Node(id=UUID("8298948dc66b43edaa221cff9178ae85")),
            created_at=datetime(2024, 12, 20, 16, 53, 49, 493484, tzinfo=UTC),
            updated_at=datetime(2022, 2, 2, 22, 22, 22, 493484, tzinfo=UTC),
        )
        expected = b'\x1a"\n 8298948dc66b43edaa221cff9178ae85"\x04test* 2024-12-20T16:53:49.493484+00:002"\n 2022-02-02T22:22:22.493484+00:00'
        actual = encode_object(instance)
        self.assertEqual(expected, actual)

    def test_decode_object(self):
        """An object instance can be decoded from protobuf format."""
        protobuf_value = b'\x1a"\n e65465bccf684efbb61c9a00b838a966"\x04test* 2022-02-02T22:22:22.493484+00:002"\n 2022-02-02T22:22:22.493484+00:00'
        expected = Object(
            name="test",
            node=Node(id=UUID("e65465bccf684efbb61c9a00b838a966")),
            created_at=datetime(2022, 2, 2, 22, 22, 22, 493484, tzinfo=UTC),
            updated_at=datetime(2022, 2, 2, 22, 22, 22, 493484, tzinfo=UTC),
        )
        actual = decode_object(protobuf_value)
        self.assertEqual(expected, actual)

    def test_object_roundtrip(self):
        """An object instance survives a roundtrip through protobuf."""
        original = Object(
            name="test",
            node=Node(
                id=UUID("63966bf7d2bf4b65b997571d9d51398c"),
                nodes=[
                    Node(id=UUID("1f616d205bec4b2e9ab96d4579411410")),
                    Node(id=UUID("e65465bccf684efbb61c9a00b838a966")),
                    Node(
                        id=UUID("bfc7fc1c99d244ec98f5a5d040d2db91"),
                        nodes=[Node(id=UUID("3d62e1bef81c476a9c508a5cd4cfcf44"))],
                    ),
                ],
            ),
            created_at=datetime(2024, 11, 10, 9, 8, 7, 654321, tzinfo=UTC),
        )
        output = encode_object(original)
        restored = decode_object(output)
        self.assertEqual(original, restored)

    def test_datetime_roundtrip(self):
        """Datetime objects survive round trips through protobuf."""
        data = (
            datetime(2022, 2, 2, 22, 22, 22, 493484, tzinfo=UTC),
            datetime(2020, 10, 31, 12, tzinfo=ZoneInfo("America/Los_Angeles")),
            datetime(2020, 10, 31, 12, tzinfo=ZoneInfo("Pacific/Kwajalein")),
        )
        for original in data:
            with self.subTest():
                output = encode_datetime(original)
                restored = decode_datetime(output)
                self.assertEqual(original, restored)
