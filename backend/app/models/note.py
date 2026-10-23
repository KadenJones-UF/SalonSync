from datetime import datetime, timezone

from ..extensions import db

class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    shades = db.Column(db.String(255), nullable=False)
    developer = db.Column(db.String(100), nullable=False)
    processing_time = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    is_public = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship("User", backref=db.backref("notes", lazy=True, cascade="all, delete-orphan"))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "author_username": self.user.username if self.user else None,
            "title": self.title,
            "brand": self.brand,
            "shades": self.shades,
            "developer": self.developer,
            "processing_time": self.processing_time,
            "notes": self.notes or "",
            "is_public": self.is_public,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
