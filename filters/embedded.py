# Filters for embedded documents

import gettext

from filters.base import Filter
from filters.constants import contains_in, eq_str, eq_int, lt, gt

_ = gettext.gettext


class EmbeddedFilter(Filter):
    def filter(self, query, value):
        raise NotImplementedError('Please, to implement me!')

    def __init__(self, field, embedded_field, condition):
        name = getattr(field, 'verbose_name', field.name)
        super().__init__(f'{name}', name)
        self.condition = condition
        self.field = field
        self.embedded_field = embedded_field

    @classmethod
    def build(cls, field, embedded_field):
        _filters = []
        for f in cls.filters:
            _filter = cls(field, embedded_field, f)
            _filters.append(_filter)
        return _filters


class EmbeddedStringFilter(EmbeddedFilter):
    filters = [_(contains_in), _(eq_str)]

    def filter(self, query, value):
        params = {}
        _filter = None

        if self.condition == contains_in:
            _filter = {f'{self.embedded_field.db_field}__icontains': value}
        elif self.condition == eq_str:
            _filter = {f'{self.embedded_field.db_field}': value}

        if _filter:
            embedded_class = self.embedded_field.owner_document
            low_level_filter = embedded_class.objects(**_filter)
            key = f'{self.field.db_field}__in'
            params.update({key: low_level_filter})

        return query.filter(**params)


class EmbeddedIntegerFilter(EmbeddedFilter):
    filters = [_(gt), _(lt), _(eq_int)]

    def filter(self, query, value):
        params = {}
        _filter = None

        if self.condition == gt:
            _filter = {f'{self.embedded_field.db_field}__gt': value}
        elif self.condition == lt:
            _filter = {f'{self.embedded_field.db_field}__lt': value}
        elif self.condition == eq_int:
            _filter = {f'{self.embedded_field.db_field}': value}

        if _filter:
            embedded_class = self.embedded_field.owner_document
            low_level_filter = embedded_class.objects(**_filter)
            key = f'{self.field.db_field}__in'
            params.update({key: low_level_filter})

        return query.filter(**params)
