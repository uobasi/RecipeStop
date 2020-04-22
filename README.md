Create a local folder

Create a virtual environment:

py -m venv env
You need to activate the virtual environment when you want to use it:

env\Scripts\activate
To fufil all the requirements for the python server, you need to run:

pip3 install -r requirements.txt
Because we are now inside a virtual environment. We do not need sudo.

before starting make sure v1.csv file in local folder because it holds
recipe data

local Folder
  recipeWeb Folder
      static folder
      templates folder
      __init__.py
      form.py
      models.py
      .... 
  requirements.txt
  run.py
  v1.csv

Then you can start the server with:

python3 run.py
