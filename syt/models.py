from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for


db = SQLAlchemy()


class Base(db.Model):
    """ 所有 model 的一个基类，默认添加了时间戳
    """
    # 表示不要把这个类当作 Model 类
    __abstract__ = True
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间


# 商品
class Product(Base):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)  # 序号
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)  # 商品名称
    price = db.Column(db.Float, nullable=False)  # 商品价格
    img_url = db.Column(db.String(256))  # 商品图片
    barcode = db.Column(db.String(32))  # 商品条形码
    is_disable = db.Column(db.Boolean, default=False)  # 商品状态，是否禁售

    @property
    def url(self):
        return url_for('product.detail', product_id=self.id)


# 订单
class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)  # 序号
    sn = db.Column(db.String(32))
    client_sn = db.Column(db.String(32))
    order_status = db.Column(db.String(32))
    payer_uid = db.Column(db.String(32))
    subject = db.Column(db.String(32))
    description = db.Column(db.String(256))
    amount = db.Column(db.Float, nullable=False)  # 总价
    product_id = db.Column(db.String(256))  # 商品序号
    payer = db.Column(db.String(32))  # 付款人
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    
# 用户
class User(Base, UserMixin):
    __tablename__ = 'user'
    
    ROLE_USER = 10  # 游客
    ROLE_STAFF = 20  # 员工
    ROLE_ADMIN = 30  # 管理员
    
    id = db.Column(db.Integer, primary_key=True)  # 序号
    username = db.Column(db.String(128), unique=True, index=True, nullable=False)  # 用户名
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)  # 用户邮箱
    phone = db.Column(db.String(12))  # 手机号码
    _password = db.Column('password', db.String(256), nullable=False)  # 用户密码
    role = db.Column(db.SmallInteger, default=ROLE_STAFF)  # 用户角色

    def __repr__(self):
        return '<User:{}>'.format(self.username)
        
    @property
    def password(self):
        """ Python 风格的 getter """
        return self._password
        
    @password.setter
    def password(self, orig_password):
        """ Python 风格的 setter，这样设置 user.password 就会自动
        为 password 生成哈希值存入 _password 字段
        """
        self._password = generate_password_hash(orig_password)
        
    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_staff(self):
        return self.role == self.ROLE_STAFF

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN
