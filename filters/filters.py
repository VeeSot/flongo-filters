from mongoengine import ReferenceField, StringField, IntField, ListField

from filters.base import IntegerFilter, StringFilter
from filters.embedded import EmbeddedStringFilter


def extract_filters(model):
    column_filters = []
    fields = model._fields.values()
    for field in fields:
        filters = []
        reference = None

        if isinstance(field, IntField):
            filters = IntegerFilter.build(field)

        elif isinstance(field, StringField):
            filters = StringFilter.build(field)

        elif isinstance(field, ReferenceField):
            reference = field.document_type

        elif isinstance(field, ListField):
            reference = field.field.document_type

        if reference:
            # Try to divide on components
            embedded_fields: [] = reference._fields.values()
            for embedded_field in embedded_fields:
                if isinstance(embedded_field, StringField):
                    filters.extend(EmbeddedStringFilter.build(field, embedded_field))
                elif isinstance(embedded_field, IntField):
                    filters.extend(EmbeddedStringFilter.build(field, embedded_field))

        if filters:
            column_filters.extend(filters)

    return column_filters
