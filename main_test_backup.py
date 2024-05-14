import json
# from bson import json_util
from flask import Flask, jsonify, render_template, redirect,request, session,flash,url_for
import requests
from test import PhonePe 
from db import collection
from functons import  current_user, login_required, upload_profile_cover_to_aws


app = Flask(__name__,static_folder="static") 
app.secret_key = 'Dheeraj@2006'

MERCHANT_ID = "PGTESTPAYUAT"
SECRET_KEY = "14fa5465-f8a7-443f-8477-f986b8fcfde9"

# Create a PhonePe payment client
phonepe = PhonePe(merchant_id=MERCHANT_ID,phone_pe_salt=SECRET_KEY ,phone_pe_host="https://api.phonepe.com/apis/hermes",redirect_url="http://127.0.0.1:5000/return-to-me",webhook_url="")


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home/index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=="POST":
        # Get form data
        print(request.form)
        email = request.form['email']
        existing_user = collection.find_one({'email': email})
        if existing_user:
            # Alert the user that the email is already registered
            flash('Email already registered. Please use a different email.', 'error')
            return render_template('account/register.html')
        profile_image = request.files['profile_picture']
        profile_image.save("pf.jpg")
        
        if request.files['profile_picture'].filename != '':
            profile_image_=upload_profile_cover_to_aws('pf.jpg','bixid',f'{email}_profile_image.jpg')
            profile_image_url=profile_image_['url']
        elif request.files['profile_picture'].filename == '':
            profile_image_url=''
        dc = request.files['doctor_certificate']
        dc.save("dc.pdf")
        if request.files['doctor_certificate'].filename != '':
            dc_=upload_profile_cover_to_aws('dc.pdf','bixid',f'{email}_dc.pdf')
            dc_url=dc_['url']
        elif request.files['profile_picture'].filename == '':
            profile_image_url=''
        password = request.form['pass']
        twitter = request.form['twitter']
        facebook = request.form['facebook']
        insta = request.form['insta']
        username = request.form['username']
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        address = request.form['address']
        about = request.form['about']
        # You can similarly get other form data here

        # Insert user data into MongoDB
        user_data = {
            'email': email,
            'password': password,
            'twitter': twitter,
            'facebook': facebook,
            'insta': insta,
            'username': username,
            "profile_image":profile_image_url,
            'fname': fname,
            'lname': lname,
            'phone': phone,
            'address': address,
            'about': about,
            'Doctor certificate': NULL,
            'verified':False
            # Add other fields as needed
        }
        # Insert user data into MongoDB
        session['account_status']='pending'
        collection.insert_one(user_data)
        # flash('Registration successful you can now login ', 'success')
        return redirect(url_for('login'))
        
    else:
        return render_template('account/register.html')


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
                flash('Login Successfully .', 'success')
                return redirect(url_for('index'))
            else:
                flash('Email already registered. Please use a different email.', 'danger')
                return  render_template('account/login.html')
        else:
            return render_template('account/login.html')
    except Exception as err:
        flash(err, 'danger')
        return render_template("account/login.html", error=err)
    
    
    
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
@app.route('/terms-condition', methods=['GET', 'POST'])
def terms_condition():
    return render_template("home/terms_condition.html")

