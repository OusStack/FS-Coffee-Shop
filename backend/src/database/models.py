"""Module for database models."""

import json
import os

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer, String


database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(
    os.path.join(project_dir, database_filename))

db = SQLAlchemy()


def setup_db(app):
    """
    Bind a flask application and a SQLAlchemy service.

    :param app:
    :return:
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    """
    Drop the database tables and starts fresh.

    It can be used to initialize a clean database.
    !!NOTE you can change the database_filename variable
    to have multiple verisons of a database
    :return:
    """
    db.drop_all()
    db.create_all()


class Drink(db.Model):
    """A persistent drink entity, extends the base SQLAlchemy Model."""

    # Auto incrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is
    # [{'color': string, 'name':string, 'parts':number}]
    recipe = Column(String(180), nullable=False)

    def short(self):
        """
        Short form representation of the Drink model.

        :return:
        """
        print(json.loads(self.recipe))
        short_recipe = [
            {'color': r['color'], 'parts': r['parts']}
            for r in json.loads(self.recipe)
        ]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    def long(self):
        """
        Long form representation of the Drink model.

        :return:
        """
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    def insert(self):
        """
        Insert a new model into a database the model.

        It must have a unique name the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
        :return:
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete a model into a database the model must exist in the database.

        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
        :return:
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """
        Update a model into a database the model must exist in the database.

        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
        :return:
        """
        db.session.commit()

    def __repr__(self):
        """
        Representation of the class.

        :return:
        """
        return json.dumps(self.short())
