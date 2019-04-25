from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String)
    professors = db.relationship('Professor', secondary=classroom, lazy='subquery', backref=db.backref('student', lazy=True))

class Professor(db.Model):
    __tablename__ = 'professor'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String)
    # classroom = db.relationship('Professor', secondary=classroom, lazy='subquery', backref=db.backref('student', lazy=True))

prof = db.Table (
    'professors',
    db.Column('student_id', db.BigInteger, db.ForeignKey('student.id'), primary_key=True),
    db.Column('professor_id', db.Integer, db.ForeignKey('professor.id'), primary_key=True)
)

@app.cli.command()
def init_db():
    click.echo('init db')
    meta = db.metadata
    db.drop_all() 
    db.create_all() 

@app.cli.command()
def init_data():
    click.echo('generate data')
    s1 = Student(name='kevin')
    s2 = Student(name='bob')
    p1 = Professor(name='John')
    s1.professors.append(s1)
    db.session.add(s1)
    db.session.commit()