#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models import db, Venue, Artist, City, Show
import sys

from utils import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate =  Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  cities = City.query.filter().order_by(City.city_name)

  for city in cities:
    if len(city.venues) > 0:
      data.append({
        "city": city.city_name,
        "state": city.state,
        "venues": city.venues
      })

  return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
  text = request.form.get('search_term', '')
  result = Venue.query.filter(Venue.name.ilike(f'%{text}%'))

  response={
    "count": result.count(),
    "data": result
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  shows = venue.shows
  past_shows = []
  upcoming_shows = []

  for show in shows:
    if show.start_time > datetime.now():
      upcoming_shows.append({
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
      })
    else:
      past_shows.append({
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
      })

  data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city.city_name,
    "state": venue.city.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  venue = {}
  venue['name'] = request.form['name']
  venue['city'] = request.form['city']
  venue['state'] = request.form['state']
  venue['address'] = request.form['address']
  venue['phone'] = request.form['phone']
  venue['genres'] = request.form.getlist('genres')
  venue['facebook_link'] = request.form['facebook_link']
  venue['image_link'] = request.form['image_link']
  
  if validate_new_venue(venue) == False:
    flash('Please fill all input')
    return render_template('forms/new_venue.html', form=VenueForm())
  else:
    error = False
    city = {}
    try:
      venue['city'] = venue['city'].capitalize()
      city_name = venue['city']
      city = City.query.filter_by(city_name=city_name).first()

      if city is None:
        city = City(
            state=venue['state'],
            city_name=venue['city']
          )
        db.session.add(city)
        db.session.flush() # flush() changes to the database and thus have your primary-key field (city_id) updated to use as foreign key in .add_venue

      city.add_venue(venue)
      db.session.commit()

      flash('Venue ' + venue['name'] + ' was successfully listed!')
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Venue could not be listed. Please check that your inputs are valid')
    finally:
      db.session.close()
      if error:
        return render_template('forms/new_venue.html', form=VenueForm())
      else:
        return redirect(url_for('venues'))

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info)
  finally:
    db.session.close()
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = []
  artists = Artist.query.all()

  for artist in artists:
    data.append(artist)
  
  return render_template('pages/artists.html', artists=data)



@app.route('/artists/search', methods=['POST'])
def search_artists():
  text = request.form.get('search_term', '')
  result = Artist.query.filter(Artist.name.ilike(f'%{text}%'))

  response={
    "count": result.count(),
    "data": result
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  shows = artist.shows
  past_shows = []
  upcoming_shows = []
  
  for show in shows:
    if show.start_time > datetime.now():
      upcoming_shows.append({
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
      })
    else:
      past_shows.append({
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
      })

  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  a = Artist.query.get(artist_id)

  form = ArtistForm()
  artist={
    "id": a.id,
    "name": a.name,
    "genres": a.genres,
    "city": a.city,
    "state": a.state,
    "phone": a.phone,
    "website": a.website,
    "facebook_link": a.facebook_link,
    "seeking_venue": a.seeking_venue,
    "seeking_description": a.seeking_description,
    "image_link": a.image_link
  }
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = {}
  artist['name'] = request.form['name']
  artist['city'] = request.form['city']
  artist['state'] = request.form['state']
  artist['phone'] = request.form['phone']
  artist['genres'] = request.form.getlist('genres')
  artist['facebook_link'] = request.form['facebook_link']
  artist['image_link'] = request.form['image_link']

  
  if validate_new_artist(artist) == False:
    flash('Please fill all input')
    return render_template('forms/new_artist.html', form=ArtistForm())
  else:
    error = False
    try:
      artist_to_update = Artist.query.get(artist_id)

      artist_to_update.name = artist['name']
      artist_to_update.city = artist['city']
      artist_to_update.state = artist['state']
      artist_to_update.phone = artist['phone']
      artist_to_update.genres = artist['genres']
      artist_to_update.facebook_link = artist['facebook_link']
      artist_to_update.image_link = artist['image_link']

      db.session.commit()
      flash('Artist ' + artist['name'] + ' was successfully updated!')
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Artist could not be updated. Please check that your inputs are valid')
    finally:
      db.session.close()
      if error:
        return render_template('forms/new_artist.html', form=ArtistForm())
      else:
        return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  v = Venue.query.get(venue_id)
  form = VenueForm()
  venue={
    "id": v.id,
    "name": v.name,
    "genres": v.genres,
    "address": v.address,
    "phone": v.phone,
    "website": v.website,
    "facebook_link": v.facebook_link,
    "seeking_talent": v.seeking_talent,
    "seeking_description": v.seeking_description,
    "image_link": v.image_link
  }
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  
  venue = {}
  venue['name'] = request.form['name']
  venue['address'] = request.form['address']
  venue['phone'] = request.form['phone']
  venue['genres'] = request.form.getlist('genres')
  venue['facebook_link'] = request.form['facebook_link']
  venue['image_link'] = request.form['image_link']

  if validate_edit_venue(venue) == False:
    flash('Please fill all input')
    return render_template('forms/new_venue.html', form=VenueForm())
  else:
    error = False
    try:
      venue_to_update = Venue.query.get(venue_id)

      venue_to_update.name = venue['name']
      venue_to_update.name = venue['address']
      venue_to_update.phone = venue['phone']
      venue_to_update.genres = venue['genres']
      venue_to_update.facebook_link = venue['facebook_link']
      venue_to_update.image_link = venue['image_link']

      db.session.commit()
      flash('Venue ' + venue['name'] + ' was successfully updated!')
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Venue could not be updated. Please check that your inputs are valid')
    finally:
      db.session.close()
      if error:
        return render_template('forms/new_venue.html', form=VenueForm())
      else:
        return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  artist = {}
  artist['name'] = request.form['name']
  artist['city'] = request.form['city']
  artist['state'] = request.form['state']
  artist['phone'] = request.form['phone']
  artist['genres'] = request.form.getlist('genres')
  artist['facebook_link'] = request.form['facebook_link']
  artist['image_link'] = request.form['image_link']
  
  if validate_new_artist(artist) == False:
    flash('Please fill all input')
    return render_template('forms/new_artist.html', form=ArtistForm())
  else:
    error = False
    try:
      new_artist = Artist(
        name=artist['name'],
        city=artist['city'],
        state=artist['state'],
        phone=artist['phone'],
        genres=artist['genres'],
        facebook_link=artist['facebook_link'],
        image_link=artist['image_link']
      )
      db.session.add(new_artist)
      db.session.commit()
      flash('Artist ' + artist['name'] + ' was successfully listed!')
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Artist could not be listed. Please check that your inputs are valid')
    finally:
      db.session.close()
      if error:
        return render_template('forms/new_artist.html', form=ArtistForm())
      else:
        return redirect(url_for('artists'))

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data = []
  shows = Show.query.order_by(Show.start_time).filter(Show.start_time >= datetime.now())

  for show in shows:
    show.print_info()
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  artist_id = request.form['artist_id']
  venue_id = request.form['venue_id']
  start_time = request.form['start_time']

  error = False
  if artist_id == "" or venue_id == "" or start_time == "":
    flash('Please fill all input boxes')
    return render_template('forms/new_show.html', form=ShowForm())
  else:
    try:
      show = Show(
        artist_id=artist_id,
        venue_id=venue_id,
        start_time=start_time
      )
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Please check that the IDs are valid')
    finally:
      db.session.close()
      if error:
        return render_template('forms/new_show.html', form=ShowForm())
      else:
        return redirect(url_for('shows'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
