from flask import Flask, render_template, request, redirect
from flask_googlemaps import GoogleMaps
import pandas as pd
from collections import defaultdict

app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = "AIzaSyAZrVQ1H1eTGMz_xt8cFuU4JPj3OY-7E9s"
GoogleMaps(app)

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    
    else:  
        #read data for sf and nyc
        sfdfc = pd.read_csv('data/sfdfc.csv', index_col = 0)
        nydfc = pd.read_csv('data/nydfc.csv', index_col = 0)
        #get coordinates
        sflat = request.args.get('lat')
        sflong = request.args.get('long')
        sf_distance = defaultdict(int)
        ny_rec = defaultdict(int)
        for i in range(len(sfdfc)):
            sf_distance[i] = np.sqrt((sflat - sfdfc['INTPTLAT'][i])**2 + (sflong - sfdfc['INTPTLONG                                                                                                                  '][i])**2)
        for index, v in sf_distance.iteritems():
            if v == min(sf_distance.values()):
                j = index
        #how many recommendation you want?
        n = 20
        sf_l = sfdfc['liquordensereal'][j:j+1].values[0]
        sf_p = sfdfc['popdensereal'][j:j+1].values[0]
        sf_h = sfdfc['housedensereal'][j:j+1].values[0]
        for q in range(len(nydfc)):
            ny_rec[q] = (np.sqrt((sf_l - nydfc['liquordensereal'][q])**2)
                         + np.sqrt((sf_p - nydfc['popdensereal'][q])**2) +
                        np.sqrt((sf_h - nydfc['housedensereal'][q])**2))
        res = sorted(ny_rec.items(), key = lambda x:x[1])
        res_coor = []
        for c in range(n):
            index = res[:n][c][0]
            lat = nydfc['INTPTLAT'][index]
            lon = nydfc['INTPTLONG                                                                                                                  '][index]
            if lat < 40.89 and lon > -74.049835 and lon < -73.81:
                co = (lat, lon)
                res_coor.append(co)
        return render_template('test.html', rec = res_coor)

if __name__ == '__main__':
    debug = True
    app.run(host='104.131.67.119')
