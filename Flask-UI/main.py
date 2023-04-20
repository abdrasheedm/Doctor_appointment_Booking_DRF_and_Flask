from flask import Flask, render_template, session, request, redirect, url_for, render_template_string, jsonify

import requests
import secrets

secret_key = secrets.token_hex(32)
app = Flask(__name__)
app.secret_key = secret_key

BASEURL = 'http://127.0.0.1:8000/api/'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['mobile']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 == password2:
            data = {
                "first_name" : first_name,
                "last_name" : last_name,
                "email" : email,
                "phone_number" : phone_number,
                "password" : password1
            }
            response = requests.post(BASEURL+'account/signup/', data=data)
            if response.status_code == 201:
                data = response.json()
                return redirect(url_for('verify_otp', phone_number=phone_number))
            else:
                print(response.json())

    return render_template('signup.html')   


@app.route('/verify_otp/<phone_number>', methods=['GET', 'POST'])
def verify_otp(phone_number):
    if request.method == 'POST':
        otp = request.form['otp']
        mobile = request.form['mobile']
        data = {
            "otp" : otp,
            "phone_number" : mobile
        }
        response = requests.post(BASEURL+'account/verify-otp/', data=data)
        if response.status_code == 200:
            return redirect('/signin')
        else:
            print(response.json())
            return redirect('/verify_otp')
    return render_template('verify_otp.html', mobile=phone_number)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        data = {
            "email" : email,
            "password" : password
        }
        response = requests.post(BASEURL+'account/signin/', data=data)
        if response.status_code == 200:
            data = response.json()
            session["token"] = data['token']
            session["user_id"] = data['user_id']
            return redirect('/')
        else:
            print(response.json())
            return redirect('/signin')
    return render_template('signin.html')


@app.route('/logout')
def logout():
    # remove token an user_id from session
    session.pop('token', None)
    session.pop('user_id', None)

    return redirect('/')


@app.route('/book-an-appointment')
def book_appointment():
    response = requests.get(BASEURL+'doctors/categories/')
    if response.status_code == 200:
        data = response.json()
        print(data)
        return render_template('appointment.html', data=data)
    else:
        print(response.json())
        return redirect('/')
    

@app.route('/choose-doctor/<int:cat_id>', methods=['GET', 'POST'])
def choose_doctor(cat_id):
    print(cat_id, 'cat_id')
    response = requests.get(BASEURL+'doctors/get-doctors-by-category/?_id='+str(cat_id))
    if response.status_code == 200:
        data = response.json()
        print(data)
        return render_template('doctors.html', data=data)
    else:
        print(response.json())
        return redirect('/')
    
@app.route('/choose-time/<int:doc_id')
def choose_time(doc_id):
    print(doc_id)
    

    


if __name__ == "__main__":
    app.run(debug=True, port=9000)
