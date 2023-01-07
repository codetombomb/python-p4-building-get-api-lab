#!/usr/bin/env python3
from sqlalchemy import desc
from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

def bakery_to_dict(bakery):
    b_dict = {
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at,
        "updated_at": bakery.updated_at
    }
    return b_dict

def baked_good_dict(bg):
    bg_dict = {
        "id": bg.id,
        "name": bg.name,
        "price": bg.price,
        "created_at": bg.created_at,
        "updated_at": bg.updated_at
    }
    return bg_dict

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    b_query = Bakery.query.all()
    bakeries = []
    for b in b_query:
        bakeries.append(bakery_to_dict(b))

    resp = make_response(jsonify(bakeries), 200)
    return resp

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    b_query = Bakery.query.filter_by(id=id).first()
    b_query = b_query.to_dict()
    resp = make_response(jsonify(b_query), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    bg_query = BakedGood.query.order_by(desc(BakedGood.price))
    baked_goods = []
    for bg in bg_query:
        baked_goods.append(baked_good_dict(bg))
    
    resp = make_response(jsonify(baked_goods), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    bg_query = BakedGood.query.order_by(desc(BakedGood.price)).first()
    print(bg_query)
    resp = make_response(jsonify(bg_query.to_dict()), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

if __name__ == '__main__':
    app.run(port=5555, debug=True)
