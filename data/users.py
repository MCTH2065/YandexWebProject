import datetime
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    rating = sqlalchemy.Column(sqlalchemy.Integer, default=45)
    experience = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    money = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    mood = sqlalchemy.Column(sqlalchemy.Integer, default=70)
    bio = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    pfp = sqlalchemy.Column(sqlalchemy.String)
    codeword = sqlalchemy.Column(sqlalchemy.String)
    comp = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("jobs.id"), nullable=True)
    head = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    field = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work = sqlalchemy.Column(sqlalchemy.String)
    work_is_done = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    salary = sqlalchemy.Column(sqlalchemy.String)

    job = orm.relation('Jobs')

    def __repr__(self):
        return f'{self.email} {self.hashed_password}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        # return check_password_hash(self.hashed_password, password)
        return str(password) == str(self.hashed_password)
