from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class Cupcake(db.Model):
    """Cupcake"""

    def __repr__(self):
        e = self
        return f"<Cupcake {e.id} {e.flavor} {e.size} {e.rating}>"
    
    @classmethod
    def serialize(cls, obj):
        return {
            "id": obj.id,
            "flavor": obj.flavor,
            "size": obj.size,
            "rating": obj.rating,
            "image": obj.image
        }

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    flavor = db.Column(db.String(20), nullable=False)

    size = db.Column(db.String(20), nullable=False)

    rating = db.Column(db.Float, nullable=False)

    image = db.Column(db.String, default="https://tinyurl.com/truffle-cupcake")