import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
setup_db(app):
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + os.environ.get('DATABASE_URL')[len('postgresql/'):]
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
'''
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.isoformat()

class Article(db.Model):
    __tablename__='articles'

    id = db.Column(db.Integer, primary_key=True)
    articleId = db.Column(db.String, unique=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    datePublished = db.Column(db.DateTime)
    bodyText = db.Column(db.Text)

    def __init__(self, articleId, title, description, datePublished, bodyText):
        self.articleId = articleId
        self.title = title
        self.description = description
        self.datePublished = datePublished
        self.bodyText = bodyText

    def __repr__(self):
        return '<Article Link %r : %r>' % self.articleId, self.datePosted

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'articleId': self.id,
            'title': self.title,
            'description': self.description,
            'datePosted': dump_datetime(self.datePosted),
            'bodyText': self.bodyText
        }

class EventType(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    eventTypeName = db.Column(db.String, unique=True)
    currString = db.Column(db.String)

    def __init__(self, tagName, currString):
        self.eventTypeName = tagName
        self.currString = currString

    def __repr__(self):
        return '<Event Type %s : %s>' % self.eventTypeName, self.currString

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'eventTypeName': self.eventTypeName,
            'currString': self.currString,
        }
