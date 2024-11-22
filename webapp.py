from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__)


@app.route("/")
def render_main():
    with open('ufo_sightings.json') as ufo_data:
        Years = json.load(ufo_data)
    return render_template('index.html')

@app.route("/p2")
def render_page2():
    shapes = get_shape_options()
    if 'Shape' in request.args:
        Shape = request.args['Shape']
        encounterLength = Shapelongest_encounter(Shape)
       # MostCommonShape = GetMostCommonShape(Shape)
      #  MostCommonLoc = GetMostCommonLoc(Shape)
        fact = "The longest encounter with a " + (Shape) + " was " + str(encounterLength) + " seconds."
       # fact2 = "The most common type of UFO was a " + str(MostCommonShape) + "."
      #  fact3 = "The loaction with the most UFO sightings in " + str(Year) + " was " + MostCommonLoc + "." 
        return render_template('page2.html', Type_options=shapes, FunFact=fact)
    #shape = most_common_shape(Year)
    #fact2 = "In " + Year + ", the most common type of ufo was " + shape + "."
    return render_template('page2.html', Type_options=shapes)
    
def Shapelongest_encounter(Shape):   
    with open('ufo_sightings.json') as enounter_data:
        Times = json.load(enounter_data)
    times = []
    for t in Times:
       # print(t["Dates"]["Sighted"]["Year"])
        if t["Data"]["Shape"] == (Shape):
            print("test")
       # if t["Dates"]["Sighted"]["Year"] == Year:
       #     print("tets")
            times.append(t["Data"]["Encounter duration"])
    longest = max(times)
    print(longest)
    return longest
    
def get_shape_options():
    with open('ufo_sightings.json') as ufo_data:
        Shapes = json.load(ufo_data)
    shapes=[]
    for s in Shapes:
        if s["Data"]["Shape"] not in shapes:
            shapes.append(str(s["Data"]["Shape"]))
    print(shapes)
    shapes = list(dict.fromkeys(shapes))
    print(shapes)
    #years = sorted(years)
    shapeOptions=""
    for y in shapes:
        shapeOptions += Markup("<option value=\"" + y + "\">" + y + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return shapeOptions
    
@app.route("/p3")
def render_page3():
    EncLength = GetEncLength()
    return render_template('page3.html', data=EncLength)
    
def GetEncLength():
    with open('ufo_sightings.json') as Ufo_data:
        UfoData = json.load(Ufo_data)
    Years = []
    for u in UfoData:
        if u["Dates"]["Sighted"]["Year"] not in Years:
            Years.append(u["Dates"]["Sighted"]["Year"])
    Years = sorted(Years)
    Encounterdata = "["
    data = {}
    for e in UfoData:
        if e["Data"]["Encounter duration"] < 20000000: #removing outliers 
           data[e["Dates"]["Sighted"]["Year"]] = e["Data"]["Encounter duration"]
    maxdata =  {}
    for y in Years:
        durations = []
        for Key,x in data.items():
            if Key == y:
                durations.append(x)
        MaxDur = max(durations)
        maxdata[y] = MaxDur
    
    
    #Encounterdata = Encounterdata + Markup("{x:" + str(e["Dates"]["Sighted"]["Year"]) + ",y:" + str(e["Data"]["Encounter duration"]) + "},")
   # Encounterdata = Encounterdata[:-1]+"]"
    ReturnData = ""
    for Key,Value in maxdata.items():
        ReturnData = ReturnData + Markup("{x:" + str(Key) + ",y:" + str(Value) + "},")
    return ReturnData
    
@app.route('/p1')
def render_fact():
    years = get_year_options()
    if 'Year' in request.args:
        Year = request.args['Year']
        encounterLength = longest_encounter(Year)
        MostCommonShape = GetMostCommonShape(Year)
        MostCommonLoc = GetMostCommonLoc(Year)
        fact = "In " + str(Year) + ", the longest ufo encounter lasted " + str(encounterLength) + " seconds."
        fact2 = "The most common type of UFO was a " + str(MostCommonShape) + "."
        fact3 = "The loaction with the most UFO sightings in " + str(Year) + " was " + MostCommonLoc + "." 
        return render_template('page1.html', Year_options=years, FunFact=fact, FunFact2=fact2, FunFact3=fact3)
    #shape = most_common_shape(Year)
    #fact2 = "In " + Year + ", the most common type of ufo was " + shape + "."
    return render_template('page1.html', Year_options=years)
    
def get_year_options():
    with open('ufo_sightings.json') as ufo_data:
        Years = json.load(ufo_data)
    years=[]
    for c in Years:
        years.append(str(c["Dates"]["Sighted"]["Year"]))
    years = list(dict.fromkeys(years))
    years = sorted(years)
    options=""
    for y in years:
        options += Markup("<option value=\"" + y + "\">" + y + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
def longest_encounter(Year):
    with open('ufo_sightings.json') as enounter_data:
        Times = json.load(enounter_data)
    times = []
    for t in Times:
       # print(t["Dates"]["Sighted"]["Year"])
        if t["Dates"]["Sighted"]["Year"] == int(Year):
            print("test")
       # if t["Dates"]["Sighted"]["Year"] == Year:
       #     print("tets")
            times.append(t["Data"]["Encounter duration"])
    longest = max(times)
    print(longest)
    return longest

def GetMostCommonShape(Year):
    with open('ufo_sightings.json') as Shape_data:
        Shapes = json.load(Shape_data)
    shapes = []
    for s in Shapes:
        if s["Dates"]["Sighted"]["Year"] == int(Year):
            shapes.append(s["Data"]["Shape"])
    #print(shapes)
    #print(max(set(shapes), key=shapes.count))
    MostCommon = (max(set(shapes), key=shapes.count))
    return MostCommon
    
def GetMostCommonLoc(Year):
    with open('ufo_sightings.json') as Loc_data:
        Cities = json.load(Loc_data)
    cities = []
    for c in Cities:
        if c["Dates"]["Sighted"]["Year"] == int(Year):
            cities.append(c["Location"]["City"])
            print("test5")
    MostCommonCity = (max(set(cities), key=cities.count))
    states = []
    for s in Cities:
        if s["Dates"]["Sighted"]["Year"] == int(Year):
            states.append(s["Location"]["State"])
    MostCommonState = (max(set(states), key=states.count))
    return MostCommonCity + " " + MostCommonState
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
