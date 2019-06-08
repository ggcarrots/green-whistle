from flask import Flask, request, jsonify
import pyproj
import requests as rq
import re
import json


def create_app():
    # create and configure the app
    app = Flask(__name__)

    @app.route('/hello')
    def hello():
        return 'Hello.'

    # original projection: ETRS89 / Poland CS2000 zone 7
    # https://github.com/kjordahl/pyproj/blob/master/lib/pyproj/data/epsg
    proj_wgs84 = pyproj.Proj(init='epsg:4326')
    proj_p2000 = pyproj.Proj("+proj=tmerc +lat_0=0 +lon_0=21 +k=0.999923 +x_0=7500000 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs")

    def to_wgs84(*coords2000):
        return pyproj.transform(proj_p2000, proj_wgs84, *coords2000)

    def to_p2000(*coords84):
        return pyproj.transform(proj_wgs84, proj_p2000, *coords84)

    @app.route('/wgs84')
    def get_wgs84():
        coords = float(request.args.get('lng')), float(request.args.get('lat'))
        return jsonify(to_wgs84(*coords))

    @app.route('/p2000')
    def get_p2000():
        coords = float(request.args.get('lng')), float(request.args.get('lat'))
        return jsonify(to_p2000(*coords))

    @app.route('/trees.json')
    def get_trees():
        # consume the bounding box
        bb = [float(x) for x in request.args.get('bb').split(',')]
        assert len(bb) == 4, 'expected bounding box as 4 numbers'

        # convert bb to P2000
        bb = to_p2000(*bb[:2]) + to_p2000(*bb[2:])

        # fetch data from city API
        p = {
            'request': 'getfoi',
            'version': '1.0',
            'bbox': ':'.join(['.8f' % x for x in bb]),
            'width': 491,
            'height': 604,
            # 'theme': 'dane_wawa.BOS_ZIELEN_WNIOSEK',
            'theme': 'dane_wawa.BOS_ZIELEN_ZGODA',
            # 'theme': 'dane_wawa.BOS_ZIELEN_NASADZENIE_POZ',
            # 'theme': 'dane_wawa.BOS_ZIELEN_NASADZENIE_ZAST',
            'clickable': 'yes',
            'area': 'yes',
            'dstsrid': '2178',
            'cachefoi': 'yes',
            'tid': '686_489998',
            'aw': 'no'
        }
        r = rq.post('http://mapa.um.warszawa.pl/mapviewer/foi', data=p)
        assert r.ok, 'failed to fetch data from the city'
        ans = r.text

        # decode the response
        trees = json.loads(re.sub(r'([,{[])(\w+):', r'\1"\2":', ans))

        # convert bb to WGS84

        return jsonify(trees)

    return app
