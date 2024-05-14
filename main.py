import hashlib
import json
from bson import ObjectId
from flask import Flask, jsonify, render_template, redirect,request, session,flash,url_for
from config import MERCHANT_ID, SECRET_KEY
from db import collection,service_provider_collection
from phonepe import PhonePe
from functons import  current_user_service, current_user, upload_profile_cover_to_aws


app = Flask(__name__,static_folder="static") 
app.secret_key = 'Dheeraj@2006'
# # phonepe = PhonePe(MERCHANT_ID, SECRET_KEY, "https://api.phonepe.com/apis/hermes", "https://doctress.in/verify_payment","https://doctress.in/verify_payment")
# phonepe = PhonePe(MERCHANT_ID, SECRET_KEY, "https://api.phonepe.com/apis/hermes", "http://127.0.0.1:5000/verify_payment","http://127.0.0.1:5000/verify_payment")

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home/index.html')

# # # # # #  Doctor  Payment methods


@app.route('/event', methods=['GET','POST'])
def event():
    return render_template("home/event.html")
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=="POST":
        print(request.form)
        email = request.form['email']
        existing_user = collection.find_one({'email': email})
        if existing_user:
            flash('Email already registered. Please use a different email.', 'error')
            return render_template('account/register.html')
        profile_image = request.files['profile_picture']
        profile_image.save("pf.jpg")
        
        if request.files['profile_picture'].filename != '':
            profile_image_=upload_profile_cover_to_aws('pf.jpg','bixid',f'{email}_profile_image.jpg')
            profile_image_url=profile_image_['url']
        elif request.files['profile_picture'].filename == '':
            profile_image_url=''
        dc_url = ""
        
        password = request.form['pass']
        username = request.form['username']
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        address = request.form['address']
        about = request.form['about']

        user_data = {
            'email': email,
            'password': password,
            'username': username,
            "profile_image":profile_image_url,
            'fname': fname,
            'phone': phone,
            'address': address,
            'about': about,
            'Doctor_certificate': "",
            "account_status":"pending",
            "membership":0
        }
        print(user_data)
        result=collection.insert_one(user_data)
    
        session['username'] = username
        session['user_id']=str(result.inserted_id).replace(" ObjectId(","").replace(")","")

        return redirect(url_for('checkout_doctor'))
        
    else:
        return render_template('account/register.html')
    
    
    
