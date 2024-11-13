#!/usr/bin/python3
"""DB Storage module"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.agent import Agent
from models.user import User
from models.property import Property
from models.transaction import Transaction
from models.whishlist import Whishlist
from models.review import Review
from models.property_image import Property_image
from models.message import Message


class DBStorage:
    """DBStorage
    Class to manage objects storage to DB
    """
    __engine = None
    __session = None

    def __init__(self):
        """Contructor method
        """
        env = os.getenv("env")

        self.__engine = create_engine(
                    'mysql+mysqldb://roofmarket_user:roofmarket_pwd@localhost/roofmarket_db')

        if env == "test":
            Base.metadata.drop_all(self.__engine)
    
    
    def property_objs(self, per_page, offset, property_type=None, listing_type=None):
        """ Returns the properties needed to be listed in one page"""
        if property_type:
            return self.__session.query(Property).filter(Property.property_type == property_type).limit(per_page).offset(offset)
        elif listing_type:
            return self.__session.query(Property).filter(Property.listing_type == listing_type).limit(per_page).offset(offset)
        return self.__session.query(Property).limit(per_page).offset(offset)



    def count(self, classe, property_type=None, listing_type=None):
        """Counts the number of rows or objects in a given table sometimes with property_type given for properties"""
        if property_type:
            return self.__session.query(classe).filter(classe.property_type == property_type).count()
        elif listing_type:
            return self.__session.query(classe).filter(classe.listing_type == listing_type).count()
        return self.__session.query(classe).count()


    def all(self, cls=None):
        """all to retrieve all records from DB

        Args:
            cls (string, optional): Object to return. Defaults to None.

        Returns:
            Dict: All records from a database
        """
        allclasses = {"User": User,
                      "State": Agent,
                      "City": Property,
                      "Amenity": Transaction,
                      "Place": Whishlist,
                      "Review": Review,
                      "Property_image": Property_image,
                      "Message": Message
                      }
        obj_result = {}
        cls = cls if not isinstance(cls, str) else allclasses.get(cls)
        if cls is None:
            for cls in allclasses:
                objs = self.__session.query(cls).all()
                for o in objs:
                    obj_result["{}.{}".format(o.name, o.id)] = o
        else:
            objs = self.__session.query(cls).all()
            for o in objs:
                obj_result["{}.{}".format(o.__table__, o.id)] = o
        return obj_result

    def new(self, obj):
        """new : to add an an obj to a session

        Args:
            obj (instance): Obj created to be added
        """
        self.__session.add(obj)

    def save(self):
        """save: method to commit changes to the db
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Method to delete an obj from the db

        Args:
            obj (string): name of the obj. Defaults to None.
        """
        if obj:
            self.__session.delete(obj)


    def get_image(self, property_id, image_type=None):
        """Returns a list of images based on the property id"""
        if not image_type:
            return self.__session.query(Property_image).filter(Property_image.property_id == property_id).all()
        
        return self.__session.query(Property_image).filter(Property_image.property_id == property_id,  Property_image.image_type == image_type).first()
    
 
    """ def get_countries_with_cities(self):
        #Returns a dictionary of countries with their respective cities from the Property table.
        results = self.__session.query(Property.country, Property.city).distinct().all()
    
        # Organize results into a dictionary {country: [city1, city2, ...]}
        countries_with_cities = {}
        for country, city in results:
            if country not in countries_with_cities:
                countries_with_cities[country] = set()  # Use a set to avoid duplicate cities
            countries_with_cities[country].add(city)
        
        # Convert each set of cities to a list for easier JSON serialization if needed
        return {country: list(cities) for country, cities in countries_with_cities.items()}"""

    def get_countries(self):
        # Fetch distinct countries
        countries = self.__session.query(Property.country).distinct().all()
        countries_list = [country[0] for country in countries]
        return countries_list
    

    def get_cities(self, country):
        # Fetch distinct cities for the given country from the database
        return self.__session.query(Property.city).filter(Property.country == country).distinct().all()


    def get_property_by_id(self, property_id):
        """Returns the property of a specific id"""
        return self.__session.query(Property).filter(Property.id == property_id).first()
    

    def reload(self):
        """create all tables in the database
        """
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(factory)()

    def close(self):
        """close session
        """
        self.__session.close()
