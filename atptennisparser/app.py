from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from config import Config
import math
from pathlib import Path
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime as dt
from datetime import timedelta
from timeout import timeout
import logging
from logging.handlers import RotatingFileHandler
from models import clsTournament, clsPlayer, clsEntrant, clsMatchup, \
        clsDrawParseHistory, clsArchiveParseHistory


def get_logger():

    # create logger
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)

    return logger


def download_archive(archive_year):
    """
    download archive for provided year
    - this HTML file contains the list of tournaments
    - return the filename
    """
    archive_url = "{}?year={}".format(Config.ARCHIVE_URL, archive_year)
    archive_filename = "{}/archive/{}.html".format(Config.DATA_FOLDER,
        archive_year)
    request = Request(url=archive_url, headers=Config.HEADERS)
    html = urlopen(request).read()

    # create folder if it does not exist
    archive_folder = Path(r'{}'.format(archive_filename))
    os.makedirs(str(archive_folder.parent), exist_ok=True)

    # write html content to file
    html_file = open(archive_filename, "w")
    html_file.write(html.decode("utf-8"))
    html_file.close()

    return archive_filename


def parse_archive(archive_filename):
    """"
    extract tournament information from archive
    - return the archive data [{'title', 'link', 'start_date'}]
    """
    soup = BeautifulSoup(open(archive_filename), "html.parser")

    def strip(title_tag):
        title = str(title_tag.contents)
        for substr in ["  ", '\\n', '\\', '[', ']', '\'', '\"']:
            title = title.replace(substr, '')
        return title

    archive_data = []

    for tourney in soup.find_all('tr', {'class': 'tourney-result'}):
        try: # this parsing method works for 2019, 2018, ...
            title_tag = tourney.find_all('span', {'class': 'tourney-title'})
            title = strip(title_tag[0])
            dates_tag = tourney.find_all('span', {'class': 'tourney-dates'})
            start_date = strip(dates_tag[0]).strip()
            links = tourney.find_all('a')
            for link in links: # only some links are relevant
                href = None if 'href' not in link.attrs else link['href']
                if href is not None and "singles" in href:
                    archive_data.append({"title": title, "link": href, "start_date": start_date})
        except: # this parsing method works for 2020
            title_tag = tourney.find_next('a')
            title = strip(title_tag)
            dates_tag = tourney.find_all('span', {'class': 'tourney-dates'})
            start_date = strip(dates_tag[0]).strip()
            links = tourney.find_all('a')
            for link in links: # only some links are relevant
                href = None if 'href' not in link.attrs else link['href']
                if href is not None and "singles" in href:
                    archive_data.append({"title": title, "link": href, "start_date": start_date})
        
    return archive_data
            

def download_draw(draw_info):
    """
    download draw information from archive
    - return the draw data
    """
    title, link, year = draw_info.get("title").replace(' ', '_'), draw_info.get("link"), \
        draw_info.get("year")
    draw_url = "{}{}".format(Config.BASE_URL, link)
    draw_filename = "{}/draw/{}/{}.html".format(Config.DATA_FOLDER,
        year, title)
    request = Request(url=draw_url, headers=Config.HEADERS)
    html = urlopen(request).read()

    # create folder if it does not exist
    draw_folder = Path(r'{}'.format(draw_filename))
    os.makedirs(str(draw_folder.parent), exist_ok=True)

    # write html content to file
    html_file = open(draw_filename, "w")
    html_file.write(html.decode("utf-8"))
    html_file.close()

    return draw_filename


def parse_first_round_entry(box, info):
    tr_tags = box.find_all('tr')
    for tr_tag in tr_tags:
        span_tags = tr_tag.find_all('span')
        a_tags = tr_tag.find_all('a')
        if len(a_tags) > 0: # player info exists
            player_name = a_tags[0]['data-ga-label']
            img_tags = tr_tag.find_all('img')
            if len(img_tags) > 0:
                player_country = img_tags[0]['src']
                info["country_map"][player_name] = player_country
            info["entrants"].append(player_name)
        else:
            player_name = "bye"
            player_country = ""
            info["country_map"][player_name] = player_country
            info["entrants"].append(player_name)
        if len(span_tags) > 0:
            seed = span_tags[0]
            if seed:
                seed_str = str(seed).strip()
                for substr in ['\n', '\t', '<', '>', 'span', '\\', '/', '(', ')']:
                    seed_str = seed_str.replace(substr, '')
                info["seed_map"] = seed_str


