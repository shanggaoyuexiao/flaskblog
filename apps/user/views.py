from flask import Blueprint, request, render_template, redirect, url_for, jsonify, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from apps.user.models import User
from exts import db

user_bp = Blueprint('user', __name__, url_prefix='/user')

# 拦截列表
required_login_list = [
    '/user/change',
    '/article/add_article',
    '/article/add_comment',
    '/article/detail']


# 自定义过滤器，用于把二进制解码
@user_bp.app_template_filter('cdecode')
def content_cdecode(content):
    content = content.decode('utf8')
    return content


# 这个钩子函数每次请求都会自动执行一次，重点。钩子函数是加到全局的
@user_bp.before_app_request
def before_request():
    if request.path in required_login_list:  # 获取用户请求路径，判断是不是在拦截列表里面
        id = session.get('uid')  # 如果拿不到用户uid，让用户返回登录页面
        if not id:
            return render_template('user/login.html')
        else:
            user = User.query.get(id)  # 拿到用户的id，根据id找到用户，然后返回回来
            g.user = user  # 然后把user用户对象放到g对象里面，这个g是本次请求的一个对象，存活周期为这一次请求


# 用户注册
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')  # request是从页面获取的，表单一点提交就会提交信息
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        phone = request.form.get('phone')
        if password == repassword:  # 如果密码一致
            # 1注册用户,与模型结合
            user = User()
            # 2给对象的属性赋值
            user.username = username  # .username表示访问user的属性，获取属性
            user.password = generate_password_hash(password)  # 使用自带的函数实现加密generate_password_hash
            user.phone = phone  # 属性赋值
            # 添加并提交
            # 3.将user对象添加到session中(类似缓存)
            db.session.add(user)
            # 4.提交到数据库
            db.session.commit()
            return render_template('base.html')

    return render_template('user/register.html')


# 验证手机号码唯一
@user_bp.route('/checkphone', methods=['GET', 'POST'])
def check_phone():
    # 传的key是phone，值是文本框输入的
    phone = request.args.get('phone')
    user = User.query.filter(User.phone == phone).all()
    # 我们这个功能是用ajax来实现的，所以返回要遵循一定的格式，必须是json的格式
    # cod :400 不能用   200可以用
    if len(user) > 0:
        return jsonify(code=400, msg='此号码已被注册')
    else:
        return jsonify(code=200, msg='此号码可用')


# 用户登录
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        f = request.args.get('f')
        if f == '1':  # 用户名和密码登录
            username = request.form.get('username')  # 获取用户名
            password = request.form.get('password')  # 获取密码
            users = User.query.filter(User.username == username).all()  # 在数据库里找到与用户密码一样的密码的列表
            for user in users:  # 第一个参数是数据库加密过后的密码，第二个表单输入的密码
                # 如果flag=True表示匹配，否则密码不匹配
                flag = check_password_hash(user.password, password)
                if flag:
                    # response=redirect(url_for('index'))
                    # #这句话的意思是把用户的id赋值给uid
                    # response.set_cookie('uid',str(user.id),max_age=1800)
                    # return response    #这里是返回给主页的
                    # session机制, 可以直接把session当成字典使用, 只要用session那就必须加一个东西到配置文件上去，可以把session看成加密后的cookie
                    session['uid'] = user.id  # 如果是True则，把用户的uid方到session中
                    return redirect(url_for('index'))
            else:
                return render_template('user/login.html', msg='用户名或者密码有误')
        elif f == '2':  # 手机号码和验证码登录
            pass

    return render_template('user/login.html')


# 发送短信息
@user_bp.route('/sendmsg')  # 发送短信暂不开同
def send_message():
    pass


# 用户退出
@user_bp.route('/logout')
def logout():
    # 把cookie删除就欧克了
    # response=redirect(url_for('index'))
    # #删除cookie，key就是要删除的cookie的key
    # response.delete_cookie('uid')
    # return response
    # 删除session , 可以把session看作加密后的cookie
    session.clear()
    return redirect(url_for('index'))


# 用户信息修改
@user_bp.route('/change', methods=['GET', 'POST'])
def change():
    if request.method == 'POST':
        username = request.form.get('username')
        # password=request.form.get('password')    #密码先不修改
        phone = request.form.get('phone')
        # 找到对象
        user = g.user
        # 进行修改
        user.username = username
        # user.password=password
        user.phone = phone
        # 提交数据库
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('user/change.html', user=g.user)
