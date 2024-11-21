#!/usr/bin/python3

"""Action module"""

from action import app_views_action

from flask import render_template, url_for, request, redirect
import os
from werkzeug.utils import secure_filename
from flask import current_app
from models.property import Property
from models.property_image import Property_image
from models.user import User



@app_views_action.route('/upload_property', methods=['POST'])
def upload_property():
    new_user = User(first_name="Amadou", last_name="Bah")
    new_user.save()
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)

    # Collecting basic property data
    new_property = Property()
    # Ensure new_user or current_user is defined
    new_property.user_id = new_user.id  # Replace with current_user.id if using Flask-Login
    new_property.title = request.form.get('title')
    new_property.description = request.form.get('description')
    new_property.property_type = request.form.get('propertyType')
    new_property.price = request.form.get('price')
    new_property.listing_type = request.form.get('listing_type')
    new_property.address = request.form.get('address')
    new_property.city = request.form.get('city')
    new_property.state = request.form.get('state')
    new_property.country = request.form.get('country')
    new_property.zip_code = request.form.get('zipCode')
    new_property.bedrooms = request.form.get('bedrooms')
    new_property.bathrooms = request.form.get('bathrooms')
    new_property.area = request.form.get('area')
    
    new_property.save()

    # Collect additional images and descriptions
    main_image = request.files.get('mainImage')
    additional_images = request.files.getlist('additionalImages')
    additional_descriptions = request.form.getlist('additionalDescriptions')

    # Save the main image
    if main_image:
        new_image = Property_image()

        image_extension = os.path.splitext(main_image.filename)[1]
        main_image_filename = secure_filename(f"{new_property.id}_Main_image{image_extension}")
        main_image_path = os.path.join(upload_folder, main_image_filename)
        main_image.save(main_image_path)

        new_image.image_type = "Main_image"
        new_image.image_url = main_image_path
        new_image.property_id = new_property.id
        new_image.save()

    # Ensure additional_images and additional_descriptions have matching lengths
    if len(additional_images) == len(additional_descriptions):
        # Save each additional image with its description
        for i in range(len(additional_images)):
            image = additional_images[i]
            if image and image.filename:  # Ensure the image is not empty
                #get the image extension
                image_extension = os.path.splitext(image.filename)[1]
                description_safe = secure_filename(additional_descriptions[i])
                image_filename = f"{new_property.id}_{description_safe}{image_extension}"
                image_path = os.path.join(upload_folder, image_filename)
                image.save(image_path)

                # Save the additional image data
                new_image = Property_image()
                new_image.image_type = additional_descriptions[i]
                new_image.image_url = image_path
                new_image.property_id = new_property.id
                new_image.save()
    else:
        # Handle mismatch between image and description counts if necessary
        print("Mismatch between additional images and descriptions.")


    
    # You can then store `property_data` in a database or process it further
    # Example response
    """return jsonify(property_data)"""
    return redirect(url_for('app_view_home.home'))



@app_views_action.route('/my_properties')
def my_properties():
    return render_template('my_properties.html')
