from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


def clsTournament(Base):
    class Tournament(Base):
        __tablename__ = "tournament"
        __table_args__ = {"schema": "atptennis"}
        id = Column(Integer, primary_key=True)
        name = Column(String)
        start_date = Column(DateTime)
        end_date = Column(DateTime)
    return Tournament


def clsPlayer(Base):
    class Player(Base):
        __tablename__ = "player"
        __table_args__ = {"schema": "atptennis"}
        id = Column(Integer, primary_key=True)
        name = Column(String)
        country_code = Column(String)
    return Player


def clsEntrant(Base):
    class Entrant(Base):
        __tablename__ = "entrant"
        __table_args__ = {"schema": "atptennis"}
        id = Column(Integer, primary_key=True)
        tournament_id = Column(Integer, ForeignKey('atptennis.tournament.id'))
        player_id = Column(Integer, ForeignKey('atptennis.player.id'))
        player_seed = Column(Integer)
        player_result = Column(Integer)
    return Entrant


def clsMatchup(Base):
    class Matchup(Base):
        __tablename__ = "matchup"
        __table_args__ = {"schema": "atptennis"}
        id = Column(Integer, primary_key=True)
        tournament_id = Column(Integer, ForeignKey('atptennis.tournament.id'))
        player1_id = Column(Integer, ForeignKey('atptennis.player.id'))
        player2_id = Column(Integer, ForeignKey('atptennis.player.id'))
        round_num = Column(Integer)
        winner_id = Column(Integer, ForeignKey('atptennis.player.id'))
    return Matchup


def clsDrawParseHistory(Base):
    class DrawParseHistory(Base):
        __tablename__ = "drawparsehistory"
        __table_args__ = {"schema": "atptennis"}
        id = Column(Integer, primary_key=True)
        tournament_title = Column(String)
        tournament_link = Column(String)
        tournament_year = Column(Integer)
        tournament_start_date = Column(DateTime)
        last_update = Column(DateTime)
    return DrawParseHistory


def clsArchiveParseHistory(Base):
    class ArchiveParseHistory(Base):
        __tablename__ = "archiveparsehistory"
        __table_args__ = {"schema": "atptennis"}
        id = Column(Integer, primary_key=True)
        archive_year = Column(Integer)
        last_update = Column(DateTime)
    return ArchiveParseHistory
