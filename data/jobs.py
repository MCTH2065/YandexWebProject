import datetime
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin



class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    boss = sqlalchemy.Column(sqlalchemy.String)
    lower_rank_bosses = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    field_rating_mood_salary = sqlalchemy.Column(sqlalchemy.String)
    is_experience_required = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    makes_happier = sqlalchemy.Column(sqlalchemy.Integer, default=10)
    makes_sadder = sqlalchemy.Column(sqlalchemy.Integer, default=25)
    chance_of_a_job = sqlalchemy.Column(sqlalchemy.Float, default=0.2)


    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
