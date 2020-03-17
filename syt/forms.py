from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import Length, Email, EqualTo, DataRequired, URL
from syt.models import db, User, Product
from wtforms import ValidationError


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email(message='请输入合法的email地址')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交')
    
    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user
        
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')
            
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')
    
    
class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')
    
    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')
            
    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')


class ProductForm(FlaskForm):
    name = StringField('商品名称', validators=[DataRequired(), Length(1, 128)])
    price = StringField('商品价格', validators=[DataRequired()])
    barcode = StringField('商品条码', validators=[DataRequired()])
    img_url = StringField('商品图片')
    submit = SubmitField('提交')

    def validate_barcode(self, field):
        if Product.query.get(self.name.data):
            raise ValidationError('商品条码已存在')

    def create_product(self):
        product = Product()
        self.populate_obj(product)
        db.session.add(product)
        db.session.commit()
        return product

    def update_product(self, product):
        self.populate_obj(product)
        db.session.add(product)
        db.session.commit()
        return product


class UserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 32)])
    email = StringField('用户邮箱', validators=[DataRequired(), Email(message='请输入合法的email地址')])
    password = PasswordField('密码', validators=[DataRequired()])
    repeat_password = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.get(self.email.data):
            raise ValidationError('邮箱已存在')

    def create_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user
