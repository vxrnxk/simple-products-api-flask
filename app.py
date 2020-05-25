import json
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.views import MethodView


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
 
from my_app.catalog.views import catalog
app.register_blueprint(catalog)
 
db.create_all()

 
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float(asdecimal=True))
 
    def __init__(self, name, price):
        self.name = name
        self.price = price
 
    def __repr__(self):
        return '<Product %d>' % self.id

 
class ProductView(MethodView):
 
    def get(self, id=None, page=1):
        if not id:
            products = Product.query.paginate(page, 10).items
            res = {}
            for product in products:
                res[product.id] = {
                    'name': product.name,
                    'price': str(product.price),
                }
        else:
            product = Product.query.filter_by(id=id).first()
            if not product:
                abort(404)
            res = {
                'name': product.name,
                'price': str(product.price),
            }
        return jsonify(res)
 
    def post(self):
        name = request.form.get('name')
        price = request.form.get('price')
        product = Product(name, price)
        db.session.add(product)
        db.session.commit()
        return jsonify({product.id: {
            'name': product.name,
            'price': str(product.price),
        }})
 
    def put(self, id):
        return
 
    def delete(self, id):
        return
 
 
product_view =  ProductView.as_view('product_view')
app.add_url_rule(
    '/product/', view_func=product_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/product/<int:id>', view_func=product_view, methods=['GET']
)

catalog = Blueprint('catalog', __name__)
 
@catalog.route('/')
@catalog.route('/home')
def home():
    return "Welcome to the Catalog Home."