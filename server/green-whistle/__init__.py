from flask import Flask, request, jsonify, send_from_directory, make_response
import pyproj
import requests as rq
import re
import json


def create_app():
    # create and configure the app
    app = Flask(__name__, static_url_path='/static')

    @app.route('/')
    def root():
        return app.send_static_file('index.html')

    @app.route('/hello')
    def hello():
        return 'Hello.'

    @app.route('/src/<path:path>')
    def send_js(path):
        return send_from_directory('src', path)

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

    def to_geojson(tree, layer):
        status = {
            'dane_wawa.BOS_ZIELEN_WNIOSEK': 'request',
            'dane_wawa.BOS_ZIELEN_ZGODA': 'accepted',
            'dane_wawa.BOS_ZIELEN_NASADZENIE_POZ': 'replacement',
            'dane_wawa.BOS_ZIELEN_NASADZENIE_ZAST': 'replacement',
        }[layer]
        tree_feature = {
            "type": "Feature",
            "properties": {
                "name": tree['name'],
                "status": status,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [tree['x'], tree['y']]
            }
        }
        return tree_feature

    # example: http://127.0.0.1:5000/trees.json?bb=52.205324323965435,20.97427896707837,52.21105683036724,20.98185675745256
    @app.route('/trees.json')
    def get_trees():
        # consume the bounding box
        bb = [float(x) for x in request.args.get('bb').split(',')]
        assert len(bb) == 4, 'expected bounding box as 4 numbers'

        # convert bb to P2000
        bb = to_p2000(*bb[:2][::-1]) + to_p2000(*bb[2:][::-1])
        bb = ':'.join(['%.8f' % x for x in bb])

        # fetch data from city API
        def _fetch_trees(layer):
            p = {
                'request': 'getfoi',
                'version': '1.0',
                'bbox': bb,
                'width': 491,
                'height': 604,
                'theme': layer,
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
            trees = json.loads(re.sub(r'([,{[])(\w+):', r'\1"\2":', ans))['foiarray']

            # convert bb to WGS84
            def _conv(t):
                lat, lon = to_wgs84(t['x'], t['y'])
                t.update({'x': lat, 'y': lon})
                return t
            trees = [_conv(t) for t in trees]

            # convert to geojson
            trees = [to_geojson(t, layer) for t in trees]

            return trees

        trees = sum([_fetch_trees(l) for l in [
            'dane_wawa.BOS_ZIELEN_WNIOSEK',
            'dane_wawa.BOS_ZIELEN_ZGODA',
            'dane_wawa.BOS_ZIELEN_NASADZENIE_POZ',
            'dane_wawa.BOS_ZIELEN_NASADZENIE_ZAST',
        ]], [])

        # CORS
        resp = make_response(jsonify(trees))
        h = resp.headers
        h['Access-Control-Allow-Origin'] = '*'
        return resp

    return app
