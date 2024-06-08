from flask import Flask
from config import Config
from config import db
from routes.venueRoute import venue_blueprint
from routes.iconRoute import icon_blueprint
from routes.mapRoutes import map_blueprint


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(venue_blueprint, url_prefix='/api/v1/venues')
app.register_blueprint(icon_blueprint, url_prefix='/api/v1/venue-icons')
app.register_blueprint(map_blueprint, url_prefix='/api/v1/venue-maps')

if __name__ == '__main__':
    app.run()
