from mongoengine.fields import StringField, Document, ReferenceField, ListField, IntField


class District(Document):
    name = StringField(max_length=255, verbose_name='Район')

    def __str__(self):
        return self.name


class Street(Document):
    name = StringField(max_length=255)

    def __str__(self):
        return self.name


class Walls(Document):
    name = StringField(max_length=255)

    def __str__(self):
        return self.name


class TypeHouse(Document):
    name = StringField(max_length=255)

    def __str__(self):
        return self.name


class Exterior(Document):
    name = StringField(max_length=255)

    def __str__(self):
        return self.name


class Flat(Document):
    district = ReferenceField(District, required=True, verbose_name='Район')
    street = ReferenceField(Street, required=True, verbose_name='Улица')
    house_number = StringField(required=True, verbose_name='№ дома')
    walls = ReferenceField(Walls, required=True, verbose_name='Материал стен')
    exterior = ListField(ReferenceField('Exterior'), verbose_name='Экстерьер')

    total_area = IntField(required=False, verbose_name='Общая площадь, кв.м')
    kitchen_area = IntField(required=False, verbose_name='Кухня, кв.м')
    live_area = IntField(required=False, verbose_name='Жилая полщадь, кв.м')
    year = IntField(required=False, verbose_name='Год постройки')
    rooms = IntField(required=True, verbose_name='Количество комнат')
    cost = IntField(required=True, verbose_name='Цена')
