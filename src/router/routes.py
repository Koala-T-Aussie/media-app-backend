from flask import request
from flask_restplus import Resource, Api
from src.logging.logger import get_logger
from src.external.external import search_imdb, get_media_from_id
from src.data.mongo import add_to_watched, add_to_watchlist, get_all_watched, get_all_watchlist, get_watch_time

_log = get_logger(__name__)

api = Api()

@api.route('/search/<str:search_string>')
class SearchRoute(Resource):
    '''Class for routing search requests'''
    @api.response(200, 'Success')
    def get(self, search_string):
        '''Retrieves a list of search results from IMDB api'''
        return search_imdb(search_string)

@api.route('/list/watched')
class WatchedRoute(Resource):
    '''Class for routing watched media'''
    @api.response(201, 'Created')
    def post(self):
        _log.debug(request.get_json()['media_id'])
        media_dict = get_media_from_id(request.get_json()['media_id'])
        add_to_watched(dict(media_dict))
        return media_dict, 201
    def get(self):
        return get_all_watched()

@api.route('/list/watchlist')
class WatchlistRoute(Resource):
    '''Class for routing watchlist media'''
    @api.response(201, 'Created')
    def post(self):
        _log.debug(request.get_json()['media_id'])
        media_dict = get_media_from_id(request.get_json()['media_id'])
        add_to_watchlist(dict(media_dict))
        return media_dict, 201
    def get(self):
        _log.debug(get_all_watchlist())
        return get_all_watchlist()

@api.route('/time')
class TimeRoute(Resource):
    '''Class for routing time requests'''
    @api.response(200, 'Success')
    def get(self):
        _log.debug(get_watch_time())
        return get_watch_time()
