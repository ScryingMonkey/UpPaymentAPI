from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps


# Create a engine for connecting to SQLite3.  Assumes salaries.db is in your app root folder
e = create_engine('sqlite:///salaries.db')
# instantiate app object
app = Flask(__name__)
# instantiate api object
api = Api(app)

# Example Method
class Example_Method(Resource):
    # define get response
    def get(self):
        returnString = 'return string for example get method'
        return returnString
    # define post response
    def post(self):
        returnString = 'return string for example post method'
        return returnString
# add method routing to api object
api.add_resource(Example_Method, '/example_method')

# Example Method
class Example_Method_With_Input_Variable(Resource):
    # define get response
    def get(self, variable_name):
        returnString = 'return string for example get method with variable: %s' % variable_name
        return returnString
    # define post response
    def post(self, variable_name):
        returnString = 'return string for example post method with variable: %s' % variable_name
        return returnString
# add method routing to api object 
api.add_resource(Example_Method_With_Input_Variable, 
            '/example_method_with_input_variable/<string:variable_name>')

            

# Example DB Query Method
class Departments_Meta(Resource):
    def get(self):
        #Connect to database
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("select distinct DEPARTMENT from salaries")
        return {'departments': [i[0] for i in query.cursor.fetchall()]}
# add method routing to api object 
api.add_resource(Departments_Meta, '/departments')


# Example DB Query Method with selector
class Departmental_Salary(Resource):
    def get(self, department_name):
        conn = e.connect()
        query = conn.execute("select * from salaries where Department='%s'"%department_name.upper())
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result
        #We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient
# add method routing to api object 
api.add_resource(Departmental_Salary, '/dept/<string:department_name>')


# Boiler plate.  Must me last.
if __name__ == '__main__':
     app.run()


