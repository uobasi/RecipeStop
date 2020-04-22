from recipeWeb.models import User, FoodItem, UserFoods, FoodComments
from flask import render_template, url_for, flash, redirect, request, jsonify
from recipeWeb.form import RegisterForm, LoginForm
from recipeWeb import app, db
from sqlalchemy import or_, and_
from flask_login import login_user, current_user, logout_user, login_required

foodList=[]
count = 0
for i in FoodItem.query.all():
    if i.image != 'No Image':
        print(i.name)
        foodList.append({"name":i.name, "image":i.image, "stars":i.stars, "id":i.id})
        count+=1
        if count > 103:
            break

popfoodList =[]
for x in FoodItem.query.all():
    if x.stars == '5 of 5 stars' and x.image != 'No Image':
        popfoodList.append({"name":x.name, "image":x.image, "stars":x.stars, "id":x.id})

repOfDay=[{"name":FoodItem.query.get(500).name, 
            "image":FoodItem.query.get(500).image, 
            "stars":FoodItem.query.get(500).stars, 
            "id":FoodItem.query.get(500).id,
            "time":FoodItem.query.get(500).time},


          {"name":FoodItem.query.get(950).name, 
          "image":FoodItem.query.get(950).image, 
          "stars":FoodItem.query.get(950).stars, 
          "id":FoodItem.query.get(950).id,
          "time":FoodItem.query.get(950).time}]




@app.route('/home', methods=['GET','POST'])
def index():
    return render_template('index.html', log_html = "Recipes", foodList=foodList, repOfDay =repOfDay)


@app.route('/popularRecipes')
def PopularPage():    
    return render_template('PopularPage.html', Popular_Page='Popular Recipes', title='Popular Foods', popfoodList=popfoodList)
    
@app.route('/register', methods=['GET','POST'])
def Register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('Login'))        
    return render_template('register.html', title="Register", form=form)

@app.route('/login', methods=['GET','POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            print(str(current_user.email))
            flash('You have been logged in!','success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')   
    return render_template('login.html', title="Login", form=form)

@app.route('/recipe/<id>', methods=['GET','POST'])
def RecipeFile(id):
    flag = False
    recipefile = FoodItem.query.filter_by(id=id).first()
    allComments = FoodComments.query.filter_by(foodId=id).all()
    if current_user.is_authenticated:
        saved = UserFoods.query.filter(and_(UserFoods.userId==current_user.email, UserFoods.foodId==id)).first()
        if saved:
            flag = True
            print(flag)
    if request.method =='POST' and request.form['comment_content']:      
        comment = request.form['comment_content']
        if comment:
            newComment = FoodComments(userId=current_user.email,foodId=recipefile.id,post=comment)
            db.session.add(newComment)
            db.session.commit()
            print(FoodComments) 
        return redirect(url_for('RecipeFile',id=recipefile.id))
    return render_template('recipeProfile.html', recipefile=recipefile, title=recipefile.name, allComments=allComments, flag=flag)

@app.route('/logout')
def logout():
    print(str(current_user.email))
    logout_user()
    return redirect(url_for('index'))


@app.route('/account')
@login_required
def Account():
   return render_template('account.html', title="Acount")

@app.route('/foryou')
@login_required
def ForYou():
    userSavedFoods= current_user.userSavedFoods
    savedList=[]
    for x in userSavedFoods:
        savedList.append(FoodItem.query.get(x.foodId))
    return render_template('foryou.html', title="Acount", savedList=savedList)

@app.route('/')
@app.route('/search', methods=['GET','POST'])
def Search():
    if request.method =='POST' and request.form['query'] is not None:
        query = request.form['query']
        if query:
            return redirect(url_for('SearchWithQuery',query=query))

        query_spage = request.form['query_spage']
        if query_spage:
            return redirect(url_for('SearchWithQuery',query=query_spage))
    if current_user.is_authenticated:
        userSavedFoods= current_user.userSavedFoods
        savedList=[]
        savedListSize = len(savedList)
        for x in userSavedFoods:
            savedList.append(FoodItem.query.get(x.foodId))
        return render_template('search.html', title="Search", savedList=savedList, savedListSize=savedListSize)
    return render_template('search.html', title="Search")

    

@app.route('/search/<query>', methods=['GET','POST'])
def SearchWithQuery(query):
    matchedFoods = FoodItem.query.filter(or_(FoodItem.ingredients.like('%'+query+'%'),FoodItem.tags.like('%'+query+'%'),FoodItem.name.like('%'+query+'%'))).all()
    return render_template('searchWithQuery.html', title=query, matchedFoods=matchedFoods)
    

@app.route('/recipeSaved/<id>', methods=['GET','POST'])
@login_required
def SaveRecipe(id):
    recipefile = FoodItem.query.filter_by(id=id).first()
    if request.method == 'POST':
        saved = UserFoods.query.filter(and_(UserFoods.userId==current_user.email, UserFoods.foodId==id)).first()
        if saved is None:
            savedRep = UserFoods(userId=current_user.email,foodId=recipefile.id)
            flash('Recipe Saved','success')
            db.session.add(savedRep)
            db.session.commit()
            print(UserFoods.query.all())
            return redirect(url_for('RecipeFile',id=recipefile.id))
        else:
            flash('Recipe is already saved','danger')

    return redirect(url_for('RecipeFile',id=recipefile.id))

@app.route('/recipeDelete/<id>', methods=['GET','POST'])
@login_required
def DeleteRecipe(id):
    recipefile = FoodItem.query.filter_by(id=id).first()
    if request.method == 'POST':
        saved = UserFoods.query.filter(and_(UserFoods.userId==current_user.email, UserFoods.foodId==id)).first()
        db.session.delete(saved)
        db.session.commit()
        flash('Recipe deleted','success')
        return redirect(url_for('RecipeFile',id=recipefile.id))
    else:
        flash('Recipe is already saved','danger')

    return redirect(url_for('RecipeFile',id=recipefile.id))
