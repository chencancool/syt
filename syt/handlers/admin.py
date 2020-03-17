from flask import Blueprint, render_template, redirect, url_for, flash
from syt.decorators import admin_required
from flask import request, current_app
from syt.models import Product, User, db
from syt.forms import ProductForm, UserForm


admin = Blueprint('admin', __name__, url_prefix='/admin')


# 管理员首页
@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html', active='admin')


# 商品管理首页
@admin.route('/products')
@admin_required
def products():
    page = request.args.get('page', default=1, type=int)
    pagination = Product.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/products.html', pagination=pagination)


# 用户管理首页
@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/users.html', pagination=pagination)


# 创建商品
@admin.route('/products/create', methods=['GET', 'POST'])
@admin_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        form.create_product()
        flash('商品添加成功', 'success')
        return redirect(url_for('admin.products'))
    return render_template('admin/create_product.html', form=form)


# 编辑商品
@admin.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        form.update_product(product)
        flash('商品更新成功', 'success')
        return redirect(url_for('admin.products'))
    return render_template('admin/edit_product.html', form=form, product=product)


# 删除商品
@admin.route('/products/<int:product_id>/delete')
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('商品删除成功', 'success')
    return redirect(url_for('admin.products'))


# 创建用户
@admin.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        form.create_user()
        flash('用户添加成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_user.html', form=form)


# 编辑用户
@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.update_user(user)
        flash('用户编辑成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html', form=form, user=user)


# 删除用户
@admin.route('/users/<int:user_id>/delete')
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('用户删除成功', 'success')
    return redirect(url_for('admin.users'))
