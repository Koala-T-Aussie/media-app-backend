import os
import requests
from dotenv import load_dotenv

from src.logging.logger import get_logger

_log = get_logger(__name__)
load_dotenv()
URL = os.getenv('IMDB_API')
API_KEY = os.getenv('API_KEY')

def search_imdb(search_term):
    _log.debug(f'{URL}SearchTitle/{API_KEY}/{search_term}')
    return requests.get(f'{URL}/SearchTitle/{API_KEY}/{search_term}').json()

def get_media_from_id(title_id):
    _log.debug(f'{URL}Title/{API_KEY}/{title_id}')
    return requests.get(f'{URL}/Title/{API_KEY}/{title_id}').json()

def get_season(show_id, season):
    _log.debug(f'{URL}/SeasonEpisodes/{API_KEY}/{show_id}/{season}')
    return requests.get(f'{URL}/SeasonEpisodes/{API_KEY}/{show_id}/{season}').json()
