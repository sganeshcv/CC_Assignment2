from flask_login import LoginManager
 
login = LoginManager()

class UserModel(): 
    
    def __init__(self,username,password):
        self.username = username
        self.password = password
     
    def check_password(self):
        if self.password == "root":
            return True
        return False

    def is_authenticated(self):
        return True
   
    
    def is_active(self):
        if(self):
            return True
        return False
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.username + "%" + self.password)
 
 
@login.user_loader
def load_user(id):
    return UserModel(id.split("%")[0],id.split("%")[1])