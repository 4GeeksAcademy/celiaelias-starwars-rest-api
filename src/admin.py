import os
from flask_admin import Admin
from models import db, User, planet, character, favourite_characters, favourite_planets
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(character, db.session))
    admin.add_view(ModelView(planet, db.session))
    admin.add_view(ModelView(favourite_characters, db.session))
    admin.add_view(ModelView(favourite_planets, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))