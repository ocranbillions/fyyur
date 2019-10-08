from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.ext.hybrid import hybrid_property
# import datetime

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
# (DONE)
#----------------------------------------------------------------------------#

class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(120))
    state = db.Column(db.String(120))
    venues = db.relationship('Venue', backref=db.backref('city', lazy=True), collection_class=list) #lazy=joined

    def __repr__(self):
      return f'<City Id: {self.id} city_name: {self.city_name} state: {self.state}>'


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    name = db.Column(db.String)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref=db.backref('venue', lazy=True), collection_class=list) 

    def __repr__(self):
      return f'<Venue Id: {self.id} city_id: {self.city_id} name: {self.name} address: {self.address} phone: {self.phone} image_link: {self.image_link} facebook_link: {self.facebook_link}>'


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref=db.backref('artist', lazy=True), collection_class=list) 

    def __repr__(self):
      return f'<Artist Id: {self.id} Name: {self.name} City: {self.city} State: {self.state} phone: {self.phone} genres: {self.genres} image_link: {self.image_link} facebook_link: {self.facebook_link}>'


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    start_time = db.Column(db.DateTime())

    def __repr__(self):
      return f'<Show Id: {self.id} artist_id: {self.artist_id} venue_id: {self.venue_id} start_time: {self.start_time}>'
