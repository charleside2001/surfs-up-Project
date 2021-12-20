# import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Set Up the Database
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect the database into our classes
Base = automap_base()
# reflect the database
Base.prepare(engine, reflect=True)
# create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station
# create a session link from Python to our database
session = Session(engine)
# Set Up Flask
app = Flask(__name__)

# create welcome route 
@app.route("/") # Now our root, or welcome route, is set up

# create a function welcome() with a return statement
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''') #  add the precipitation, stations, tobs, and temp routes that we'll need for this module into our return statement
    
# next route we'll build is for the precipitation analysis.
@app.route("/api/v1.0/precipitation")

# create the precipitation() function, add the line of code that calculates the date one year ago from the most recent date in the database and write a query to get the date and precipitation for the previous year, and use Jsonify() to convert to a dictionary
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


# next route we'll build is for the station analysis
@app.route("/api/v1.0/stations")

# create a query that will allow us to get all of the stations in our database, start by unraveling our results into a one-dimensional array. To do this, we want to use the function np.ravel(), with results as our parameter  and convert to a list
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Monthly Temperature Route
@app.route("/api/v1.0/tobs")

# create a function called temp_monthly(), calculate the date one year ago from the last date in the database, query the primary station for all the temperature observations from the previous year and unravel the results into a one-dimensional array and convert that array into a list.  and jsonify our temps list, and then return it
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# 9.5.6 Create Statistics Route
# provide both a starting and ending date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# create a function called stats() to put our code in
def stats(start=None, end=None): # add parameters to our stats()function: a start parameter and an end parameter.
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)] # create a query to select the minimum, average, and maximum temperatures from our SQLite database
    # add an if-not statement to our code
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    # calculate the temperature minimum, average, and maximum with the start and end dates
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()     
    temps = list(np.ravel(results))
    return jsonify(temps)