from flask import Flask
from flask_cors import CORS
from flask_restplus import Api, Resource

from src.router.routes import SearchRoute, WatchedRoute, WatchlistRoute, TimeRoute

api = Api() # Initialize an instance of the Flask RestPLUS API class
app = Flask(__name__) # Initialize Flask

# Initialize CORS for cross origin requests for testing purposes
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Initialize and run the API
api.init_app(app, version='0.0', title='My Media App',
             description='The back end for the My Media App')

api.add_resource(SearchRoute, '/search/<string:search_string>')
api.add_resource(WatchedRoute, '/list/watched')
api.add_resource(WatchlistRoute, '/list/watchlist')
api.add_resource(TimeRoute, '/time')
