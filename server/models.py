from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    devices = db.relationship('Device', backref='room', lazy=True)
    
    def __repr__(self):
        return f'<Room {self.name}>'
    
    def __init__(self, name: str, description: str | None = None, **kwargs):
        """Explicit constructor to help static analyzers and provide clarity."""
        self.name = name
        self.description = description
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    def to_dict(self):
        # Use a DB count query to avoid type-checker issues with relationship proxy
        from models import Device  # local import to avoid circular at module import time
        device_count = 0
        try:
            device_count = db.session.query(db.func.count(Device.id)).filter(Device.room_id == self.id).scalar() or 0
        except Exception:
            # Fallback to counting by iterating relationship (avoids len() static-type complaint)
            device_count = sum(1 for _ in getattr(self, 'devices', []) )

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'device_count': int(device_count)
        }

class DeviceCategory(db.Model):
    __tablename__ = 'device_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    icon = db.Column(db.String(50))  # For UI icons
    
    # Relationship
    devices = db.relationship('Device', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<DeviceCategory {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon
        }
    
    def __init__(self, name: str, icon: str | None = None, **kwargs):
        self.name = name
        self.icon = icon
        for k, v in kwargs.items():
            setattr(self, k, v)

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    device_type = db.Column(db.String(50), nullable=False)  # light, sensor, camera, etc.
    brand = db.Column(db.String(50))
    model = db.Column(db.String(100))
    ip_address = db.Column(db.String(15))
    mac_address = db.Column(db.String(17))
    status = db.Column(db.String(20), default='offline')  # online, offline, error
    is_active = db.Column(db.Boolean, default=True)
    last_seen = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('device_categories.id'))
    
    # Relationships
    logs = db.relationship('DeviceLog', backref='device', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Device {self.name} ({self.device_type})>'
    
    def to_dict(self):
        # Use getattr to avoid static type errors in linters (relationship attributes are created dynamically)
        room_obj = getattr(self, 'room', None)
        if room_obj:
            room_data = {'id': room_obj.id, 'name': room_obj.name}
        else:
            room_data = None

        category_obj = getattr(self, 'category', None)
        if category_obj:
            category_data = {'id': category_obj.id, 'name': category_obj.name, 'icon': category_obj.icon}
        else:
            category_data = None
            
        return {
            'id': self.id,
            'name': self.name,
            'device_type': self.device_type,
            'brand': self.brand,
            'model': self.model,
            'ip_address': self.ip_address,
            'mac_address': self.mac_address,
            'status': self.status,
            'is_active': self.is_active,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'room': room_data,
            'category': category_data
        }

    def __init__(self, name: str, device_type: str, brand: str | None = None, model: str | None = None,
                 ip_address: str | None = None, mac_address: str | None = None, status: str | None = None,
                 is_active: bool | None = True, last_seen: datetime | None = None, room_id: int | None = None,
                 category_id: int | None = None, **kwargs):
        # Assign required/optional fields and accept extra kwargs
        self.name = name
        self.device_type = device_type
        self.brand = brand
        self.model = model
        self.ip_address = ip_address
        self.mac_address = mac_address
        if status is not None:
            self.status = status
        self.is_active = is_active if is_active is not None else True
        self.last_seen = last_seen
        self.room_id = room_id
        self.category_id = category_id
        for k, v in kwargs.items():
            setattr(self, k, v)

class DeviceLog(db.Model):
    __tablename__ = 'device_logs'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)  # turned_on, turned_off, status_change, etc.
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Key
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    
    def __repr__(self):
        return f'<DeviceLog {self.action} for Device {self.device_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'action': self.action,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'device_id': self.device_id
        }

    def __init__(self, action: str, device_id: int, old_value: str | None = None, new_value: str | None = None, timestamp: datetime | None = None, **kwargs):
        self.action = action
        self.device_id = device_id
        self.old_value = old_value
        self.new_value = new_value
        self.timestamp = timestamp or datetime.utcnow()
        for k, v in kwargs.items():
            setattr(self, k, v)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

    def __init__(self, username: str, email: str, is_active: bool = True, **kwargs):
        self.username = username
        self.email = email
        self.is_active = is_active
        for k, v in kwargs.items():
            setattr(self, k, v)


