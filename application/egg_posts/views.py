import os
from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from application import db
from application.models import EggPost
from application.egg_posts.forms import EggPostForm
from flask import send_file
import pandas as pd
from datetime import date



egg_posts = Blueprint('egg_posts', __name__)

#Create
@egg_posts.route('/create', methods = ['GET','POST'])
@login_required
def create_post():
    form = EggPostForm()
    if form.validate_on_submit():
        egg_post = EggPost(eggs_amount = form.eggs_amount.data,
                            broken_eggs = form.broken_eggs.data,
                            current_food = form.current_food.data,
                            dead_chicken = form.dead_chicken.data,
                            user_id = current_user.id)

        posts = pd.read_csv('application/egg_posts/collecting.csv')
        eggs = {
            'index':[len(posts)+1],
            'date' :[date.today().strftime('%d-%m-%Y')],
            'eggs_amount':[form.eggs_amount.data],
            'broken_eggs':[form.broken_eggs.data],
            'current_food':[form.current_food.data],
            'dead_chicken':[form.dead_chicken.data],
                  }
        df = pd.DataFrame(eggs)
        df.to_csv('application/egg_posts/collecting.csv', index=False, mode='a', header=False)


        db.session.add(egg_post)
        db.session.commit()
        flash('Eggs Collected')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form = form)
#view
@egg_posts.route('/<int:egg_post_id>')
def egg_post(egg_post_id):
    # grab the requested blog post by id number or return 404
    egg_post = EggPost.query.get_or_404(egg_post_id)
    return render_template('egg_post.html',eggs_amount=egg_post.eggs_amount,
                            date=egg_post.date,broken_eggs=egg_post.broken_eggs,
                            current_food=egg_post.current_food,dead_chicken=egg_post.dead_chicken, post=egg_post)
#update
@egg_posts.route("/<int:egg_post_id>/update", methods=['GET', 'POST'])
@login_required
def update(egg_post_id):
    egg_post = EggPost.query.get_or_404(egg_post_id)
    if egg_post.collector != current_user:
        # Forbidden, No Access
        abort(403)

    form = EggPostForm()
    if form.validate_on_submit():
        egg_post.eggs_amount = form.eggs_amount.data
        egg_post.broken_eggs = form.broken_eggs.data
        egg_post.current_food = form.current_food.data
        egg_post.dead_chicken = form.dead_chicken.data
        db.session.commit()
        flash('Post Updated')

        df = pd.read_csv('application/egg_posts/collecting.csv', index_col='index')
        df.loc[egg_post.id, 'date'] = date.today().strftime('%d-%m-%Y')
        df.to_csv('application/egg_posts/collecting.csv')
        df.loc[egg_post.id, 'eggs_amount'] = form.eggs_amount.data
        df.to_csv('application/egg_posts/collecting.csv')
        df.loc[egg_post.id, 'broken_eggs'] = form.broken_eggs.data
        df.to_csv('application/egg_posts/collecting.csv')
        df.loc[egg_post.id, 'current_food'] = form.current_food.data
        df.to_csv('application/egg_posts/collecting.csv')
        df.loc[egg_post.id, 'dead_chicken'] = form.dead_chicken.data
        df.to_csv('application/egg_posts/collecting.csv')
        return redirect(url_for('egg_posts.egg_post', egg_post_id=egg_post.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.eggs_amount.data = egg_post.eggs_amount
        form.broken_eggs.data = egg_post.broken_eggs
        form.current_food.data = egg_post.current_food
        form.dead_chicken.data = egg_post.dead_chicken

    return render_template('create_post.html', title='Update',
                           form=form)

#delete
@egg_posts.route("/<int:egg_post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(egg_post_id):
    egg_post = EggPost.query.get_or_404(egg_post_id)
    if egg_post.collector != current_user:
        # Forbidden, No Access
        abort(403)
    db.session.delete(egg_post)
    db.session.commit()
    flash('Egg_Post deleted')
    df = pd.read_csv('application/egg_posts/collecting.csv')
    df = df.drop(egg_post.id-1)
    df.to_csv('application/egg_posts/collecting.csv', index=False,)

    return redirect(url_for('core.index'))

@egg_posts.route('/download', methods=['GET', 'POST'])
@login_required
def download():
    # converting csv to html
    filepath = 'egg_posts/collecting.csv'

    #filename = 'collecting.csv'
    return send_file(filepath ,as_attachment=True)
