# import needed modules
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,func
import datetime as dt
from flask import Flask,jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)


# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# Home page of climate app
@app.route("/")
def home():
    # show all the available URLs in home page
    return (
        f"Welcome to Climate App </br>"
        f"Available URLs are listed below </br>"
        f"/api/v1.0/precipitation </br>"
        f"/api/v1.0/stations </br>"
        f"/api/v1.0/tobs </br>"
        f"/api/v1.0/2016-01-13</br>"
        f"/api/v1.0/2016-01-13/2017-01-13 </br>"
        #f"<b>NOTE: Enter date in yyyy-mm-dd(2103-01-23) format </b>"
    )

# URL to view precipitations for all dates 
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Binding the session
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.prcp).all()
    session.close()
    prcp_data = []
    for rec in results:
        temp_prcp_data = {}
        temp_prcp_data[f"{rec['date']}"] = rec['prcp']
        prcp_data.append(temp_prcp_data)
    return jsonify(prcp_data)

# URL to view all the stations
@app.route("/api/v1.0/stations")
def stations():
    # Binding the session
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    all_stations = list(np.ravel(results))    
    return jsonify(all_stations)

# URL to view tempreture observation for the previous year for th emost active station
@app.route("/api/v1.0/tobs")
def tempreture():
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >='2016-01-01').filter(Measurement.date <'2017-01-01').order_by(Measurement.date).all()
    session.close()
    active_station_tobs = list(np.ravel(results))
    print(active_station_tobs)
    # Return a JSON list of temperature observations for the previous year.
    return jsonify(active_station_tobs)
 
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date.
@app.route('/api/v1.0/<start>')
def get_temp_summary(start):    
    # For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >=start).all()
    session.close()
    start_temp_summary = list(np.ravel(results))
    if start_temp_summary:
        return jsonify(start_temp_summary)
    else:
        return jsonify({"error": f"For {start} there is no record found"}), 404
    

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route('/api/v1.0/<start>/<end>')
def get_temp_summary_range(start,end):    
    # For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >=start).filter(Measurement.date <= end).all()
    session.close()
    sart_end_temp_summary = list(np.ravel(results))
    return jsonify(sart_end_temp_summary)


if __name__ == "__main__":
    app.run(debug=True)