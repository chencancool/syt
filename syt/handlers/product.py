from flask import Blueprint, render_template
from syt.models import Product


product = Blueprint('product', __name__, url_prefix='/product')


@product.route('/')
def index():
    return  render_template('product/index.html')


@product.route('/<int:product_id>')
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product/product_detail.html', product=product)
