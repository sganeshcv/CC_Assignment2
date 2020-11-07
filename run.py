from flask import Flask, render_template,request,redirect,url_for 
from pymongo import MongoClient
from bson import ObjectId
from flask_login import login_required, current_user, login_user, logout_user

# config system
app = Flask(__name__)
app.config.update(dict(SECRET_KEY='yoursecretkey'))
client = MongoClient('localhost:27017')
db = client.Image

login.init_app(app)
login.login_view = 'login'

@app.route("/create", methods = ['POST'])
@login_required
def create():
    image_name=request.values.get("image_name")  
    key1=request.values.get("key1")
    value1=request.values.get("value1")
    key2=request.values.get("key2")
    value2=request.values.get("value2")
    key3=request.values.get("key3")
    value3=request.values.get("value3")
    entry = {"name":image_name, key1:value1, key2:value2, key3:value3}
    db.ImageEntry.insert_one(entry)
    return redirect('/listall')

@app.route("/create", methods = ['GET'])
@login_required
def createGET():
    return render_template('create.html')

# @app.route("/redirectPage", methods = ['GET', 'POST'])
# def redirectPage():
#     page = request.values.get("page")
#     print(page)
#     return render_template(page)

@app.route("/search", methods = ['GET', 'POST'])
def search():
    key1=request.values.get("key1")
    value1=request.values.get("value1")
    key2=request.values.get("key2")
    value2=request.values.get("value2")
    key3=request.values.get("key3")
    value3=request.values.get("value3")
    entry = {key1:value1, key2:value2, key3:value3}
    db.ImageEntry.insert_one(entry)
    return render_template('results.html')

@app.route('/authenticate', methods = ['GET', 'POST'])
def authenticate():
    uname=request.values.get("uname")  
    psw=request.values.get("psw")
    userType=request.values.get("userType")
    
    if(userType == "admin" and uname == "root" and psw == "root"):
        return render_template('adminHome.html')

    elif(userType == "guest" and uname == "guest" and psw == "guest"):
        return render_template('searchPage.html')

    return render_template('error.html')

@app.route("/")
def login():
    return render_template('loginPage.html')

@app.route("/remove")
@login_required  
def remove ():  
    #Deleting a user with various references  
    key=request.values.get("_id")  
    db.ImageEntry.remove({"_id":ObjectId(key)})  
    return redirect("/listall")  


@app.route("/listall", methods = ['GET', 'POST'])
def listall():
    docs = db.ImageEntry.find()
    data = []
    for i in docs:
        data.append(i)
    return render_template('listall.html', data = data)

if __name__=='__main__':
    app.run(debug=True)
