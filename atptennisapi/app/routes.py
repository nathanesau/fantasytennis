from app import app, db

from flask import request, abort, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import cross_origin
from app.models import Player, Tournament, Entrant, Matchup
from datetime import datetime, timedelta
from hashlib import md5
import os
import redis
import json
import shutil


@app.route('/')
@cross_origin()
def index():
    return "Hello, World"

@app.route('/api/v1/players')
@cross_origin()
def get_players():
    players = Player.query.all()
    return jsonify(players=[{"id": i.id, "name": i.name, 
        "country_code": i.country_code } for i in players])


@app.route('/api/v1/tournaments')
@cross_origin()
def get_tournaments():
    tournaments = Tournament.query.all()
    return jsonify(tournaments=[{"id": i.id, "name": i.name,
        "start_date": i.start_date, "end_date": i.end_date }
        for i in tournaments])
