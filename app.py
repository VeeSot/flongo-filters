import os

import flask_admin as admin
from flask import Flask, request, session

from flask_admin.contrib.mongoengine import ModelView
from flask_babelex import Babel
from flask_mongoengine import MongoEngine


from filters.filters import extract_filters
from models import Flat, District, Exterior, Street, Walls

app = Flask(__name__)
babel = Babel(app)
# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'
app.config['MONGODB_SETTINGS'] = {'DB': 'testing'}

os.environ['LANGUAGE'] = 'ru'
@babel.localeselector
def get_locale():
    override = request.args.get('lang')

    if override:
        session['lang'] = override

    return session.get('lang', 'en')


# Create models
db = MongoEngine()
db.init_app(app)





class FlatView(ModelView):
    column_filters = extract_filters(Flat)
    form_ajax_refs = {
        'exterior': {
            'fields': ('name',)
        }
    }


class DistrictView(ModelView):
    column_filters = extract_filters(District)
    pass


class StreetView(ModelView):
    column_filters = extract_filters(Street)


class ExteriorView(ModelView):
    column_filters = extract_filters(Exterior)


class WallsView(ModelView):
    column_filters = extract_filters(Walls)



@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


if __name__ == '__main__':
    # Create admin
    admin = admin.Admin(app, 'Flaty:Интерфейс')

    # Add views
    admin.add_view(FlatView(Flat, 'Квартиры'))
    admin.add_view(DistrictView(District, 'Районы'))
    admin.add_view(StreetView(Street, 'Улицы'))
    admin.add_view(ExteriorView(Exterior, 'Экстерьер'))
    admin.add_view(WallsView(Walls, 'Стены'))

    # Start app
    app.run(debug=True)
