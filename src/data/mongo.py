import pymongo
import os
from dotenv import load_dotenv
from src.logging.logger import get_logger
from src.external.external import get_season

_log = get_logger(__name__)
load_dotenv()

try:
    _db = pymongo.MongoClient(os.getenv('MONGO_URI_RENE')).medialist
except pymongo.errors.PyMongoError:
    _log.exception('Mongo connection has failed')
    raise

key_list = ['_id', 'title', 'fullTitle', 'type', 'year', 'image', 'releaseDate', 'runtimeMins',
            'runtimeStr', 'tvSeriesInfo', 'tvEpisodeInfo']

def setup_dict(input_dict):
    input_dict['_id'] = input_dict.pop('id')
    input_dict['runtimeMins'] = int(input_dict['runtimeMins'])
    if input_dict['tvSeriesInfo']:
        seasons = input_dict['tvSeriesInfo']['seasons']
        episodes = 0
        for season in seasons:
            season_info = get_season(input_dict['_id'], int(season))
            episodes = episodes + len(season_info['episodes'])
        input_dict['runtimeMins'] = input_dict['runtimeMins'] * episodes
    concise_dict = {key: input_dict[key] for key in key_list}
    return concise_dict

def add_to_watched(media_dict):
    new_dict = setup_dict(media_dict)
    # media_dict['_id'] = media_dict.pop('id')
    # media_dict['runtimeMins'] = int(media_dict['runtimeMins'])
    # if media_dict['tvSeriesInfo']:
    #     seasons = media_dict['tvSeriesInfo']['seasons']
    #     episodes = 0
    #     for season in seasons:
    #         season_info = get_season(media_dict['_id'], int(season))
    #         episodes = episodes + len(season_info['episodes'])
    #     media_dict['runtimeMins'] = media_dict['runtimeMins'] * episodes
    # new_dict = {key: media_dict[key] for key in key_list}
    already_in = _db.watched.find_one(new_dict)
    in_watchlist = _db.watchlist.find_one(new_dict)
    if not already_in:
        _db.watched.insert_one(new_dict)
    if in_watchlist:
        _db.watchlist.delete_one(new_dict)

def add_to_watchlist(media_dict):
    new_dict = setup_dict(media_dict)
    # media_dict['_id'] = media_dict.pop('id')
    # media_dict['runtimeMins'] = int(media_dict['runtimeMins'])
    # if media_dict['tvSeriesInfo']:
    #     seasons = media_dict['tvSeriesInfo']['seasons']
    #     episodes = 0
    #     for season in seasons:
    #         season_info = get_season(media_dict['_id'], int(season))
    #         episodes = episodes + len(season_info['episodes'])
    #     media_dict['runtimeMins'] = media_dict['runtimeMins'] * episodes
    # new_dict = {key: media_dict[key] for key in key_list}
    already_in = _db.watchlist.find_one(new_dict)
    in_watched = _db.watched.find_one(new_dict)
    if not already_in and not in_watched:
        _db.watchlist.insert_one(new_dict)

def get_all_watched():
    return list(_db.watched.find({}))

def get_all_watchlist():
    return list(_db.watchlist.find({}))

def get_watch_time():
    agr = [{'$group': {'_id': 1, 'total': {'$sum': '$runtimeMins'}}}]
    watchtime = list(_db.watched.aggregate(agr))
    watchtime = watchtime[0]['total']
    return watchtime
