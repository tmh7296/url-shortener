from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()

# class for the ORM to infer DB table creations
class ShortenedUrl(db.Model):
    __tablename__ = 'shortened_urls'
 
    slug = db.Column(db.String(), primary_key=True)
    url = db.Column(db.String())
    created_at = db.Column(db.DateTime())
 
    def __init__(self, slug, url, created_at=None):
        self.slug = slug
        self.url = url
        if created_at is None:
            created_at = datetime.utcnow()
        self.created_at = created_at

    def __repr__(self):
        return f"{self.slug} : {self.url}"
 