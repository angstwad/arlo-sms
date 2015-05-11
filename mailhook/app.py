# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from rq import Queue
from flask import Flask
from redis import Redis
from flask import request
from flask.ext.restful import Api, abort
from flask.ext.restful import Resource

from config import config
from jobs import send_picture


redis_conn = Redis(config.REDIS_HOST)
queue = Queue(connection=redis_conn)


class HookResource(Resource):
    def post(self, request_path):
        if request_path != 'arlo':
            abort(404)
        req_body_html = request.form.get('body-html', '')
        if not req_body_html:
            abort(400)
        soup = BeautifulSoup(req_body_html)
        img_url = soup.img.get('src')
        for recipient in config.RECIPIENTS:
            queue.enqueue(send_picture, recipient, img_url)
        return {'message': 'ok'}


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(HookResource, '/<path:request_path>')
    return app
