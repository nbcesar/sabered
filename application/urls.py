"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app
from application import views


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# Home page
app.add_url_rule('/', 'home', view_func=views.home)

# Say hello
app.add_url_rule('/hello/<username>', 'say_hello', view_func=views.say_hello)

# Examples list page
app.add_url_rule('/tests', 'list_tests', view_func=views.list_tests, methods=['GET', 'POST'])

# Register
app.add_url_rule('/register', 'register', view_func=views.register, methods=['GET', 'POST'])

# Login
app.add_url_rule('/login', 'login', view_func=views.login, methods=['GET', 'POST'])

# Logout
app.add_url_rule('/logout', 'logout', view_func=views.logout)

# Examples list page (cached)
app.add_url_rule('/tests/cached', 'cached_tests', view_func=views.cached_tests, methods=['GET'])

# Contrived admin-only view example
app.add_url_rule('/admin_only', 'admin_only', view_func=views.admin_only)

# Edit an example
app.add_url_rule('/tests/<int:test_id>/edit', 'edit_test', view_func=views.edit_test, methods=['GET', 'POST'])

# Update an example
app.add_url_rule('/tests/<int:test_id>/update', 'update_test', view_func=views.update_test, methods=['GET', 'POST'])

# Delete an example
app.add_url_rule('/tests/<int:test_id>/delete', view_func=views.delete_test, methods=['POST'])

# Test Details
app.add_url_rule('/tests/<int:test_id>/test_details', 'test_details', view_func=views.test_details, methods=['GET', 'POST'])

# New Test Dtails
app.add_url_rule('/tests/new_test', 'new_test', view_func=views.new_test, methods=['GET', 'POST'])

# Student Details
app.add_url_rule('/tests/<int:test_id>/student_details', 'student_details', view_func=views.student_details, methods=['GET', 'POST'])

# Test Analysis
app.add_url_rule('/tests/<int:test_id>/analysis', 'analysis', view_func=views.analysis, methods=['GET', 'POST'])

## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