def parse_next_round_entry(box, info):
    a_tags = box.find_all('a')
    if len(a_tags) > 0: # only true if match has happened
        player_name = a_tags[0]['data-ga-label']
        info["win_players"].append(player_name)
    else:
        player_name = "unknown"
        info["win_players"].append(player_name)


def get_rounds(info, num_rounds, draw_size):

    def get_winner(players, round_num, wins_map):
        player1, player2 = players
        wins1, wins2 = [0 if i not in wins_map else wins_map[i] for i in players]
        return player1 if wins1 >= round_num else player2 if wins2 >= round_num else "unknown"

    wins_map = dict((player, info["win_players"].count(player))
        for player in info["entrants"])

    rounds = [[] for i in range(num_rounds)]
    remain_draw_size = draw_size
    for round_num in range(0, num_rounds, 1):
        if round_num == 0:  # round 1
            for i in range(0, remain_draw_size, 2):
                rounds[0].append((info["entrants"][i], info["entrants"][i + 1]))
        else: # round 2, ...
            if remain_draw_size == 1: # last round
                winner = get_winner(rounds[round_num - 1][0], round_num, wins_map)
                rounds[round_num].append((winner))
                break
            for i in range(0, remain_draw_size, 2):
                winner1 = get_winner(rounds[round_num - 1][i], round_num, wins_map)
                winner2 = get_winner(rounds[round_num - 1][i + 1], round_num, wins_map)
                rounds[round_num].append((winner1, winner2))
        remain_draw_size = int(remain_draw_size / 2)

    return rounds


def get_matchups(rounds):
    
    num_rounds = len(rounds)

    def find_winner(player1, player2, round_num):
        if round_num == num_rounds - 1:
            return None # last round, don't look for winner
        
        if round_num == num_rounds - 2:
            return rounds[round_num + 1][0]
        
        for matchup in rounds[round_num + 1]:
            if player1 in matchup[0] or player1 in matchup[1]:
                return player1
            elif player2 in matchup[0] or player2 in matchup[1]:
                return player2

        return None

    matchup_list = []

    for round_num in range(0, num_rounds, 1):
        if round_num == num_rounds - 1: # final round
            player1, player2 = rounds[round_num][0], ""
            winner = None
            matchup = {"round": round_num + 1, "player1": player1,
                "player2": player2, "winner": winner}
            matchup_list.append(matchup)
            break
        for i in range(0, len(rounds[round_num]), 1):
            player1, player2 = rounds[round_num][i]
            winner = find_winner(player1, player2, round_num)
            matchup = {"round": round_num + 1, "player1": player1,
                "player2": player2, "winner": winner}
            matchup_list.append(matchup)

    return matchup_list


def get_player_results(matchups, num_rounds):

    player_results = {}

    player_final_round = {}
    for matchup in matchups:
        round_num = matchup["round"]
        player1, player2 = matchup["player1"], matchup["player2"]
        player_final_round[player1] = round_num
        player_final_round[player2] = round_num

    # let X = final round, N = num rounds, x = N - X + 1
    # then result = 2 ** (x-1) + 1
    for player, round_num in player_final_round.items():
        x = num_rounds - round_num
        result = 1 if x == 0 else 2 ** (x-1) + 1
        player_results[player] = result

    return player_results


def get_players(info, player_results):

    players = []

    for player in info["entrants"]:
        seed = "0" if player not in info["seed_map"] else info["seed_map"][player]
        seed = seed.strip()
        country_icon = "" if player not in info["country_map"] else info["country_map"][player]
        country_code = country_icon[-7:].replace(".svg", "")
        players.append({"name": player, "seed": seed, "country_code": country_code,
            "result": player_results[player]})

    return players


