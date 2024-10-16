from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__)


@app.route("/")
def render_main():
    return render_template('index.html')

@app.route("/p2")
def render_page2():
    return render_template('page2.html')
    
@app.route("/p3")
def render_page3():
    return render_template('page3.html')
    
@app.route('/p1')
def render_fact():
    years = get_year_options()
    #Year = request.args.get('Year')
    #encounterLength = longest_encounter(Year)
    #shape = most_common_shape(Year)
    #fact = "In " + Year + ", the longest ufo encounter lasted" + encounterLength + " seconds."
   # fact2 = "In " + Year + ", the most common type of ufo was " + shape + "."
    return render_template('page1.html', Year_options=years)
    
def get_year_options():
    with open('ufo_sightings.json') as ufo_data:
        Years = json.load(ufo_data)
    years=[]
    for c in Years:
        if c["Dates"]["Sighted"]["Year"] not in years:
            years.append(str(c["Dates"]["Sighted"]["Year"]))
    options=""
    for y in years:
        options += Markup("<option value=\"" + y + "\">" + y + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
"""    
def longest_encounter(state):
    with open('ufo_sightings.json') as demographics_data:
        counties = json.load(demographics_data)
    highest=0
    county = ""
    for c in counties:
        if c["State"] == state:
            if c["Age"]["Percent Under 18 Years"] > highest:
                highest = c["Age"]["Percent Under 18 Years"]
                county = c["County"]
    return county
"""
if __name__=="__main__":
    app.run(debug=True)


def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url


if __name__ == '__main__':
    app.run(debug=False) # change to False when running in production
