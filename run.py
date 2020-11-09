from flask import Flask,render_template,request,redirect,url_for 
from pymongo import MongoClient
from bson import ObjectId
from flask_login import login_required, current_user, login_user, logout_user
from models import login, UserModel
import os
from flask_socketio import SocketIO, emit
from flask import session

# config system
app = Flask(__name__, static_folder="images")
app.config.update(dict(SECRET_KEY='yoursecretkey'))
client = MongoClient('localhost:27017')
db = client.Image
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

login.init_app(app)
login.login_view = 'loginPage'

socketio = SocketIO(app)

@socketio.on('disconnect')
def disconnect_user():
    logout_user()
    session.pop('yourkey', None)

@app.route("/create", methods = ['POST'])
@login_required
def create():
    if not current_user.is_authenticated:
        return render_template('loginPage.html')
    image_name=request.values.get("image_name")  
    key1=request.values.get("key1")
    value1=request.values.get("value1")
    if(request.values.get("dataType1") == "double"):
        value1 = float(value1)
    key2=request.values.get("key2")
    value2=request.values.get("value2")
    if(request.values.get("dataType2") == "double"):
        value2 = float(value2)
    key3=request.values.get("key3")
    value3=request.values.get("value3")
    if(request.values.get("dataType3") == "double"):
        value3 = float(value3)

    target = os.path.join(APP_ROOT,'images/')
    if not os.path.isdir(target):
        os.mkdir(target)
    for upload in request.files.getlist("img"):
        filename = image_name
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png"):
            print("File supported moving on...")
        else:
            return render_template('create.html')
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)

    if image_name:
        entry = {"name":image_name, key1:value1, key2:value2, key3:value3}
        db.ImageEntry.insert_one(entry)
        return redirect('/listall')

    else:
        return render_template('create.html')

@app.route("/create", methods = ['GET'])
@login_required
def createGET():
    if not current_user.is_authenticated:
        return render_template('loginPage.html')

    return render_template('create.html')

@app.route("/search", methods = ['GET', 'POST'])
def search():
    key1=request.values.get("key1")
    value1=request.values.get("value1")
    if(request.values.get("dataType1") == "double"):
        value1 = float(value1)
    op = request.values.get("operation")
    # key2=request.values.get("key2")
    # value2=request.values.get("value2")
    # key3=request.values.get("key3")
    # value3=request.values.get("value3")
    # entry = {key1:value1, key2:value2, key3:value3}
    if op == "eq":
        entry = {key1:value1}
        results = db.ImageEntry.find(entry)
    elif op == "gt":
        print({key1:{"$gt":value1}})
        results = db.ImageEntry.find({key1:{"$gt":value1}})
    else :
        results = db.ImageEntry.find({key1:{"$lt":value1}})
    # for result in results:
    #     # target = os.path.join(APP_ROOT,'images/')
    #     # destination = "".join([target, result.get('name')])
    #     # names.append(destination)
    #     names.append(result.get('name'))
    return render_template('results.html', data = results)

@app.route('/authenticate', methods = ['GET', 'POST'])
def authenticate():
    uname=request.values.get("uname")  
    psw=request.values.get("psw")
    userType=request.values.get("userType")
    user = UserModel(uname,psw)
    if(psw == "root" and uname == "root"):
        login_user(user)
        return render_template('adminHome.html')
    elif(userType == "guest" and uname == "guest" and psw == "guest"):
        return render_template('searchPage.html')

    return render_template('error.html')

@app.route("/")
def loginPage():
    return render_template('loginPage.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    session.pop('yourkey', None)
    return render_template('loginPage.html')

@app.route("/remove")
@login_required  
def remove ():  
    #Deleting a user with various references  
    key=request.values.get("_id")  
    db.ImageEntry.remove({"_id":ObjectId(key)})  
    return redirect("/listall")  


@app.route("/listall", methods = ['GET', 'POST'])
@login_required
def listall():
    if not current_user.is_authenticated:
        return render_template('loginPage.html')
    docs = db.ImageEntry.find()
    data = []
    for i in docs:
        data.append(i)
    return render_template('listall.html', data = data)

if __name__=='__main__':
    app.run(debug=True)