@app.route('/checkout', methods=['GET','POST'])
def checkout():
    if request.method=='POST':
        if request.form.get('stage')=="initial":
            return render_template("home/checkout.html")
        elif request.form.get("stage")=="payment":
            fullname = request.form['fullname']
            email = request.form['email']
            phone = request.form['phone']
            tickets = request.form['tickets']
            total_price = int(request.form['price']) * tickets  # Assuming price is passed as a hidden field in the form
            order_data= phonepe.create_txn("123456432", total_price, "USER_ID")
            print(order_data)
            #Extract Payment Link
            link = order_data["data"]["instrumentResponse"]["redirectInfo"]["url"]
            
            print(link)
            



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
                twitter = request.form['twitter']
                facebook = request.form['facebook']
                insta = request.form['insta']
                username = request.form['username']
                fname = request.form['fname']
                lname = request.form['lname']
                phone = request.form['phone']
                address = request.form['address']
                about = request.form['about']
            # You can similarly get other form data here

            # Insert user data into MongoDB
                user_data = {
                
                
                    'twitter': twitter,
                    'facebook': facebook,
                    'insta': insta,
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
       
        
if __name__ == '__main__':
    app.run(debug=True)
import json
# from bson import json_util
from flask import Flask, jsonify, render_template, redirect,request, session,flash,url_for
import requests
from test import PhonePe 
from db import collection
from functons import  current_user, login_required, upload_profile_cover_to_aws
import shortuuid
import img2pdf

app = Flask(__name__,static_folder="static") 
app.secret_key = 'Dheeraj@2006'

MERCHANT_ID = "PGTESTPAYUAT"
SECRET_KEY = "14fa5465-f8a7-443f-8477-f986b8fcfde9"

# Create a PhonePe payment client
phonepe = PhonePe(merchant_id=MERCHANT_ID,phone_pe_salt=SECRET_KEY ,phone_pe_host="https://api.phonepe.com/apis/hermes",redirect_url="http://127.0.0.1:5000/return-to-me",webhook_url="")


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home/index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=="POST":
        # Get form data
        print(request.form)
        email = request.form['email']
        existing_user = collection.find_one({'email': email})
        if existing_user:
            # Alert the user that the email is already registered
            flash('Email already registered. Please use a different email.', 'error')
            return render_template('account/register.html')
        profile_image = request.files['profile_picture']
        profile_image.save("pf.jpg")
        
        if request.files['profile_picture'].filename != '':
            profile_image_=upload_profile_cover_to_aws('pf.jpg','bixid',f'{email}_profile_image.jpg')
            profile_image_url=profile_image_['url']
        elif request.files['profile_picture'].filename == '':
            profile_image_url=''
        dc = request.files['doctor_certificate']
        dc.save("dc.pdf")
        if request.files['doctor_certificate'].filename != '':
            dc_=upload_profile_cover_to_aws('dc.pdf','bixid',f'{email}_dc.pdf')
            dc_url=dc_['url']
        elif request.files['profile_picture'].filename == '':
            profile_image_url=''
        password = request.form['pass']
        twitter = request.form['twitter']
        facebook = request.form['facebook']
        insta = request.form['insta']
        username = request.form['username']
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        address = request.form['address']
        about = request.form['about']
        # You can similarly get other form data here

        # Insert user data into MongoDB
        user_data = {
            'email': email,
            'password': password,
            'twitter': twitter,
            'facebook': facebook,
            'insta': insta,
            'username': username,
            "profile_image":profile_image_url,
            'fname': fname,
            'lname': lname,
            'phone': phone,
            'address': address,
            'about': about,
            'Doctor certificate': dc_url,
            'verified':False
            # Add other fields as needed
        }
        # Insert user data into MongoDB
        session['account_status']='pending'
        collection.insert_one(user_data)
        # flash('Registration successful you can now login ', 'success')
        return redirect(url_for('login'))
        
    else:
        return render_template('account/register.html')


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
                flash('Login Successfully .', 'success')
                return redirect(url_for('index'))
            else:
                flash('Email already registered. Please use a different email.', 'danger')
                return  render_template('account/login.html')
        else:
            return render_template('account/login.html')
    except Exception as err:
        flash(err, 'danger')
        return render_template("account/login.html", error=err)
    
    
    
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
@app.route('/terms-condition', methods=['GET', 'POST'])
def terms_condition():
    return render_template("home/terms_condition.html")

@app.route('/checkout', methods=['GET','POST'])
def checkout():
    if request.method=='POST':
        if request.form.get('stage')=="initial":
            return render_template("home/checkout.html")
        elif request.form.get("stage")=="payment":
            fullname = request.form['fullname']
            email = request.form['email']
            phone = request.form['phone']
            tickets = request.form['tickets']
            total_price = int(request.form['price']) * tickets  # Assuming price is passed as a hidden field in the form
            order_data= phonepe.create_txn("123456432", total_price, "USER_ID")
            print(order_data)
            #Extract Payment Link
            link = order_data["data"]["instrumentResponse"]["redirectInfo"]["url"]
            
            print(link)
            



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
                twitter = request.form['twitter']
                facebook = request.form['facebook']
                insta = request.form['insta']
                username = request.form['username']
                fname = request.form['fname']
                lname = request.form['lname']
                phone = request.form['phone']
                address = request.form['address']
                about = request.form['about']
            # You can similarly get other form data here

            # Insert user data into MongoDB
                user_data = {
                
                
                    'twitter': twitter,
                    'facebook': facebook,
                    'insta': insta,
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
       
        
if __name__ == '__main__':
    app.run(debug=True)
