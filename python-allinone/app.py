# Program: app.py
# Purpose: Default URI context for Web app
# Author:  Ray Lai
# Updated: Jul 10, 2017
# License: MIT
#
from flask import Flask
app = Flask(__name__)
xPort = 5000

#
# Default URI context / 
#
@app.route('/')
def launchWebContainer():
    return 'Web application v1.0'

# 
# main
#
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=xPort)
