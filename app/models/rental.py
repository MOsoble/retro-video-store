from app import db
from app.models.customer import Customer
from app.models.video import Video
import datetime 

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime, default=datetime.date.today() + datetime.timedelta(days=7))
    
    def get_checked_out_count(self, video_id):
        return Rental.query.filter_by(video_id=video_id).count()
    
    def get_available_inventory(self, video_id):
        video = Video.query.get(video_id)
        return video.total_inventory - self.get_checked_out_count(video_id)
    
    def to_json(self):
        return {
            "customer_id" : self.customer_id,
            "video_id" : self.video_id,
            "videos_checked_out_count" : self.get_checked_out_count(self.video_id),
            "available_inventory" : self.get_available_inventory(self.video_id)
        }

    def customer_details(self):
        customer = Customer.query.get(self.customer_id)
        return {
            "due_date" : self.due_date,
            "name" : customer.name,
            "phone" : customer.phone,
            "postal_code" : customer.postal_code 
        }

    def video_details(self):
        video = Video.query.get(self.video_id)
        return {
            "release_date": video.release_date,
            "title": video.title,
            "due_date": self.due_date,
        }