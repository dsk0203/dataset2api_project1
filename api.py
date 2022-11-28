
from flask import Flask, jsonify, request,  make_response
from flask_restful import Resource, Api
import joblib
import pandas as pd

# load in our model
loaded_model = joblib.load('finalized_model.sav')

# load in our encoder
encoder = joblib.load('OHEencoder.sav')

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

        # tell how to make requests to our API (during posts)
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
        
        # grab the payload data sent
        data = request.get_json()

        # make sure we have all of our columns
        if 'experience_level' not in data \
            or 'employment_type' not in data \
            or 'company_size' not in data \
            or 'role' not in data \
            or 'residence' not in data \
            or 'remote%' not in data:

            return make_response(jsonify({'message' : 'Missing A Category'}), 400)

        # convert the roles
        # the exact same way we did
        # in trainning
        def convertJob(text):
            
            '''
            converts job titles to form model can understand
            '''
    
            if 'lead' in text.lower() or 'manager' in text.lower() or 'director' in text.lower() or 'head' in text.lower():
                return 'LDR'
            
            elif 'machine' in text.lower() or 'ai ' in text.lower() or 'vision' in text.lower():
                return 'ML'
            
            if 'scientist' in text.lower() or 'analytics' in text.lower() or 'science' in text.lower():
                return 'DS'
            
            if 'analyst' in text.lower():
                return 'AL'
            
            if 'engineer' in text.lower():
                return 'DE'

            
            return 'OTHR_ROLE'

        # convert residence
        # the exact same way we did
        # in trainning
        def convertResidence(text):

            '''
            converts user input of residence so model can understand
            
            '''

            if len(text) != 2:
                return 'OTHER_RES'
    
            approved = ['US','GB','IN','CA','DE','FR','ES','GR','JP']
            
            if text.upper() in approved:
                return text
            
            return 'OTHR_RES'

        # convert remote work
        # the exact same way we did
        # in trainning
        def ConvertRemote(percentage):
            
            if int(percentage) > 50:
                return 'Remote'
            
            if int(percentage) < 50:
                return 'Office'
            
            return 'Hybrid'

        # build out a prediction dictionary, using our functions 
        # that we used during trainning
        user_dict = {
            'experience_level': data['experience_level'],
            'employment_type' : data['employment_type'],
            'company_size' : data['company_size'],
            'roles_converted' : convertJob(data['role']),
            'residence_converted' : convertResidence(data['residence']),
            'remote_converted' : ConvertRemote(data['remote%'])
        }

        # convert our dictoinary to a dataframe
        df = pd.DataFrame([user_dict])


        # use our encoder from trainning
        encoded_df = pd.DataFrame(encoder.transform(df).toarray())

        # now use our model from trainning for a prediction
        pred = loaded_model.predict(encoded_df)


        # return our prediction in a JSON
        return make_response(jsonify({'prediction' : str(pred[0])}), 201)


    


  
api.add_resource(Prediction, '/pred')
  
  
# driver function
if __name__ == '__main__':

    ## load in model on start
    app.run(debug = True)