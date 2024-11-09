#!/usr/bin/python3
"""Property module"""

from property  import app_views_property
from flask import render_template, abort, request, jsonify
from models import storage
from models.property import Property
from models.property_image import Property_image


@app_views_property.route("/property/<property_id>", methods = ["GET"])
def property_onclick(property_id):
    the_property = storage.get_property_by_id(property_id)
    if not the_property:
        abort(404, description="Bad request: Property not found")

    the_property_images = storage.get_image(property_id)
    property_dict = {}
    for image in the_property_images:
        property_dict[image.image_type] = image.image_url
    print(property_dict)
    property_dict["title"] = the_property.title
    property_dict["description"] = the_property.description
    property_dict["price"] = the_property.price
    property_dict["listing_type"] = the_property.listing_type

    return render_template("property.html", property=property_dict)



@app_views_property.route("/property_list")
def property_list():

    per_page = 3  # Number of properties per page
    property_type = request.args.get('type', None)
    if property_type not in ["apartment", "studio", "house", "villa"]:
        property_type = None

    # Get the total number of properties
    total_properties = storage.count(Property, property_type)  # Assuming `count()` is defined in your storage model
    if per_page > total_properties:
        per_page = total_properties
    print(total_properties)
    total_pages = (total_properties + per_page - 1) // per_page  # Total pages required


    return render_template('property_listing.html', total_pages=total_pages, property_type=property_type, per_page=per_page)
  

@app_views_property.route("/page_generation")
def page_generation():
    per_page = int(request.args['per_page'])  # Number of properties per page
    page = int(request.args.get('page', 1))  # Get current page from query parameters
    offset = (page - 1) * per_page
    property_type = request.args.get('property_type', None)

    if property_type not in ["apartment", "studio", "house", "villa"] or property_type == 'None':
        property_type = None

    # Query properties with limit and offset
    property_objs = storage.property_objs(per_page, offset, property_type)

    property_list = []
    for obj in property_objs:
        # Retrieve property images and select the main image URL
        main_image_obj = storage.get_image(obj.id, "Main_image")
    
        
        # Append property details to the list
        property_list.append({
            "id": obj.id,
            "title": obj.title,
            "property_type": obj.property_type,
            "price": obj.price,
            "listing_type": obj.listing_type,
            "address": obj.address,
            "city": obj.city,
            "country": obj.country,
            "bedrooms": obj.bedrooms,
            "bathrooms": obj.bathrooms,
            "area": obj.area,
            "Main_image_url": main_image_obj.image_url
        })

    #return render_template("index.html", properties=property_list, page=page, total_pages=total_pages)
    #return property_list
    #return render_template('property_listing.html', properties=property_list)
    return jsonify({
        "properties": property_list
        }) 
