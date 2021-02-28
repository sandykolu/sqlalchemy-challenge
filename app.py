#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Session link from Python to SQLLite DB
#################################################
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes for Hawaii Climate."""
    return (
        f"Hawaii Climate API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def prec():
    # Return prec data from last year
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    prec = session.query(Measurement.date, Measurement.prcp).        filter(Measurement.date >= prev_year).all()
    session.close()
    precipitat = {date: prcp for date, prcp in prec}
    return jsonify(precipitat)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).    session.close()
    results_months = session.query(Measurement.tobs).    filter(Measurement.station == 'USC00519281').    filter(Measurement.date>= prev_year).all()
    return jsonify(results_months)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all
    session.close()
    stations=list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/temp/start/end")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    
    results = session.query(*sel).        filter(Measurement.date >= start).        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)

