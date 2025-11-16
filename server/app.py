from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Room, DeviceCategory, Device, DeviceLog
from routes import api
from config import config
import os

def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    # Ensure the instance folder exists (Flask uses this for instance-specific files)
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except Exception:
        # If instance_path cannot be created, continue; config will attempt to use relative path
        pass
    app.config.from_object(config[config_name])
    # If no explicit DATABASE_URL is set, prefer an absolute path under the instance folder.
    # This ensures the DB lives in <project>/instance/app.db regardless of current working dir.
    if not os.environ.get('DATABASE_URL'):
        instance_db_path = os.path.join(app.instance_path, 'app.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{instance_db_path}"
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    # Allow cross-origin requests (development only). Adjust origins for production.
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    app.register_blueprint(api)
    
    # Main route
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Smart Home Device Manager API',
            'version': '1.0.0',
            'endpoints': {
                'devices': '/api/devices',
                'rooms': '/api/rooms',
                'categories': '/api/categories',
                'stats': '/api/stats'
            }
        })
    
    return app

def init_sample_data():
    """Initialize the database with sample data"""
    # Check if we already have data
    if Room.query.first() is not None:
        print("Database already has data")
        return
    
    # Create sample rooms
    living_room = Room(name='Living Room', description='Main living area')
    bedroom = Room(name='Bedroom', description='Master bedroom')
    kitchen = Room(name='Kitchen', description='Kitchen area')
    
    db.session.add_all([living_room, bedroom, kitchen])
    
    # Create device categories
    lights = DeviceCategory(name='Lights', icon='lightbulb')
    sensors = DeviceCategory(name='Sensors', icon='sensor')
    cameras = DeviceCategory(name='Cameras', icon='camera')
    thermostats = DeviceCategory(name='Thermostats', icon='thermostat')
    
    db.session.add_all([lights, sensors, cameras, thermostats])
    
    # Commit the rooms and categories first
    db.session.commit()
    
    # Create sample devices
    devices = [
        Device(
            name='Smart LED Bulb 1',
            device_type='light',
            brand='Philips',
            model='Hue White',
            ip_address='192.168.1.10',
            status='online',
            room_id=living_room.id,
            category_id=lights.id
        ),
        Device(
            name='Motion Sensor',
            device_type='sensor',
            brand='Samsung',
            model='SmartThings',
            ip_address='192.168.1.11',
            status='online',
            room_id=living_room.id,
            category_id=sensors.id
        ),
        Device(
            name='Security Camera',
            device_type='camera',
            brand='Ring',
            model='Indoor Cam',
            ip_address='192.168.1.12',
            status='offline',
            room_id=bedroom.id,
            category_id=cameras.id
        )
    ]
    
    db.session.add_all(devices)
    db.session.commit()
    
    print("Database initialized with sample data!")

# Create the app instance
app = create_app()

if __name__ == '__main__':
    # Prefer explicit PORT env var (use 5555 to avoid macOS AirPlay conflicts on 5000)
    port = int(os.environ.get('PORT', os.environ.get('FLASK_RUN_PORT', 5555)))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() in ('1', 'true', 'yes')

    with app.app_context():
        db.create_all()
        init_sample_data()

    app.run(host='0.0.0.0', port=port, debug=debug)