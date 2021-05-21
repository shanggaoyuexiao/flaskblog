from flask import Blueprint, render_template, session, request, g, redirect, url_for
from apps.articles.models import Article_tepy, Article, Comment
from apps.user.models import User
from exts import db

article_bp = Blueprint('article', __name__, url_prefix='/article')


# 添加文章
@article_bp.route('/add_article', methods=['GET', 'POST'])
def add_article():
    types = Article_tepy.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        type_id = request.form.get('type')
        content = request.form.get('content')
        # 加入数据库
        article = Article()
        article.title = title
        article.type_id = type_id
        article.content = content
        article.user_id = g.user.id
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('article/add_article.html', user=g.user, types=types)  # 拿到用户对象，然后渲染到页面base


# 文章详情
@article_bp.route('/detail', methods=['GET', 'POST'])
def detail():
    article_id = request.args.get('aid')  # 拿到主键，这个主键是在base页面上获取的
    articles = Article.query.get(article_id)  # 找到用户对象
    types = Article_tepy.query.all()  # 拿到文章分类
    user_id = session.get('uid', None)
    user = User.query.get(user_id)
    return render_template('article/detail.html', articles=articles, types=types, user=user)


# 发表文章评论
@article_bp.route('/add_comment', methods=['POST', 'GET'])
def add_comment():
    if request.method == 'POST':
        comment_content = request.form.get('comment')
        user_id = g.user.id
        article_id = request.form.get('aid')
        to_id = request.form.get('to_id')
        # 评论模型
        comment = Comment()
        comment.comment = comment_content  # 给评论内容赋值
        comment.user_id = user_id
        comment.article_id = article_id
        comment.to_id = user_id
        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('article.detail') + "?aid=" + article_id)
    return redirect(url_for('index'))
