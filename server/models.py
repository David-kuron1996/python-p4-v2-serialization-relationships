from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


class Animal(db.Model, SerializerMixin):
    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    species = db.Column(db.String)

    enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosures.id'))
    enclosure = db.relationship('Enclosure', back_populates='animals')

    # prevent circular serialization
    serialize_rules = ('-enclosure.animals',)


class Enclosure(db.Model, SerializerMixin):
    __tablename__ = 'enclosures'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    animals = db.relationship('Animal', back_populates='enclosure')
    zookeepers = db.relationship('Zookeeper', back_populates='enclosure')

    serialize_rules = (
        '-animals.enclosure',
        '-zookeepers.enclosure',
    )


class Zookeeper(db.Model, SerializerMixin):
    __tablename__ = 'zookeepers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosures.id'))
    enclosure = db.relationship('Enclosure', back_populates='zookeepers')

    serialize_rules = ('-enclosure.zookeepers',)
