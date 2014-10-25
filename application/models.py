"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb


class Test(ndb.Model):
    """Test Models"""
    test_name = ndb.StringProperty(required=True)
    num_mc = ndb.IntegerProperty(required=True)
    mc_answers = ndb.IntegerProperty(required=True)
    num_or = ndb.IntegerProperty(required=True)
    #or_points = ndb.IntegerProperty(required=True)
    num_students = ndb.IntegerProperty(required=True)
    correct_answers = ndb.IntegerProperty(repeated=True,indexed=False)
    pt_values = ndb.IntegerProperty(repeated=True,indexed=False)
    mc_data = ndb.JsonProperty()
    or_data = ndb.JsonProperty()
    student_data = ndb.JsonProperty()
    analysis_data = ndb.JsonProperty()
    added_by = ndb.StringProperty()
    #double check how to use this reference property
    #teacher = ndb.ReferenceProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)


class Teacher(ndb.Model):
    """Teacher Models"""
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
