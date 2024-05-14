import time

from bson import ObjectId
from db import collection, service_provider_collection

import ssl
from functools import wraps
from flask import session,redirect,url_for,request, render_template

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session and 'username' in session:
            return func(*args, **kwargs)
        else:
            # Store the requested URL in the session before redirecting to login
            session['next_url'] = request.url
            return redirect(url_for('login'))
    return wrapper
    
    
def current_user():
    # Check if the user is logged in
    if 'user_id' in session:
        user_id = session['user_id'] 
        # user_id =  "65d4885c537bae39a494c49a"

        # Retrieve user data from MongoDB using the user_id
        user_data = collection.find_one({'_id': ObjectId(user_id)})
        return user_data
    
def current_user_service():
    # Check if the user is logged in
    if 'user_id' in session:
        user_id = session['user_id'] 
        # user_id =  "65d4885c537bae39a494c49a"

        # Retrieve user data from MongoDB using the user_id
        user_data = service_provider_collection.find_one({'_id': ObjectId(user_id)})
        return user_data
    
import boto3
from botocore.exceptions import NoCredentialsError
ACCESS_KEY='AKIA4C6C3STL37NFUWNO'
SECRET_KEY='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'
def upload_profile_cover_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return {"url":f"https://bixid.s3.amazonaws.com/{s3_file}"}
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    