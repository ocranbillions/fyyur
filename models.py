from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.ext.hybrid import hybrid_property
# import datetime

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# insert into venues (name, city, state, address, phone, image_link, facebook_link) values ('The new venue', 'Lekki', 'LG', '14 church street Lekki', '08092400904', 'https://via.placeholder.com/150', 'https://www.facebook.com/ocranbillions');
# insert into artists (name, city, state, phone, genres, image_link, facebook_link) values ('Smith & The Gang', 'Lekki', 'LG', '08172080572', 'ROCK, METAL, PUNK', 'https://via.placeholder.com/150', 'https://www.facebook.com/ocranbillions');


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __repr__(self):
      return f'<Artist Id: {self.id} Name: {self.name} City: {self.city} State: {self.state} phone: {self.phone} genres: {self.genres} image_link: {self.image_link} fb_link: {self.facebook_link}>'

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.