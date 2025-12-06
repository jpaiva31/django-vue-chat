from django.core.exceptions import ImproperlyConfigured


class ReadWriteSerializerMixin:
    """Selects serializer based on HTTP method.

    GET uses the read serializer; POST uses the write serializer.
    Set `read_serializer_class` and `write_serializer_class` on the viewset.
    """

    read_serializer_class = None
    write_serializer_class = None

    def get_serializer_class(self):
        """Return the class to use for the serializer."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return self.get_write_serializer_class()
        return self.get_read_serializer_class()

    def get_read_serializer_class(self):
        """Return the class to use for the read serializer."""
        if self.read_serializer_class is None:
            raise ImproperlyConfigured(
                f"'{self.__class__.__name__}' must define `read_serializer_class` "
                f"or override `get_read_serializer_class()`."
            )
        return self.read_serializer_class

    def get_write_serializer_class(self):
        """Return the class to use for the write serializer."""
        if self.write_serializer_class is None:
            raise ImproperlyConfigured(
                f"'{self.__class__.__name__}' must define `write_serializer_class` "
                f"or override `get_write_serializer_class()`."
            )
        return self.write_serializer_class