# models.py
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from config import DATABASE_URI

Base = declarative_base()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    books = relationship('Book', backref='author', lazy=True)

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    isbn_code = Column(String(13), unique=True, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

def create_tables():
    Base.metadata.create_all(engine)