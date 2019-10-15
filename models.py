from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    city_name = db.Column(db.String(120))
    state = db.Column(db.String(120))
    venues = db.relationship('Venue', backref=db.backref('city', lazy=True), collection_class=list) #lazy=joined

    def add_venue(self, venue):
      v = Venue(
          name=venue['name'],
          address=venue['address'],
          phone=venue['phone'],
          genres=venue['genres'],
          facebook_link=venue['facebook_link'],
          image_link=venue['image_link'],
          city_id=self.id
        )

      db.session.add(v)

    def print_info(self):
      print(f"Id: {self.id}")
      print(f"City_name: {self.city_name}")
      print(f"State: {self.state}")
    

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
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

    def print_info(self):
      print(f"Id: {self.id}")
      print(f"city_id: {self.city_id}")
      print(f"name: {self.name}")
      print(f"address: {self.address}")
      print(f"phone: {self.phone}")
      print(f"genres: {self.genres}")
      print(f"image_link: {self.image_link}")
      print(f"website: {self.website}")
      print(f"facebook_link: {self.facebook_link}")
      print(f"seeking_talent: {self.seeking_talent}")
      print(f"seeking_description: {self.seeking_description}")

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
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

    def print_info(self):
      print(f"Id: {self.id}")
      print(f"name: {self.name}")
      print(f"city: {self.city}")
      print(f"state: {self.state}")
      print(f"phone: {self.phone}")
      print(f"genres: {self.genres}")
      print(f"image_link: {self.image_link}")
      print(f"website: {self.website}")
      print(f"facebook_link: {self.facebook_link}")
      print(f"seeking_venue: {self.seeking_venue}")
      print(f"seeking_description: {self.seeking_description}")


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    start_time = db.Column(db.DateTime())

    def print_info(self):
      print(f"Id: {self.id}")
      print(f"artist_id: {self.artist_id}")
      print(f"venue_id: {self.venue_id}")
      print(f"start_time: {self.start_time}")
