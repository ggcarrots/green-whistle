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

    @app.route('/wgs84')
    def get_wgs84():
        # request.args.get('user')
        return 'not supported yet'

    @app.route('/trees.json')
    def get_trees():
        # consume the bounding box
        bb = [float(x) for x in request.args.get('bb').split(',')]
        assert len(bb) == 4, 'expected bounding box as 4 numbers'

        # fetch data from city API
        p = {
            'request': 'getfoi',
            'version': '1.0',
            'bbox': '7498108.517198522:5785744.619496521:7498626.680139457:5786382.277156488',
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

        return jsonify(trees)

    return app
