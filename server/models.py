from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    restaurantpizzas = db.relationship("RestaurantPizza",back_populates = "restaurant")

    # add serialization rules
    def to_dict (self):
        return {"id":self.id, 
                "name":self.name,
                "adress":self.address,
                "restaurantpizzas":[rp.to_dict() for rp in self.restaurantpizzas]
                }
        



    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    restaurantpizzas = db.relationship("RestaurantPizza", back_populates = "pizzas")

    # add relationship

    # add serialization rules

    def to_dict (self):
        return {"id":self.id, 
                "name":self.name,
                "ingredients":self.ingredients,
                "restaurantpizza":[rp.to_dict() for rp in self.restaurantpizzas]
                }
        

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    restaurant = db.relationship("Restaurant", back_populates = "restaurantpizzas")
     
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))
    pizzas = db.relationship("Pizza", back_populates = "restaurantpizza")
    # add serialization rules
    def to_dict (self):
        return {"id":self.id, 
                "price":self.price,
                "restaurant":self.restaurant.to_dict(),
                "pizzas":self.pizzas.to_dict()}
        

    # add validation

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
