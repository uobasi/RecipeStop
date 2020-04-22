



from recipeWeb import app

if __name__ == '__main__':
    app.debug = True
    ip = '127.0.0.1'
    
    app.run(host=ip)