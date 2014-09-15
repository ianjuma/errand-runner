#! /usr/bin/env python
# -*- coding: utf-8 -*-

# res/ rep cycle
from app import app

from flask import (render_template, request, redirect)
from flask import make_response
from flask import jsonify


@app.route('/')
def index():
    if 'username' in request.cookies:
        return redirect('/task/myTasks/')

    return render_template('index.html')


@app.route('/robots.txt')
def robots():
    return render_template('robots.txt')


# Basic Error handlers
@app.errorhandler(404)
def resource_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(400)
def bad_request(e):
    return make_response(jsonify({"Error 400":
                                  "Bad request"}), 400)


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


@app.errorhandler(408)
def timeout(e):
    return make_response(jsonify({"Error 408":
                                  "Request Timeout"}), 408)


@app.errorhandler(405)
def invalidMethod(e):
    return make_response(jsonify({"Error 405":
                                  "Invalid Request Method"}), 405)


@app.errorhandler(410)
def gone(e):
    return make_response(jsonify({"Error 410":
                                  "Resource is Gone"}), 410)
