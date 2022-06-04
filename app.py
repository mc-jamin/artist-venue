#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from config import SQLALCHEMY_DATABASE_URI
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config.from_object('config')
db = SQLAlchemy(app)
moment = Moment(app)
migrate = Migrate(app, db)


# TODO: connect to a local postgresql database


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue_Artist(db.Model):
  __tablename__= 'venue_artist'
  venue_id=db.Column ('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True)
  artist_id=db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True)
  start_time = db.Column(db.String(120))
  venue_link=db.relationship('Venue', backref='venue_association')
  artist_link = db.relationship('Artist', backref='artist_assocaition')


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    #venue_link = db.relationship('Artist', secondary=artist_identifier)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    #venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  return render_template('pages/venues.html', areas= Venue.query.all());

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term', '')
  
  return render_template('pages/search_venues.html', results=Venue.query.filter(Venue.name.contains(search_term)), search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  return render_template('pages/show_venue.html', venues=Venue.query.filter_by(id=venue_id), shows = Venue_Artist.query.filter_by(venue_id=venue_id))



#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  try:
    name = form.name.data
    city = form.city.data
    state = form.state.data
    address = form.address.data
    phone = form.phone.data
    image_link = form.image_link.data
    facebook_link = form.facebook_link.data
    genres = form.genres.data
    website_link = form.website_link.data
    seeking_talent = form.seeking_talent.data
    seeking_description = form.seeking_description.data
    form_data = Venue(name= name,city = city,state = state,address = address,phone= phone,image_link= image_link,facebook_link= facebook_link, genres=genres, website_link=website_link, seeking_talent=seeking_talent, seeking_description=seeking_description )

    db.session.add(form_data)
    db.session.commit()

    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    #on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  
  return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  error=True
  try:    
    Venue.query.filter_by(id=venue_id).delete()    
    db.session.commit()   
    error=False 
  except:
    flash('ERROR!')
    error=True
  finally:
    db.session.close()
  
  return redirect(url_for('index'))



  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    
  return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term=request.form.get('search_term', '')
  
  artist_query = Artist.query.filter(Artist.name.contains(search_term)) 
  
  return render_template('pages/search_artists.html', results=artist_query, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  return render_template('pages/show_artist.html', artists= Artist.query.filter_by(id=artist_id), shows = Venue_Artist.query.filter_by(artist_id=artist_id))



#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm(request.form)  
  #populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artists=Artist.query.filter_by(id=artist_id))

@app.route('/artists/<artist_id>/edit/', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm(request.form)  
  edit_artist = Artist.query.filter_by(id=artist_id).first()

  try:
    edit_artist.name = form.name.data
    edit_artist.city = form.city.data
    edit_artist.state = form.state.data
    edit_artist.phone = form.phone.data
    edit_artist.genres = form.genres.data
    edit_artist.image_link = form.image_link.data
    edit_artist.facebook_link = form.facebook_link.data
    edit_artist.website_link = form.website_link.data
    edit_artist.seeking_venue = form.seeking_venue.data
    edit_artist.seeking_description = form.seeking_description.data    

    #edit_artist= db.session.merge(edit_artist)
    #db.session.flush()
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  except:
    #on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
  finally:
    db.session.close()

  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return render_template('pages/show_artist.html', artists=Artist.query.filter_by(id=artist_id))

@app.route('/venues/<venue_id>/edit')
def edit_venue(venue_id):
  form = VenueForm(request.form)
  #populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venues=Venue.query.filter_by(id=venue_id))


@app.route('/venues/<venue_id>/edit/', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm(request.form)  
  edit_venue = Venue.query.filter_by(id=venue_id).first()

  try:
    edit_venue.name = form.name.data
    edit_venue.city = form.city.data
    edit_venue.state = form.state.data
    edit_venue.address = form.address.data
    edit_venue.phone = form.phone.data
    edit_venue.image_link = form.image_link.data
    edit_venue.facebook_link = form.facebook_link.data
    edit_venue.genres = form.genres.data
    edit_venue.website_link = form.website_link.data
    edit_venue.seeking_talent = form.seeking_talent.data
    edit_venue.seeking_description = form.seeking_description.data

    #edit_artist= db.session.merge(edit_artist)
    #db.session.flush()
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  except:
    #on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
  finally:
    db.session.close()

  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return render_template('pages/show_venue.html', venues=Venue.query.filter_by(id=venue_id))




#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  
  try:
    name = form.name.data
    city = form.city.data
    state = form.state.data
    phone = form.phone.data
    genres = form.genres.data
    image_link = form.image_link.data
    facebook_link = form.facebook_link.data
    website_link = form.website_link.data
    seeking_venue = form.seeking_venue.data
    seeking_description = form.seeking_description.data

    artist_data = Artist(name= name,city = city,state = state,phone= phone,genres=genres,image_link= image_link,facebook_link= facebook_link, website_link=website_link, seeking_venue=seeking_venue, seeking_description=seeking_description )

    db.session.add(artist_data)
    db.session.commit()

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')


  except:
    #on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')

  finally:
    db.session.close()

  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():

  # displays list of shows at /shows
  #replace with real venues data.
  
  return render_template('pages/shows.html', shows=Venue_Artist.query.all())

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)
  try:    
    venue_id= form.venue_id.data
    artist_id = form.artist_id.data
    start_time = form.start_time.data

    venue_artist=Venue_Artist(venue_id=venue_id, artist_id=artist_id, start_time=start_time)

    db.session.add(venue_artist)

    #statement = artist_identifier.insert().values(venue_id=venue_id, artist_id=artist_id, start_time=start_time)
    #db.session.execute(statement)
    db.session.commit()

    # on successful db insert, flash success
    flash('Show was successfully listed!')

  except:
    #TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Make sure you have entered the correct IDs')

  finally:
    db.session.close()

  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead 
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

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
    app.run(host='127.0.0.1', port=3000, debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