def parse_draw(draw_filename):
    """"
    extract matchup information from draw
    - return the draw data
    """
    soup = BeautifulSoup(open(draw_filename), "html.parser")

    draw_data = {"dates": {}, "matchups": [], "players": []}

    # store details in map
    info = {"entrants": [], "win_players": [],  "country_map": {},  "seed_map": {}}
    for box in soup.find_all('div', {'class': 'scores-draw-entry-box'}):
        table_tags = box.find_all('table')
        if len(table_tags) > 0: # round 1 entry
            parse_first_round_entry(box, info)
        else: # round 2, ..., entry
            parse_next_round_entry(box, info)

    draw_size = len(info["entrants"])
    if draw_size not in [8,16,32,64,128]:
        print("could not parse draw (invalid num of entrants)")
        return # parser not programmed to handle this case

    num_rounds = int(math.log(draw_size) / math.log(2)) + 1
    if num_rounds > 8:
        print("could not parse draw (too many rounds)")
        return # parser not programmed to handle this case

    # dates
    date_tag = soup.find_all('span', {'class': 'tourney-dates'})[0]
    dates = date_tag.text.strip().replace('\n', '').replace(' - ', ' ').split(' ')
    draw_data["dates"] = dates

    # matchups
    rounds = get_rounds(info, num_rounds, draw_size)
    matchups = get_matchups(rounds)
    draw_data["matchups"] = matchups

    # players
    player_results = get_player_results(matchups, num_rounds)
    players = get_players(info, player_results)
    draw_data["players"] = players

    return draw_data


def write_archive_to_db(archive_data, archive_info):
    """
    write archive to db (archive_data from parse_archive)
    """
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
    Base = declarative_base()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()

    ArchiveParseHistoryCls = clsArchiveParseHistory(Base)
    DrawParseHistoryCls = clsDrawParseHistory(Base)

    # archiveparsehistory
    aphquery = session.query(ArchiveParseHistoryCls)
    new_archive = aphquery.filter_by(archive_year=archive_info["year"]).first() is None
    ongoing_archive = dt.now().year == archive_info["year"]

    if new_archive: # first time writing data for this archive
        session.bulk_save_objects([ArchiveParseHistoryCls(archive_year=archive_info["year"],
            last_update=dt.now())])
    elif ongoing_archive: # update last_update column
        row = aphquery.filter_by(archive_year=archive_info["year"]).first()
        if row is not None:
            row.last_update = dt.now()

    # drawparsehistory
    dphquery = session.query(DrawParseHistoryCls)

    if new_archive or ongoing_archive: # first time writing data for this archive
        objects = []
        for tinfo in archive_data:
            df = '%Y.%m.%d'
            start = tinfo["start_date"]
            title, link, tdate = tinfo["title"], tinfo["link"], dt.strptime(start, df)
            if dphquery.filter_by(tournament_title=title, tournament_start_date=tdate).first() is None:
                # first time processing this tournament
                objects.append(DrawParseHistoryCls(tournament_title=title, tournament_link=link,
                    tournament_year=archive_info["year"], tournament_start_date=tdate))
        
        if objects:
            session.bulk_save_objects(objects)
    
    session.commit()


