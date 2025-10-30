from flask import Flask
from flask_restx import Api, Resource, fields, Namespace
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    api = Api(
        app,
        version='1.0',
        title='Notification Service',
        description="Handles notifications for Orders, Payments, and Shipments",
        doc="/v1/",
        prefix="/v1")
    
    # DB setup
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notifications.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Model
    class Notification(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        message = db.Column(db.String(200), nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

    ns = Namespace('notifications', description='Notification operations')

    notification_model = ns.model('Notification', {
        'id': fields.Integer(readOnly=True, description='Notification ID'),
        'message': fields.String(required=True, description='Notification message'),
        'created_at': fields.DateTime(description='Time created')
    })

    @ns.route('/')
    class NotificationList(Resource):
        @ns.marshal_list_with(notification_model)
        def get(self):
            return Notification.query.all()

        @ns.expect(notification_model)
        @ns.marshal_with(notification_model, code=201)
        def post(self):
            data = ns.payload
            notif = Notification(message=data['message'])
            db.session.add(notif)
            db.session.commit()
            return notif, 201

    api.add_namespace(ns)

    with app.app_context():
        db.create_all()

    return app
