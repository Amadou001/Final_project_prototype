#!/usr/bin/python3
"""Home module"""

from home import app_views_home
from flask import render_template, jsonify
from models import storage
from models.property import Property
from models.property_image import Property_image





@app_views_home.route("/")
def home():

    property_objs = storage.all(Property)
    property_list = []
    list_length = len(property_objs)
    num_to_list = 0
    if list_length >= 50:
        num_to_list = 50
    else:
        num_to_list = list_length

    i = 0
    for obj in property_objs.values():
        if i == num_to_list:
            break
        Main_image_obj = storage.get_image(obj.id, "Main_image")

        property_list.append({"id": obj.id, "title": obj.title, "property_type": obj.property_type, "price": obj.price, "listing_type": obj.listing_type,
                              "address": obj.address, "city": obj.city, "country": obj.country, "bedrooms": obj.bedrooms, 
                              "bathrooms": obj.bathrooms, "area": obj.area, "Main_image_url": Main_image_obj.image_url})
        i += 1

    Number_per_type ={"apartment": storage.count(Property, "apartment"), "villa": storage.count(Property, "villa"), 
                      "studio": storage.count(Property, "studio"), "house":storage.count(Property, "house") }

    return render_template("index.html", properties=property_list, Number_per_type=Number_per_type)