def write_draw_to_db(draw_data, draw_info):
    """
    write draw to db (draw_data from parse_draw)
    """
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
    Base = declarative_base()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()

    TournamentCls = clsTournament(Base)
    PlayerCls = clsPlayer(Base)
    EntrantCls = clsEntrant(Base)
    MatchupCls = clsMatchup(Base)

    # tournaments
    tquery = session.query(TournamentCls)

    df = '%Y.%m.%d'
    start, end = draw_data["dates"][0], draw_data["dates"][1]
    tname, tstart, tend = draw_info["title"], dt.strptime(start, df), dt.strptime(end, df)
    new_tournament = tquery.filter_by(name=tname, start_date=tstart, end_date=tend).first() is None
    ongoing_tournament = tstart < dt.now() and tend >= dt.now()
    
    if new_tournament:
        session.bulk_save_objects([TournamentCls(name=tname, start_date=tstart, end_date=tend)])

    # players
    pquery = session.query(PlayerCls)

    if new_tournament: # first time writing data for this tourney
        players = []
        for player in draw_data["players"]:
            name, country_code = player["name"], player["country_code"]
            if pquery.filter_by(name=name).first() is None:
                players = [PlayerCls(name=name, country_code=country_code)]
                session.bulk_save_objects(players)
    # entrants
    equery = session.query(EntrantCls)

    if new_tournament: # first time writing data for this tourney
        tid = tquery.filter_by(name=tname, start_date=tstart, end_date=tend).first().id
        entrants = []
        for player in draw_data["players"]:
            pname, presult, pseed = player["name"], player["result"], player["seed"]
            pid = pquery.filter_by(name=pname).first().id
            if equery.filter_by(tournament_id=tid, player_id=pid).first() is None:
                entrants.append(EntrantCls(tournament_id=tid, player_id=pid, player_seed=pseed,
                    player_result=presult))

        if entrants:
            session.bulk_save_objects(entrants)

    # matchups
    mquery = session.query(MatchupCls)

    if new_tournament or ongoing_tournament: # first time writing or ongoing tourney
        tid = tquery.filter_by(name=tname, start_date=tstart, end_date=tend).first().id
        matchups = []
        for matchup in draw_data["matchups"]:
            n1, n2 = matchup["player1"], matchup["player2"]
            winner = matchup["winner"]
            if not (n1 and n2): # exclude matchup if player name missing
                continue
            if not winner: # match was never completed
                continue
            if n1 == "unknown" or n2 == "unknown": # bracket was never completed
                continue
            id1, id2 = pquery.filter_by(name=n1).first().id, pquery.filter_by(name=n2).first().id
            round_num = matchup["round"]
            winner = matchup["winner"]
            wid = pquery.filter_by(name=winner).first().id
            if mquery.filter_by(tournament_id=tid, player1_id=id1, player2_id=id2).first() is None:
                matchups.append(MatchupCls(tournament_id=tid, player1_id=id1, player2_id=id2,
                    round_num=round_num, winner_id=wid))

        if matchups:
            session.bulk_save_objects(matchups)

    session.commit()


def update_drawhistory_db(draw_info):
    """
    update last_update column for drawparsehistory
    """
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
    Base = declarative_base()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()

    DrawParseHistoryCls = clsDrawParseHistory(Base)

    # drawparsehistory
    dphquery = session.query(DrawParseHistoryCls)

    row = dphquery.filter_by(tournament_title=draw_info["title"],
        tournament_year=draw_info["year"]).first()

    if row is not None:
        row.last_update = dt.now()
        session.commit()


@timeout(1000)
def update_db():
    """
    dynamic update for db based on parsehistory and current date
    """
    logger = get_logger()

    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
    Base = declarative_base()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()

    ArchiveParseHistoryCls = clsArchiveParseHistory(Base)
    DrawParseHistoryCls = clsDrawParseHistory(Base)

    # archiveparsehistory
    aphquery = session.query(ArchiveParseHistoryCls)

    for archive_year in range(Config.MIN_YEAR, dt.now().year + 1, 1):

        if aphquery.filter_by(archive_year=archive_year).first() is None: # new archive
            archive_filename = download_archive(archive_year)
            archive_data = parse_archive(archive_filename)
            write_archive_to_db(archive_data, {"year": archive_year})
        elif dt.now().year == archive_year: # ongoing archive
                archive_filename = download_archive(archive_year)
                archive_data = parse_archive(archive_filename)
                write_archive_to_db(archive_data, {"year": archive_year})

    # drawparsehistory
    dphquery = session.query(DrawParseHistoryCls)

    for row in dphquery.all():
        draw_info = None
        if row.last_update is None: # first time parsing this draw
            draw_info = {'title': row.tournament_title,
                'link': row.tournament_link, 'year': row.tournament_year}
        else: # check if tournament may be in progress
            start_date = row.tournament_start_date
            end_date = start_date + timedelta(days=21) # hypothetical end date
            if dt.now() > start_date and dt.now() < end_date: # ongoing
                draw_info = {'title': row.tournament_title,
                    'link': row.tournament_link, 'year': row.tournament_year}

        if draw_info: # download and parse draw
            if (draw_info["title"], draw_info["year"]) in Config.UNAVAILABLE_TOURNAMENTS:
                continue
            try:
                draw_filename = download_draw(draw_info)
                draw_data = parse_draw(draw_filename)
                write_draw_to_db(draw_data, draw_info)
                update_drawhistory_db(draw_info)
                logger.info("Updated DB for Draw {} ({})".format(draw_info["title"],
                    draw_info["year"]))
            except:
                logger.info("Unable to Update DB for Draw {} ({})".format(draw_info["title"],
                    draw_info["year"]))
