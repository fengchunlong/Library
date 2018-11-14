from . import db
from datetime import datetime

# 会员数据模型
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)                         # 编号
    openid = db.Column(db.String(50),)                                   # 微信用户id
    nickname = db.Column(db.String(100))                                 # 微信昵称
    truename = db.Column(db.String(100))                                 # 用过真实姓名
    password = db.Column(db.String(100))                                 # 密码
    phone = db.Column(db.String(11), unique=True)                        # 手机号
    avatar = db.Column(db.String(200))                                   # 微信头像
    role_id = db.Column(db.Integer,default=0)                                      # 用户角色id 0:普通员工 1：管理员 2：组长
    status = db.Column(db.Boolean(), default=0)                          # 0:未审核；1：已通过；2：未通过:；3：已拉黑
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 注册时间
    borrow_info = db.relationship("BorrowInfo", backref='user')          # 外键关系关联
    def __repr__(self):
        return '<User %r>' % self.name



# 图书表
class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)                        # 编号
    isbn = db.Column(db.String(20))                                     # isbn号
    title = db.Column(db.String(100))                                   # 标题
    author = db.Column(db.String(100))                                  # 作者
    image_url = db.Column(db.String(200))                               # 头像url
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加景区时间
    cate_id = db.Column(db.Integer, db.ForeignKey('category.id'))        # 所属tag
    review = db.relationship("Review", backref='book')                  # 外键关系关联

    def __repr__(self):
        return "<Books %r>" % self.title

# 分类
class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)                        # 编号
    name = db.Column(db.String(255),unique=True)                        # 标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    book = db.relationship("Book", backref='category')                  # 外键关系关联


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)                        # 编号
    name = db.Column(db.String(100), unique=True)                       # 管理员账号
    pwd = db.Column(db.String(100))                                     # 管理员密码
    adminlogs = db.relationship("Adminlog", backref='admin')            # 管理员登录日志外键关系关联
    oplogs = db.relationship("Oplog", backref='admin')                  # 管理员操作日志外键关系关联

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        """
        检测密码是否正确
        :param pwd: 密码
        :return: 返回布尔值
        """
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)                         # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))          # 所属管理员
    ip = db.Column(db.String(100))                                       # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 登录时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id

# 操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)                        # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))         # 所属管理员
    ip = db.Column(db.String(100))                                      # 操作IP
    reason = db.Column(db.String(200))                                  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Oplog %r>" % self.id

# 图书借阅信息
class BorrowInfo(db.Model):
    __tablename__ = 'borrow_info'
    id = db.Column(db.Integer, primary_key=True)                        # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))           # 所属用户
    status = db.Column(db.Boolean(), default=0)                         # 借阅状态 0:未审核 1：已通过 2：未通过
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 借阅时间

# 图书评论
class Review(db.Model):
    __tablename__ = 'review'
    id      = db.Column(db.Integer, primary_key=True)                   # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))           # 所属用户
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))           # 所属图书
    score   = db.Column(db.Integer)                                     # 评分,取值范围：1-10
    content = db.Column(db.String(200))                                 # 评论内容
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 借阅时间

    def __repr__(self):
        return "<Review %r>" % self.id


# 申请购买
class ApplyBuy(db.Model):
    __tablename__ = 'apply_buy'
    id    = db.Column(db.Integer, primary_key=True)                     # 编号
    isbn  = db.Column(db.String(20))                                    # isbn号
    title = db.Column(db.String(100))                                   # 图书标题
    user_id   = db.Column(db.Integer, db.ForeignKey('user.id'))         # 所属用户
    leader_id = db.Column(db.Integer)                                   # 组长id
    reason  = db.Column(db.String(200))                                 # 申请理由
    status  = db.Column(db.Boolean(), default=0)                        # 申请状态 0:未审核 1：已通过 2：未通过
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 申请时间

    def __repr__(self):
        return "<ApplyBuy %r>" % self.id