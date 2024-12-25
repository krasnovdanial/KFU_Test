from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Operator(db.Model):
    __tablename__ = 'operators'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    wells = db.relationship('Well', backref='operator', lazy=True)

class Well(db.Model):
    __tablename__ = 'wells'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    operator_id = db.Column(db.Integer, db.ForeignKey('operators.id'), nullable=False)
    productions = db.relationship('Production', backref='well', lazy=True)
    equipments = db.relationship('Equipment', backref='well', lazy=True)

class Production(db.Model):
    __tablename__ = 'productions'
    id = db.Column(db.Integer, primary_key=True)
    well_id = db.Column(db.Integer, db.ForeignKey('wells.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    oil_produced = db.Column(db.Float, nullable=False)
    gas_produced = db.Column(db.Float, nullable=False)

class Equipment(db.Model):
    __tablename__ = 'equipments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    well_id = db.Column(db.Integer, db.ForeignKey('wells.id'), nullable=False)
    maintenances = db.relationship('Maintenance', backref='equipment', lazy=True)

class Maintenance(db.Model):
    __tablename__ = 'maintenances'
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    cost = db.Column(db.Float, nullable=False)
