from app import app, db

from flask import request, abort, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import cross_origin
from app.models import Player, Tournament, Entrant, Matchup, DrawParseHistory
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


@app.route('/players')
@cross_origin()
def get_players():
    players = Player.query.all()
    return jsonify([{"id": i.id, "name": i.name,
                     "country": i.country_code} for i in players if i.name != 'bye']), 200


@app.route('/player')
@cross_origin()
def get_player():
    player = Player.query.filter_by(id=request.args.get("id")).first()
    return jsonify({"id": player.id, "name": player.name,
                    "country": player.country_code}), 200


@app.route('/tournaments')
@cross_origin()
def get_tournaments():
    tournaments = Tournament.query.all()
    return jsonify([{"id": i.id, "name": i.name,
                     "start": i.start_date, "end": i.end_date}
                    for i in tournaments]), 200


@app.route('/tournament')
@cross_origin()
def get_tournament():
    tournament = Tournament.query.filter_by(id=request.args.get("id")).first()
    return jsonify({"id": tournament.id, "name": tournament.name,
                    "start": tournament.start_date, "end": tournament.end_date}), 200


@app.route('/matchups')
@cross_origin()
def get_matchups():
    tournament_name = request.args.get("tournament_name")
    tournament_start_date = datetime.strptime(request.args.get("tournament_start_date"),
                                              '%a, %d %b %Y %H:%M:%S %Z')

    tournament = Tournament.query.filter_by(name=tournament_name,
                                            start_date=tournament_start_date).first()

    if tournament is None:
        abort(400)

    matchups = Matchup.query.filter_by(tournament_id=tournament.id)

    matchups_list = []
    for matchup in matchups:
        player1 = Player.query.filter_by(id=matchup.player1_id).first().name
        player2 = Player.query.filter_by(id=matchup.player2_id).first().name
        winner = Player.query.filter_by(id=matchup.winner_id).first().name
        matchups_list.append({"player1": player1, "player2": player2,
                              "round": matchup.round_num, "winner": winner})

    return jsonify(matchups_list), 200
