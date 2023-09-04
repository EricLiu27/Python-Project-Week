from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user_model import User
from flask_app.models.forum_model import Forum
from pprint import pprint
import os




# displays the forums 


@app.route('/forums')
def forum_display():
    if 'user_id' not in session: 
        return redirect ('/')

    data = {
        'id' : session ['user_id']
    }
    logged_user = User.get_by_id(data)
    all_forums = Forum.get_all()
    return render_template('forums_display.html', logged_user=logged_user, all_forums=all_forums)




@app.route('/forums/create', methods = ['POST'])
def create_forum():
    if 'user_id' not in session:
        return redirect ('/')
    if not Forum.is_valid(request.form):
        return redirect('/forums/new')
    forum_data = {
        **request.form,
        'user_id' : session ['user_id']
    }
    Forum.create(forum_data)
    return redirect ('/users/dashboard')


@app.route('/api/forums/create', methods = ['POST'])
def api_create_forum():
    if 'user_id' not in session:
        return redirect ('/')
    errors= Forum.api_is_valid(request.form)
    if len(errors)>=1:
        return {'message': 'validations fail', 'errors': errors}
    forum_data = {
        **request.form,
        'user_id' : session ['user_id']
    }
    logged_user = User.get_by_id({'id':session['user_id']})
    id = Forum.create(forum_data)
    res = {
        **forum_data,
        'id':id,
        'user_name': f'{logged_user.first_name} {logged_user.last_name}'
    }
    return res

@app.route('/forums/<int:id>/view')
def view_one_forum(id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id' : id
    }

    data2 = {
        'id' : session ['user_id']
    }
    one_forum = Forum.get_one(data)
    logged_user = User.get_by_id(data2)
    return render_template('forums_one.html', one_forum = one_forum, logged_user=logged_user)

@app.route('/forums/<int:id>/edit')
def edit_forum_form(id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id' : id
    }
    logged_user = User.get_by_id(data)
    one_forum = Forum.get_one(data)
    if one_forum.user_id != session ['user_id']:
        flash('This is not your forum! Unable to edit.')
        return redirect('/forums')
    return render_template('forums_edit.html', one_forum=one_forum, logged_user=logged_user)



@app.route('/forums/<int:id>/update', methods=['POST'])
def update_forum(id):
    if 'user_id' not in session:
        return redirect ('/')
    if not Forum.is_valid(request.form):
        return redirect(f'/forums/{id}/edit')
    data = {
        **request.form,
        'id' : id
    }
    one_forum = Forum.get_one(data)
    if one_forum.user_id != session ['user_id']:
        flash('This is not your forum! Unable to edit.')
        return redirect('/forums')
    Forum.update(data)
    return redirect ('/forums')

@app.route('/forums/<int:id>/delete')
def delete_forum(id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id' : id
    }
    this_forum = Forum.get_one(data)
    if this_forum.user_id != session ['user_id']:
        flash('This is not your forum! Unable to delete.')
        return redirect('/forums')
    Forum.delete(data)
    return redirect('/forums')


@app.route('/api/forums')
def get_all_forums_api():
    return Forum.api_get_all()

