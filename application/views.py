"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect, jsonify, session

from flask_cache import Cache
from grid import mcDetails, orDetails, studentDetails, analysisGrid
from application import app
from decorators import login_required, admin_required
from forms import TestForm, RegisterForm, LoginForm
from models import Test, Teacher
import logging
import json


# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)


def home():
    return redirect(url_for('list_tests'))


def say_hello(username):
    """Contrived example to demonstrate Flask's url routing capabilities"""
    return 'Hello %s' % username


@login_required
def list_tests():
    """List examples"""
    tests = Test.query(Test.added_by == session['email']).order(-Test.timestamp)
    form = TestForm()
    return render_template('list_tests.html', tests=tests, form=form)

@login_required
def test_details(test_id): 
    test = Test.get_by_id(test_id)
    if request.method == "POST":
        data = request.get_json(force=False, silent=False, cache=False)
        if data[0][0] == "Open Response":
            test.or_data = data
            test.put()
        elif data[0][0] == "Multiple Choice":
            test.mc_data = data
            test.put()
        else:
            test.student_data = data
            test.put()
    mc_data = json.dumps(test.mc_data)
    or_data = json.dumps(test.or_data)
    student_data = json.dumps(test.student_data)
    return render_template('test_details.html', test_id = test_id, test = test, mc_data = mc_data, or_data = or_data, student_data = student_data)

@login_required
def student_details(test_id):
    test = Test.get_by_id(test_id)
    if request.method == "POST":
        data = request.get_json(force=False, silent=False, cache=False) 
        test.student_data = data
        test.put()
    student_data = json.dumps(test.student_data)
    return render_template('student_details.html', test_id = test_id, test = test, student_data = student_data)

@login_required
def analysis(test_id):
    test = Test.get_by_id(test_id)
    analysis_data, fixedRows, num_mc, num_or, num_groups, num_periods = analysisGrid(test.num_mc, test.num_or, test.mc_data, test.or_data, test.mc_answers, test.student_data) #, test.or_points)
    analysis_data = json.dumps(analysis_data)
    return render_template('test_analysis.html', test_id = test_id, test = test, analysis_data = analysis_data, fixedRows = fixedRows, num_mc = num_mc, num_or = num_or, num_groups = num_groups, num_periods = num_periods)
    #return redirect(url_for('test_details', test_id = test_id ))

@login_required
def new_test():
    form = TestForm()
    if form.validate_on_submit():
        test = Test(
            test_name=form.test_name.data,
            num_mc=form.num_mc.data,
            mc_answers = int(form.mc_answers.data),
            num_or=form.num_or.data,
            #or_points = int(form.or_points.data),
            num_students=form.num_students.data,
            #test_data = defaultGrid(form.num_mc.data, int(form.mc_answers.data), form.num_or.data, form.or_points.data,form.num_students.data),
            mc_data = mcDetails(form.num_mc.data, int(form.mc_answers.data)),
            or_data = orDetails(form.num_mc.data,form.num_or.data),
            student_data = studentDetails(form.num_students.data),
            added_by=session['email']
        )
        try:
            test.put()
            test_id = test.key.id()
            test = Test.get_by_id(test_id)
            mc_data = json.dumps(test.mc_data)
            or_data = json.dumps(test.or_data)
            student_data = json.dumps(test.student_data)
            flash(u'Test %s successfully saved.' % test_id, 'success')
            return render_template('test_details.html', test = Test.get_by_id(test_id), test_id = test_id, mc_data = mc_data, or_data = or_data, student_data = student_data)
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_tests'))
    return redirect(url_for('list_tests'))

@login_required
def edit_test(test_id):
    test = Test.get_by_id(test_id)
    form = TestForm(obj=test)
    if request.method == "POST":
        if form.validate_on_submit():
            test.test_name = form.data.get('test_name')
            test.num_mc = form.data.get('num_mc')
            test.num_or = form.data.get('num_or')
            #test.num_students = json.dumps(form.data.get('num_students'))
            test.num_students = form.data.get('num_students')
            test.put()
            flash(u'Test %s successfully saved.' % test_id, 'success')
            return redirect(url_for('list_tests'))
    return render_template('edit_test.html', test=test, form=form)

@login_required
def update_test(test_id):
    test = Test.get_by_id(test_id)
    if request.method == "POST":
        data = request.get_json(force=False, silent=False, cache=False)
        test.test_data = data
        #test.test_data = request.get_json(force=False, silent=False, cache=False);
        test.put()
    new_data = json.dumps(test.test_data)
    return render_template('update_test.html', test=test, mc_data = new_data, bad_test = test.test_data)

@login_required
def delete_test(test_id):
    """Delete a test object"""
    test = Test.get_by_id(test_id)
    try:
        test.key.delete()
        flash(u'Test %s successfully deleted.' % test_id, 'success')
        return redirect(url_for('list_tests'))
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')
        return redirect(url_for('list_tests'))

def register():
    error = None
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        teacher = Teacher(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data,
        )
        try:
            teacher.put()
            teacher_id = teacher.key.id()
            flash(u'Teacher %s successfully saved.' % teacher_id, 'success')
            return redirect(url_for('login'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('register'))
    return render_template('register.html', form=form)

def logout():
    session.pop('logged_in', None)
    session.pop('name', None)
    session.pop('email', None)
    flash('You are logged out. Bye. :( ')
    return redirect(url_for('login'))

def login():
    error = None
    if request.method == 'POST':
        t = Teacher.query(Teacher.email == request.form['email'], 
            Teacher.password == request.form['password']).fetch(1)
        if len(t) == 0:
            flash('Email/PW combo not found')
        else:
            name = t[0].first_name
            email = t[0].email
            session['logged_in'] = True
            session['name'] = name
            session['email'] = email
            flash('You are logged in. Go Crazy.')
            return redirect(url_for('list_tests'))
    return render_template('login.html', form = LoginForm(), error = error)

@admin_required
def admin_only():
    """This view requires an admin account"""
    return 'Super-seekrit admin page.'


@cache.cached(timeout=60)
def cached_tests():
    """This view should be cached for 60 sec"""
    tests = Test.query()
    return render_template('list_tests_cached.html', tests=tests)


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''



