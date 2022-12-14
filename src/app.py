from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy as np
import pickle
import json

app = Flask(__name__)
api = Api(app)

# Create a function to create log transformations of Total_Income and LoanAmount
def transform_features(df):
    """
    - Returns a dataframe with:
        - Log of the Total_Income
        - Log of the LoanAmount
        - Transformed features dropped
    """
    
    # Log of loan amount
    df['LoanAmount_log'] = np.log(df['LoanAmount'].astype('float64')) 

    # Total income and log of total income
    df['Total_Income'] = df['ApplicantIncome'] + df['CoapplicantIncome']
    
    transformed_feats = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Total_Income']
    df['Total_Income_log'] = np.log(df['Total_Income'].astype('float64')) 

    return df[['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
       'Loan_Amount_Term', 'Credit_History', 'Property_Area', 'Total_Income_log','LoanAmount_log']]

model = pickle.load(open('/Users/silvh/OneDrive/lighthouse/projects/mini-project-IV/model_logistic_regression.sav', "rb" ) )

class predict(Resource):
    def post(self):
        json_data = request.get_json()
        df = pd.DataFrame(json_data.values(), index=json_data.keys()).transpose()

        res = model.predict(df)

        res = res.tolist()

        if res == ['Y']:
            res.append(dict({'Meaning of prediction': 'Loan application approval. ☺'}))

        return res

# assign endpoint
api.add_resource(predict, '/predict')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)