#import dependencies
from itertools import groupby
from flask import Flask,jsonify

import numpy as np
import datetime as dt

# Python SQL Toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

######### Database Set up ###########
# engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=True)
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=True)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# # Save References to Each Table
Measurement = Base.classes.measurement
Station = Base.classes.station

# # Create Session (Link) From Python to the DB
session = Session(engine)

# # Create an app

app = Flask(__name__)

#Create routes

# Home page.
# List all routes that are available.
@app.route("/")
def Welcome():
    return (
        f"Welcome to the Hawaii climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start date<br/>"
        f"/api/v1.0/start date/end date<br/>"
    )



@app.route("/api/v1.0/precipitation")
def about():
    # Converts the Query Results to a Dictionary Using `date` as the Key and `prcp` as the Value
    # Calculates the Date 1 Year Ago from the Last Data Point in the Database
    # Returns the JSON representation of your dictionary
    date_calc = dt.date(2017,8,23)-dt.timedelta(days=365)
    prcp_date = session.query(Measurement.date,Measurement.prcp).\
                filter(Measurement.date >= date_calc).\
                group_by(Measurement.date).\
                order_by(Measurement.date.desc()).all()
    prcp_list = dict(prcp_date)
    return jsonify(prcp_list)

#Returns a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    sta = session.query(Station.station, Station.name).all()
    sta_list = []
    for x in range(len(sta)):
        sta_list.append((sta[x][0],sta[x][1]))
    return jsonify(sta_list)
    


#Query the dates and temperature 
#observations of the most active station for the last year of data.

#Return a JSON list of temperature observations 
#(TOBS) for the previous year.    

@app.route("/api/v1.0/tobs")
def Temperature():
    date_calc = dt.date(2017,8,23)-dt.timedelta(days=365)
    temp_obsv = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.date >= date_calc).\
        filter(Measurement.station == "USC00519281")
    temps = []
    for x in range(len(temp_obsv.all())):
        temps.append((temp_obsv.all()[x][0],temp_obsv.all()[x][1]))
    return jsonify(temps)

# Returns a JSON list of the minimum temperature, the average temperature, 
# and the max temperature for a given start
@app.route("/api/v1.0/<start>")
def start(start):
    temp_func = session.query(func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start)
    temp_list = []
    for x in range(len(temp_func.all())):
        temp_list.append((temp_func.all()[x][0],
        temp_func.all()[x][1],
        temp_func.all()[x][2]))

    return jsonify(temp_list)

# Returns a JSON list of the minimum temperature, the average temperature, 
# and the max temperature for a given start-end range.
@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    temp_func = session.query(func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date >= end)     
    temp_list = []
    for x in range(len(temp_func.all())):
        temp_list.append((temp_func.all()[x][0],
        temp_func.all()[x][1],
        temp_func.all()[x][2]))

    return jsonify(temp_list)

if __name__ == "__main__":
    app.run(debug=True)