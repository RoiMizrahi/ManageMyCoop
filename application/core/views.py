from flask import render_template, request, Blueprint
from application.models import EggPost
core = Blueprint('core', __name__)

@core.route('/')
def info():
    return render_template('info.html')

@core.route('/collections')
def index():
    page = request.args.get('page', 1, type = int)
    egg_posts = EggPost.query.order_by(EggPost.date.desc()).paginate(page= page, per_page = 10)
    return render_template('index.html', egg_posts = egg_posts)
