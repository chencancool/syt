from flask import Blueprint, render_template, request, jsonify
from syt.models import Product, Order, db
import json
from syt.sqb import client


checkout = Blueprint('checkout', __name__, url_prefix='/checkout')


@checkout.route('/')
def index():
    products = Product.query.all()
    return render_template('checkout/index.html', products=products)


@checkout.route('/convert', methods=['POST', 'GET'])
def convert():
    amount = request.form.get('amount')
    data = {}
    data['amount'] = amount
    data['success'] = 1
    return json.dumps(data)


@checkout.route('/product_get', methods=['POST', 'GET'])
def product_get():
    barcode = request.form.get('barcode')
    product = Product.query.filter_by(barcode=barcode).first()
    data = {}
    if product:
        data['barcode'] = product.barcode
        data['name'] = product.name
        data['price'] = product.price
        return json.dumps(data)
    return ''


@checkout.route('/cashier', methods=['POST', 'GET'])
def cashier():
    amount = request.form.get('amount')
    return render_template('checkout/cashier.html', amount=amount)


@checkout.route('/pay', methods=['POST', 'GET'])
def pay():
    dynamic_id = request.form.get('dynamic_id')
    amount = request.form.get('amount')
    subject = request.form.get('subject')
    ret = client.pay(amount, dynamic_id, subject=subject)
    if ret['result_code'] == '200' and ret['biz_response']['result_code'] == 'PAY_SUCCESS' and ret['biz_response']['data']['order_status'] == 'PAID':
        data = ret['biz_response']['data']
        sn = data['sn']
        client_sn = data['client_sn']
        order_status = data['order_status']
        payer_uid = data['payer_uid']
        subject = data['subject']
        # description = data['description']
        amount = data['total_amount']
        # payer = data['payer']
        # operator = data['operator']
        status = True
        order = Order(sn=sn, client_sn=client_sn, order_status=order_status, payer_uid=payer_uid, subject=subject, amount=amount, status=status)
        db.session.add(order)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        return json.dumps(ret)


@checkout.route('/gen_order', methods=['POST', 'GET'])
def gen_order():
    data = dict(request.form)['biz_response']
    return data
