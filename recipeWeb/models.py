from recipeWeb import db, loginManager
from sqlalchemy import exc
from flask_login import UserMixin
import csv

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    userSavedFoods = db.relationship('UserFoods', backref='savedFoods', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class FoodItem(db.Model):
    __tablename__='fooditem'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), nullable=False)
    image = db.Column(db.String(225), nullable=False, default='default.jpg')
    stars = db.Column(db.String(20), nullable=True)
    reviews = db.Column(db.String(20), nullable=True)
    level = db.Column(db.String(50), nullable=True) 
    time = db.Column(db.String(50), nullable=True)
    servings = db.Column(db.String(20), nullable=True)
    ingredients = db.Column(db.Text, nullable=True)
    directions = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(227), nullable=True)
    usersThatSavedItem = db.relationship('UserFoods', backref='savedUsers', lazy=True)

    def __repr__(self):
        return f"FoodItem('{self.name}','{self.image}','{self.stars}','{self.reviews}','{self.level}','{self.time}','{self.servings}','{self.ingredients}','{self.directions}','{self.tags}')"

class UserFoods(db.Model):
    __tablename__='userfoods'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    foodId = db.Column(db.Integer, db.ForeignKey('fooditem.id'), nullable=False)

    def __repr__(self):
        return f"UserFoods('{self.userId}','{self.foodId}')"

class FoodComments(db.Model):
    __tablename__='foodcomments'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(120), nullable=False)
    foodId = db.Column(db.String(225), nullable=False)
    post = db.Column(db.Text, nullable=True)
#db.drop_all()
db.create_all()



flist=[]
with open('v1.csv', 'r',encoding='utf-8') as f:
  reader = csv.reader(f)
  flist = list(reader)

flist[0][0]='id'

try:
    for i in range(1,len(flist)):
        fooditem = FoodItem(id=i,
                            name=flist[i][0],
                            image=flist[i][1],
                            stars=flist[i][2],
                            reviews=flist[i][3],
                            level=flist[i][4],
                            time=flist[i][5],
                            servings=flist[i][6],
                            ingredients=flist[i][7],
                            directions=flist[i][8],
                            tags=flist[i][9])
        db.session.add(fooditem)
        print(i)

    db.session.commit()
except exc.IntegrityError:
    db.session.rollback()
