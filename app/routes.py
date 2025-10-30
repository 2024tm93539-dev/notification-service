from flask_restx import Namespace, Resource, fields

ns = Namespace("notifications", description="Notification operations")

# Example model (for documentation)
notification_model = ns.model("Notification", {
    "id": fields.Integer(readonly=True),
    "type": fields.String(required=True, description="Type of notification"),
    "message": fields.String(required=True, description="Notification message"),
    "status": fields.String(default="pending"),
})

notifications = []  # In-memory storage for now

@ns.route("/")
class NotificationList(Resource):
    @ns.marshal_list_with(notification_model)
    def get(self):
        """List all notifications"""
        return notifications
    
    @ns.expect(notification_model)
    @ns.marshal_with(notification_model, code=201)
    def post(self):
        """Create a new notification"""
        new_notification = ns.payload
        new_notification["id"] = len(notifications) + 1
        notifications.append(new_notification)
        return new_notification, 201

