from app import db


used_stamps = db.Table(
    "used_stamps",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("stamp_id", db.Integer, db.ForeignKey("stamps.id"), primary_key=True),
)


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    image_id = db.Column(db.String(10), nullable=True, unique=True)
    used_stamps = db.relationship(
        "Stamps",
        secondary=used_stamps,
        backref=db.backref("users", lazy="dynamic"),
        cascade="save-update",
    )


class StampCategories(db.Model):
    __tablename__ = "stamp_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    stamps = db.relationship("Stamps", backref="category", cascade="all")


class Stamps(db.Model):
    __tablename__ = "stamps"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("stamp_categories.id"), nullable=False
    )
    image_id = db.Column(db.String(10), nullable=True, unique=True)
