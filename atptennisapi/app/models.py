from app import db


class Player(db.Model):
    
    __tablename__ = "player"
    __table_args__ = {"schema":"atptennis"}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    country_code = db.Column(db.String)

    def __repr__(self):
        return '<Player {}>'.format(self.id)


class Tournament(db.Model):

    __tablename__ = "tournament"
    __table_args__ = {"schema":"atptennis"}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Tournament {}>'.format(self.name)


class Entrant(db.Model):

    __tablename__ = "entrant"
    __table_args__ = {"schema":"atptennis"}

    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('atptennis.tournament.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('atptennis.player.id'))
    player_seed = db.Column(db.Integer)
    player_result = db.Column(db.Integer)

    def __repr__(self):
        return '<Entrant {}>'.format(self.id)


class Matchup(db.Model):

    __tablename__ = "matchup"
    __table_args__ = {"schema":"atptennis"}

    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('atptennis.tournament.id'))
    player1_id = db.Column(db.Integer, db.ForeignKey('atptennis.player.id'))
    player2_id = db.Column(db.Integer, db.ForeignKey('atptennis.player.id'))
    round_num = db.Column(db.Integer)
    winner_id = db.Column(db.Integer, db.ForeignKey('atptennis.player.id'))

    def __repr__(self):
        return '<Matchup {}>'.format(self.matchup)