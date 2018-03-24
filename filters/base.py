import gettext

from flask_admin.contrib.mongoengine.filters import BaseMongoEngineFilter

from filters.constants import contains_in, eq_str, lt, gt, eq_int

_ = gettext.gettext


# Filters for primitives
class Filter(BaseMongoEngineFilter):
    filters = []

    def __init__(self, field, condition):
        name = getattr(field, 'verbose_name', field)
        super().__init__(f'{field}_{name}', name)
        self.condition = condition
        self.field = field

    def filter(self, query, value):
        raise NotImplementedError('Please, to implement me!')

    def apply(self, query, value):
        if not value:
            return query
        return self.filter(query, value)

    def operation(self):
        return self.condition

    @classmethod
    def build(cls, field):
        _filters = []
        for f in cls.filters:
            _filter = cls(field, f)
            _filters.append(_filter)
        return _filters


class IntegerFilter(Filter):
    filters = [_(gt), _(lt), _(eq_int)]

    def filter(self, query, value):
        params = {}
        if self.condition == eq_int:
            params = {f'{self.field.name}': value}
        elif self.condition == gt:
            params = {f'{self.field.name}__gt': value}
        elif self.condition == lt:
            params = {f'{self.field.name}__lt': value}
        return query.filter(**params)


class StringFilter(Filter):
    filters = [_(contains_in), _(eq_str)]

    def filter(self, query, value):
        params = {}
        if self.condition == contains_in:
            params = {f'{self.field.name}__icontains': value}
        elif self.condition == eq_str:
            params = {f'{self.field.name}': value}
        return query.filter(**params)
