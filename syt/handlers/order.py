from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from syt.models import Order, db
from syt.sqb import client

order = Blueprint('order', __name__, url_prefix='/order')


@order.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Order.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('order/index.html', active='admin', pagination=pagination)


@order.route('/refund/<string:sn>/')
def refund(sn):
    ret = client.refund(sn=sn)
    if ret['result_code'] == '200' and ret['biz_response']['result_code'] == 'REFUND_SUCCESS' and ret['biz_response']['data']['order_status'] == 'REFUNDED':
        order = Order.query.filter_by(sn=sn).first()
        order.order_status = 'REDUNDED'
        order.status = False
        db.session.add(order)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        flash('退款成功', 'success')
        return redirect(url_for('.index'))
