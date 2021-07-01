import os
import time
import requests
from flask import Flask, request, jsonify, make_response, after_this_request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/database.db'
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['Access-Control-Allow-Origin'] = '*'
db = SQLAlchemy(app)


#ID, NUMBER, SIZE, COLOR
cart = []

def abort_if_not_exist(cart_id):
    if cart_id not in cart:
        abort(404, message="Could not find cart item...")

def abort_if_exist(cart_id):
    if cart_id in cart:
        abort(409, message="Cart item already exists...")

class ProductModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shortDesc = db.Column(db.String(100), nullable=False)
    longDesc = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    sizes = db.Column(db.String(100), nullable=False)
    colors = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Product(name={name}, shortDesc={shortDesc}, longDesc={longDesc}, price = {price}, sizes={sizes}, colors = {colors})"

class PrevPurchased(db.Model):
    dato = db.Column(db.String(100), primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    items = db.Column(db.String(100), nullable=False)


cart_put_args = reqparse.RequestParser()
cart_put_args.add_argument("product", type=str, help="Which product", required=True)
cart_put_args.add_argument("number", type=int, help="Number of products", required=True)
cart_put_args.add_argument("price", type=int, help="Price of products", required=True)
cart_put_args.add_argument("size", type=str, help="Size of products", required=True)
cart_put_args.add_argument("color", type=str, help="Color of products", required=True)

cart_update_args = reqparse.RequestParser()
cart_update_args.add_argument("product", type=str, help="Which product", required=True)
cart_update_args.add_argument("number", type=int, help="Name of the product")
cart_update_args.add_argument("price", type=int, help="Price of products")
cart_update_args.add_argument("size", type=str, help="Size of products")
cart_update_args.add_argument("color", type=str, help="Color of the products")

prod_put_args = reqparse.RequestParser()
prod_put_args.add_argument("name", type=str, help="Name of the product", required=True)
prod_put_args.add_argument("shortDesc", type=str, help="Short product description missing...", required=True)
prod_put_args.add_argument("longDesc", type=str, help="Long product description missing...", required=True)
prod_put_args.add_argument("price", type=int, help="Price of the products", required=True)
prod_put_args.add_argument("sizes", type=str, help="Sizes of the products", required=True)
prod_put_args.add_argument("colors", type=str, help="Colors of the products", required=True)

prod_update_args = reqparse.RequestParser()
prod_update_args.add_argument("name", type=str, help="Name of the product")
prod_update_args.add_argument("shortDesc", type=str, help="Short product description")
prod_update_args.add_argument("longDesc", type=str, help="Long product description")
prod_update_args.add_argument("price", type=int, help="Price of the products")
prod_update_args.add_argument("sizes", type=str, help="Sizes of the products")
prod_update_args.add_argument("colors", type=str, help="Colors of the products")

prod_delete_args = reqparse.RequestParser()

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'shortDesc': fields.String,
    'longDesc': fields.String,
    'price': fields.Integer,
    'sizes': fields.String,
    'colors': fields.String
}


class Products(Resource):
    @marshal_with(resource_fields)
    def get(self):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        result = ProductModel.query.all()
        if not result:
            abort(404, message="Could not find product with that id...")
        return result, 200

    def put(self):
        pass


class Product(Resource):
    @marshal_with(resource_fields)
    def get(self, prod_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        result = ProductModel.query.filter_by(id=prod_id).first()
        if not result:
            abort(404, message="Could not find product with that id...")
        return result

    @marshal_with(resource_fields)
    def put(self, prod_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        args = prod_put_args.parse_args()
        result = ProductModel.query.filter_by(id=prod_id).first()
        if result:
            abort(409, message="Product id taken...")

        product = ProductModel(id=prod_id, name=args['name'], shortDesc=args['shortDesc'], longDesc=args['longDesc'], price=args['price'], sizes=args['sizes'], colors=args['colors'])
        db.session.add(product)
        db.session.commit()
        return product, 201


    @marshal_with(resource_fields)
    def patch(self, prod_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = True
            response.headers['Access-Control-Allow-Methods'] = ["GET", "PUT", "PATCH"]
            response.headers['Access-Control-Allow-Headers'] = ["Origin", "Content-Type", "Accept"]
            return response

        args = prod_update_args.parse_args()
        result = ProductModel.query.filter_by(id=prod_id).first()
        if not result:
            abort(404, message="Could not find product with that id...")

        if args['name']:
            result.name = args['name']
        if args['shortDesc']:
            result.shortDesc = args['shortDesc']
        if args['longDesc']:
            result.longDesc = args['longDesc']
        if args['price']:
            result.price = args['price']
        if args['sizes']:
            result.sizes = args['sizes']
        if args['colors']:
            result.colors = args['colors']
        db.session.commit()

        return result

    @marshal_with(resource_fields)
    def delete(self, prod_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = True
            response.headers['Access-Control-Allow-Methods'] = ["GET", "PUT", "PATCH", "DELETE"]
            response.headers['Access-Control-Allow-Headers'] = ["Origin", "Content-Type", "Accept"]
            return response

        args = prod_delete_args.parse_args()
        result = ProductModel.query.filter_by(id=prod_id).first()
        if not result:
            abort(404, message="Product does not exist...")

        db.session.delete(result)
        db.session.commit()
        return "Deleted...", 400

num_items = len(cart)

class Carts(Resource):

    def get(self):
        return cart, 200

    def put(self):
        args = cart_put_args.parse_args()
        cart.append(args)
        return cart,201

class Cart(Resource):
    now = datetime.now()

    def get(self, cart_id):
        abort_if_not_exist(cart_id)
        return cart[cart_id], 200

    def put(self, cart_id):
        abort_if_exist(cart_id)
        args = cart_put_args.parse_args()
        cart.append(args)
        return cart[cart_id], 201

    def delete(self, cart_id):
        abort_if_not_exist(cart_id)
        args = prod_put_args.parse_args()
        del cart[cart_id]
        return "Deleted...", 204


    def calcPrice(self):
        price = 0
        for product in self.cart:
            price += product.price
        return price

    def purchase(self):
        items = "Items purchased: "
        price = self.calcPrice()
        dateofpurchase = self.now.strftime("%d/%m/%Y %H:%M:%S")

        for item in self.cart:
            items += item.name + ", "

        purchase = PrevPurchased(dato=dateofpurchase, price=price, items=items)

        db.session.add(purchase)
        db.session.commit()

        return 'Something...', 200

    def delete(self, cart_id):
        pass


api.add_resource(Cart, "/cart/<int:cart_id>")
api.add_resource(Carts, "/carts")
api.add_resource(Product, "/product/<int:prod_id>")
api.add_resource(Products, "/products")


if not os.path.exists("tmp/database.db"):
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)