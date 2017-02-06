from flask import Flask, render_template, request, redirect
import pandas as pd
import numpy as np
from scripts import sf

app = Flask(__name__)
app.vars = {}

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template(
            'index.html')
    
    else:  
        app.vars['lat'] = float(request.form['lat'])
        app.vars['long'] = float(request.form['long'])
        return redirect('/recommendation')
    
@app.route('/recommendation', methods=['GET'])
def recommendation():
        
        to_gmap = sf.recommendation_coor(app.vars['lat'], app.vars['long'])

        return render_template(
            'recommendation.html',
            to_gmap=to_gmap
        )
if __name__ == '__main__':
    #debug = True
    app.run()
#host='104.131.67.119'