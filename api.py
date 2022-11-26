
from flask import Flask, jsonify, request,  make_response
from flask_restful import Resource, Api
import joblib
  

# load in our model
#loaded_model = joblib.load(filename)

# creating the flask app
app = Flask(__name__)

# creating an API object
api = Api(app)


  

class Prediction(Resource):

    def get(self):
        
        '''
        
        returns the structure of the request needed for our
        post request
        
        '''

        # tell how to make reuqests to our API on get

        return make_response(jsonify({
                                      'experience_level': ['SE','MI','EN','EX'],
                                      'employment_type' : ['FT','PT','CT','FL'],
                                      'company_size': ['S', 'M', 'L'],
                                      'role' : ['**Job Title**'],
                                      'residence' : ['2 Syl Country Code (US, GB) etc'],
                                      'remote%' : ['0','50','100']
                                      }), 201)
  
    def post(self):

        '''

        retrieves payload
        sends back model prediction


        '''
        
        data = request.get_json()

        if 'experience_level' not in data \
            or 'employment_type' not in data \
            or 'company_size' not in data \
            or 'role' not in data \
            or 'residence' not in data \
            or 'remote%' not in data:

            return make_response(jsonify({'message' : 'Missing A Category'}), 400)


        



        return make_response(jsonify(data), 201)
  

  
api.add_resource(Prediction, '/pred')
  
  
# driver function
if __name__ == '__main__':

    ## load in model on start
    app.run(debug = True)