@app.route('/register-service-provider', methods=['GET', 'POST'])
def register_service_provider():
    if request.method=="POST":
        print(" i am in poerefkel")
        print(request.form)
        email = request.form['email']
        existing_user = service_provider_collection.find_one({'email': email})
        if existing_user:
            flash('Email already registered. Please use a different email.', 'error')
            return render_template('account/register.html')
        profile_image = request.files['profile_picture']
        profile_image.save("pf.jpg")
        
        if request.files['profile_picture'].filename != '':
            profile_image_=upload_profile_cover_to_aws('pf.jpg','bixid',f'{email}_profile_image.jpg')
            profile_image_url=profile_image_['url']
        elif request.files['profile_picture'].filename == '':
            profile_image_url=''
        dc = request.files['aadhar_card']
        dc.save("aadhar_card.pdf")
        if request.files['aadhar_card'].filename != '':
            dc_=upload_profile_cover_to_aws('aadhar_card.pdf','bixid',f'{email}_aadhar_card.pdf')
            dc_url=dc_['url']
        elif request.files['profile_picture'].filename == '':
            profile_image_url=''
        password = request.form['pass']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        phone_number = request.form['phone_number']
        address = request.form['address']
        city = request.form['city']
        state = request.form['country']
        country = request.form['name']
        about = request.form['about_us']
        company_name = request.form['company_name']
        company_address = request.form['company_address']
       

        user_data = {
            'email': email,
            'password': password,
            'username': name,
            "profile_image":profile_image_url,
            'age': age,
            'gender': gender,
            'phone': phone_number,
            'address': address,
            'city': city,
            'state': state,
            'country': country,
            'about': about,
            'adhar_card': dc_url,
            'company_name': company_name,
            'company_address': company_address,
            "account_status":"pending",
            "membership":0
        }
        
        result=service_provider_collection.insert_one(user_data)
    
        session['username'] = name
        session['user_id']=str(result.inserted_id).replace(" ObjectId(","").replace(")","")

        return redirect(url_for('checkout_service'))
        
    else:
        return render_template('account/register_service_provider.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        print("this is login")
        if request.method == 'POST':
            print("in post request")
            print(request.form)
            username = request.form['email']
            password = request.form['pass']
            user_data = collection.find_one({'email': username, 'password': password})
            print(user_data)
            if user_data:
                # user_data_json = json_util.dumps(user_data)
                # print(user_data_json)
                user_data=json.loads(str(user_data).replace("'",'"').replace(" ObjectId(","").replace(")",""))
                
                session['username'] = username
                session['user']=user_data
                session['user_id']=user_data['_id']
                session['login']=True
                if user_data['membership']==1: 
                    flash('Login Successfully .', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Login Successfully Kindly complete the payment', 'success')
                    return redirect(url_for('checkout_doctor'))
            else:
                flash('User not found  register first .', 'danger')
                return  render_template('account/login.html')
        else:
            return render_template('account/login.html')
    except Exception as err:
        flash(err, 'danger')
        return render_template("account/login.html", error=err)
    
@app.route('/login-service-provider', methods=['GET', 'POST'])
def login_service_provider():
    try:
        print("this is login")
        if request.method == 'POST':
            print("in post request")
            print(request.form)
            username = request.form['email']
            password = request.form['pass']
            user_data = service_provider_collection.find_one({'email': username, 'password': password})
            print(user_data)
            if user_data:
                # user_data_json = json_util.dumps(user_data)
                # print(user_data_json)
                user_data=json.loads(str(user_data).replace("'",'"').replace(" ObjectId(","").replace(")","")) 
                session['username'] = username
                session['user']=user_data
                session['user_id']=user_data['_id']
                session['login']=True
                if user_data['membership']==1: 
                    flash('Login Successfully .', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Login Successfully Kindly complete the payment', 'success')
                    return redirect(url_for('checkout_service'))
            else:
                flash('User not found  register first .', 'danger')
                return  render_template('account/login_service_provider.html')
        else:
            return render_template('account/login_service_provider.html')
    except Exception as err:
        flash(err, 'danger')
        return render_template("account/login_service_provider.html", error=err)
 


   



@app.route('/update_user_profile', methods=['GET', 'POST'])
def update_user_profile():
    try:
        if request.method == 'POST':
            profile_image = request.files['profile_picture']
            profile_image.save("pf.jpg")
            if request.files['profile_picture'].filename != '':
                profile_image_=upload_profile_cover_to_aws('pf.jpg','bixid',f'{session["user"]["email"]}_profile_image.jpg')
                profile_image_url=profile_image_['url']
            elif request.files['profile_picture'].filename == '':
                profile_image_url=''
                username = request.form['username']
                fname = request.form['fname']
                lname = request.form['lname']
                phone = request.form['phone']
                address = request.form['address']
                about = request.form['about']
            # You can similarly get other form data here

            # Insert user data into MongoDB
                user_data = {
                    'username': username,
                    "profile_image":profile_image_url,
                    'fname': fname,
                    'lname': lname,
                    'phone': phone,
                    'address': address,
                    'about': about
                    # Add other fields as needed
                }
                update_operation = {
                "$set": user_data
            }
                result = collection.update_one({"email": session['user']['email']}, update_operation)
                print(result)
                # Check if the update was successful
                if result.modified_count > 0:
                    flash("User updated successfully","success")
                else:
                    flash("User not found or no update necessary","danger")
                    
                        # Insert user data into MongoDB
                user=current_user()
                user.pop('_id')
                session['user']=user
                print(session['user'])
                return redirect(url_for('profile'))           
                
    except Exception as err :
        flash(str(err), 'danger')
        return render_template("home/update_profile.html" )
    user=current_user()
    user.pop('_id')
    session['user']=user
    print(session['user'])
        
    return render_template("home/update_profile.html" )        
       
       
       
       
       
       
       
       
       
# # # # # #  Doctor  Payment methods


@app.route('/checkout-doctor', methods=['GET','POST'])
def checkout_doctor():
    if request.method=='POST':
        if request.form.get('stage')=="initial":
            return render_template("home/checkout.html")
        elif request.form.get("stage")=="payment":
            import uuid
            unique_id = str(uuid.uuid4().int)[:8]
            merchantTransactionId = "MT" + unique_id
            amount=request.form.get("price")
            phonepe = PhonePe(MERCHANT_ID, SECRET_KEY, "https://api.phonepe.com/apis/hermes", "https://doctress.in/verify-payment","https://doctress.in/verify-payment")
            #phonepe = PhonePe(MERCHANT_ID, SECRET_KEY, "https://api.phonepe.com/apis/hermes", "http://127.0.0.1:5000/verify_payment","http://127.0.0.1:5000/verify_payment")

            response_data=phonepe.create_txn(merchantTransactionId,int(amount)*100,"MUID123")
            print(response_data)
            return redirect(response_data['data']['instrumentResponse']['redirectInfo']['url'])
    return render_template("home/checkout.html",price=288,type="doctor")        
           

@app.route('/verify-payment', methods=['GET','POST'])
def verify_payment_doctor():
    if request.method=='POST':
        form_data = request.form
        form_data_dict = dict(form_data)
        phonepe = PhonePe(MERCHANT_ID, SECRET_KEY, "https://api.phonepe.com/apis/hermes", "https://doctress.in/verify-payment","https://doctress.in/verify-payment")
        #phonepe = PhonePe(MERCHANT_ID, SECRET_KEY, "https://api.phonepe.com/apis/hermes", "http://127.0.0.1:5000/verify_payment","http://127.0.0.1:5000/verify_payment")

        response=phonepe.check_txn_status(request.form.get('transactionId'))
        print(response)
        if response['success']:
            print(session)
            user_id=session['user_id']
            query = {'_id':ObjectId(user_id)}  
            update_data = {'$set': {'account_status': 'approved', 'membership': 1}}
            a=collection.update_one(query, update_data)
            print(a)
            session['login']=True
            user=current_user()
            user.pop('_id')
            session['user']=user
            flash(response['message'], response['success'])
            return redirect(url_for('index'))  
    return "this is not post request"         
       
       
       
# # # Service provider payment modes        


@app.route('/checkout-service', methods=['GET','POST'])
def checkout_service():
    if request.method=='POST':
        if request.form.get('stage')=="initial":
            return render_template("home/checkout.html")
        elif request.form.get("stage")=="payment":
            import uuid
            unique_id = str(uuid.uuid4().int)[:8]
            merchantTransactionId = "MT" + unique_id
            amount=request.form.get("price")
            phonepe = PhonePe(MERCHANT_ID, SECRET_KEY, "https://api.phonepe.com/apis/hermes", "https://doctress.in/verify-payment-service","https://doctress.in/verify-payment-service")
            #phonepe = PhonePe(MERCHANT_ID, SECRET_KEY, "https://api.phonepe.com/apis/hermes", "http://127.0.0.1:5000/verify_payment","http://127.0.0.1:5000/verify_payment")
            response_data=phonepe.create_txn(merchantTransactionId,int(amount)*100,"MUID123")
            return redirect(response_data['data']['instrumentResponse']['redirectInfo']['url'])
    return render_template("home/checkout.html",price=2088,type="service")        
           

@app.route('/verify-payment-service', methods=['GET','POST'])
def verify_payment_service():
    if request.method=='POST':
        form_data = request.form
        form_data_dict = dict(form_data)
        phonepe = PhonePe(MERCHANT_ID, SECRET_KEY, "https://api.phonepe.com/apis/hermes", "https://doctress.in/verify_payment","https://doctress.in/verify_payment")
        #phonepe = PhonePe(MERCHANT_ID, SECRET_KEY, "https://api.phonepe.com/apis/hermes", "http://127.0.0.1:5000/verify_payment","http://127.0.0.1:5000/verify_payment")
        response=phonepe.check_txn_status(request.form.get('transactionId'))
        print(response)
        if response['success']:
            print(session)
            user_id=session['user_id']
            print(user_id)
            query = {'_id':ObjectId(user_id)}
            print(query)
            update_data = {'$set': {'account_status': 'approved', 'membership': 1}}
            a=service_provider_collection.update_one(query, update_data)
            print("this is a ",a)
            session['login']=True
            user=current_user_service()
            user.pop('_id')
            session['user']=user
            flash(response['message'], response['success'])
            return redirect(url_for('index'))  
    return "this is not post request"         
       
       
       
       
       
       
@app.route("/logout", methods=['GET', 'POST'])  
def logout(): 
    session.pop('username',None)
    session.pop('login',None)
    session['login']=False
    return redirect(url_for('index'))   
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user=current_user()
    user.pop('_id')
    session['user']=user
    return render_template("home/profile.html", )
@app.route('/refund-policy', methods=['GET', 'POST'])
def refund_policy():
    return render_template("home/refund_policy.html")
    
@app.route('/privacy-policy', methods=['GET', 'POST'])
def privacy_policy():
    return render_template("home/privacy_policy.html")
@app.route('/terms-condition', methods=['GET', 'POST'])
def terms_condition():
    return render_template("home/terms_condition.html")
        
if __name__ == '__main__':
    app.run(debug=True)
