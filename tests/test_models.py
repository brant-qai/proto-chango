import logging
from unittest import TestCase

from proto_chango.models import Node, Object

LOG = logging.getLogger(__name__)


class TestModels(TestCase):
    def test_create_empty_node(self):
        """Can create an empty node instance."""
        try:
            Node()
        except Exception as ex:
            raise AssertionError("Unexpected error creating empty node instance.") from ex

    def test_create_recursive_node(self):
        """Can create nested Node instances."""
        try:
            Node(nodes=[Node(), Node(), Node(nodes=[Node()])])
        except Exception as ex:
            raise AssertionError("Unexpected error creating recursive node instances.") from ex

    def test_create_simple_object(self):
        """Can create simple object instances."""
        try:
            Object(node=Node(), name="test")
        except Exception as ex:
            raise AssertionError("Unexpected error creating simple object instance.") from ex
