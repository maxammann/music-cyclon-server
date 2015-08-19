import random
import json

from flask import Flask, url_for, send_file, request
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from beets import Library

app = Flask(__name__)


@app.route("/get", methods=['POST'])
def get():
    return send_file("/media/music/library/" + request.get_data(cache=False))


@app.route("/random/<int:max_size>")
def random_list(max_size):
    max_size *= 1000000

    app.logger.info("Collecting music items...")
    objs = list(library.albums())

    app.logger.info("Selecting random items...")
    result = []

    size = 0

    while size < max_size:
        rnd = objs[random.randint(0, len(objs) - 1)]
        for item in rnd.items():
            size += item.try_filesize()
            result.append(item)

    app.logger.info("Returning paths...")
    paths = [path.destination(fragment=True) for path in result]
    return json.dumps(paths, ensure_ascii=False).encode("utf-8")


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():

        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint)
            links.append(url)

    return str(links)


def run():
    global library
    library = Library("/media/data/music/library.db", "/media/music/library/")

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()
