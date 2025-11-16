from flask import Blueprint, jsonify, request
from sqlalchemy import desc
from models import db, Device, Room, DeviceCategory, DeviceLog, User

# Create Blueprint for API routes
api = Blueprint('api', __name__, url_prefix='/api')

# Device routes
@api.route('/devices', methods=['GET'])
def get_devices():
    """Get all devices"""
    devices = Device.query.all()
    return jsonify([device.to_dict() for device in devices])

@api.route('/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    """Get a specific device"""
    device = Device.query.get_or_404(device_id)
    return jsonify(device.to_dict())

@api.route('/devices', methods=['POST'])
def create_device():
    """Create a new device"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'device_type' not in data:
        return jsonify({'error': 'Name and device_type are required'}), 400
    
    device = Device(
        name=data['name'],
        device_type=data['device_type'],
        brand=data.get('brand'),
        model=data.get('model'),
        ip_address=data.get('ip_address'),
        mac_address=data.get('mac_address'),
        room_id=data.get('room_id'),
        category_id=data.get('category_id')
    )
    
    db.session.add(device)
    db.session.commit()
    
    return jsonify(device.to_dict()), 201

@api.route('/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    """Update a device"""
    device = Device.query.get_or_404(device_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields if provided
    if 'name' in data:
        device.name = data['name']
    if 'device_type' in data:
        device.device_type = data['device_type']
    if 'brand' in data:
        device.brand = data['brand']
    if 'model' in data:
        device.model = data['model']
    if 'ip_address' in data:
        device.ip_address = data['ip_address']
    if 'mac_address' in data:
        device.mac_address = data['mac_address']
    if 'status' in data:
        device.status = data['status']
    if 'is_active' in data:
        device.is_active = data['is_active']
    if 'room_id' in data:
        device.room_id = data['room_id']
    if 'category_id' in data:
        device.category_id = data['category_id']
    
    db.session.commit()
    return jsonify(device.to_dict())

@api.route('/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    """Delete a device"""
    device = Device.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    return jsonify({'message': 'Device deleted successfully'})

# Room routes
@api.route('/rooms', methods=['GET'])
def get_rooms():
    """Get all rooms"""
    rooms = Room.query.all()
    return jsonify([room.to_dict() for room in rooms])

@api.route('/rooms/<int:room_id>', methods=['GET'])
def get_room(room_id):
    """Get a specific room"""
    room = Room.query.get_or_404(room_id)
    return jsonify(room.to_dict())

@api.route('/rooms', methods=['POST'])
def create_room():
    """Create a new room"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    room = Room(
        name=data['name'],
        description=data.get('description')
    )
    
    db.session.add(room)
    db.session.commit()
    
    return jsonify(room.to_dict()), 201

# Device Category routes
@api.route('/categories', methods=['GET'])
def get_categories():
    """Get all device categories"""
    categories = DeviceCategory.query.all()
    return jsonify([category.to_dict() for category in categories])

@api.route('/categories', methods=['POST'])
def create_category():
    """Create a new device category"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    category = DeviceCategory(
        name=data['name'],
        icon=data.get('icon')
    )
    
    db.session.add(category)
    db.session.commit()
    
    return jsonify(category.to_dict()), 201

# Device Log routes
@api.route('/devices/<int:device_id>/logs', methods=['GET'])
def get_device_logs(device_id):
    """Get logs for a specific device"""
    device = Device.query.get_or_404(device_id)
    # Order by timestamp using a text clause to avoid static type-checker complaints
    logs = DeviceLog.query.filter_by(device_id=device_id).order_by(db.text('timestamp DESC')).all()
    return jsonify([log.to_dict() for log in logs])

# Dashboard stats route
@api.route('/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    total_devices = Device.query.count()
    online_devices = Device.query.filter_by(status='online').count()
    offline_devices = Device.query.filter_by(status='offline').count()
    error_devices = Device.query.filter_by(status='error').count()
    total_rooms = Room.query.count()
    
    # Convert device type counts into a JSON-serializable list of objects
    # Use a select + execute to construct a predictable result and avoid type warnings
    sel = db.select(Device.device_type, db.func.count(Device.id)).group_by(Device.device_type)
    rows = db.session.execute(sel).fetchall()
    device_types = [{'device_type': row[0], 'count': int(row[1])} for row in rows]

    return jsonify({
        'total_devices': total_devices,
        'online_devices': online_devices,
        'offline_devices': offline_devices,
        'error_devices': error_devices,
        'total_rooms': total_rooms,
        'device_types': device_types
    })