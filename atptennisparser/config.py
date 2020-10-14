import os
import platform

class Config:
    SERVICE_LOG = "/root/logs/atptps.txt" if platform.system() == 'Linux' else "D:/logs/atptps.txt"
    BASE_URL = "https://www.atptour.com"
    ARCHIVE_URL = "https://www.atptour.com/en/scores/results-archive"
    DATA_FOLDER = "/root/data" if platform.system() == 'Linux' else "D:/atptourdata"
    HEADERS = {"userAgent": 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver' if platform.system() == 'Linux' else \
        'D:\chromedriver_win32\chromedriver.exe'
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    MIN_YEAR = 2010

    # parser cannot currently handle these cases
    UNAVAILABLE_TOURNAMENTS = {
        ("Memphis", 2010): "unavailable",
        ("World Team Cup", 2010): "unavailable",
        ("Memphis", 2011): "unavailable",
        ("World Team Cup", 2011): "unavailable",
        ("ATP Finals", 2011): "unavailable",
        ("Memphis", 2012): "unavailable",
        ("World Team Cup", 2012): "unavailable",
        ("Memphis", 2013): "unavailable",
        ("ATP Finals", 2014): "unavailable",
        ("Stockholm", 2016): "unavailable",
        ("Antwerp", 2016): "unavailable",
        ("Basel", 2016): "unavailable",
        ("Vienna", 2016): "unavailable",
        ("ATP Masters 1000 Paris", 2016): "unavailable",
        ("ATP Finals", 2016): "unavailable",
        ("Laver Cup", 2017): "unavailable",
        ("Nitto ATP Finals", 2017): "unavailable",
        ("Laver Cup", 2018): "unavailable",
        ("Laver Cup", 2019): "unavailable",
        ("ATP Cup", 2020): "unavailable",
        ("ATP Masters 1000 Indian Wells", 2020): "unavailable",
        ("ATP Masters 1000 Miami", 2020): "unavailable",
        ("Marrakech", 2020): "unavailable",
        ("Houston", 2020): "unavailable",
        ("ATP Masters 1000 Monte Carlo", 2020): "unavailable",
        ("Barcelona", 2020): "unavailable",
        ("Budapest", 2020): "unavailable",
        ("Estoril", 2020): "unavailable",
        ("Munich", 2020): "unavailable",
        ("Geneva", 2020): "unavailable",
        ("Lyon", 2020): "unavailable",
        ("Stuttgart", 2020): "unavailable",
        ("s-Hertogenbosch", 2020): "unavailable",
        ("Halle", 2020): "unavailable",
        ("London / Queens Club", 2020): "unavailable",
        ("Mallorca", 2020): "unavailable",
        ("Eastbourne", 2020): "unavailable",
        ("Wimbledon", 2020): "unavailable",
        ("Newport", 2020): "unavailable",
        ("Bastad", 2020): "unavailable",
        ("Los Cabos", 2020): "unavailable",
        ("Gstaad", 2020): "unavailable",
        ("Umag", 2020): "unavailable",
        ("Tokyo Olympics", 2020): "unavailable",
        ("Atlanta", 2020): "unavailable",
        ("ATP Masters 1000 Canada", 2020): "unavailable",
        ("Washington", 2020): "unavailable",
        ("Winston-Salem", 2020): "unavailable",
        ("ATP Masters 1000 Madrid", 2020): "unavailable",
        ("Metz", 2020): "unavailable",
        ("Hamburg", 2020): "unavailable",
        ("Laver Cup", 2020): "unavailable"
    }
