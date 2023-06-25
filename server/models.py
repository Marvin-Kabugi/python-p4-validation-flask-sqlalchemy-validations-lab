from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, db.CheckConstraint('len(name) > 0'), unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('phone_number','name')
    def validate_phonenumber(self, key, address):
        if key == "phone_number":
            if len(address) != 10:
                raise ValueError("Phone number has to be 10 digits")
            return address
        
        elif key == "name":
            if len(address) <= 0:
                raise ValueError("Author must have a name")
            return address

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, db.CheckConstraint("len(title) > 0"), nullable=False,)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content', 'summary', 'category', 'title')
    def validate_post_content(self, key, address):
        if key == "content":
            if len(address) < 250:
                raise ValueError("Content has to be more than 250 characters long")
            return address
        
        elif key == "summary":
            if len(address) >= 250:
                raise ValueError("Summary should not be more than 250 characters long")
            return address
            
        elif key == "category":
            if address != "Non-Fiction" and address != "Fiction":
                raise ValueError("Category should either be 'Fiction' or 'Non-Fiction'")
            return address
        
        elif key == "title":
            if len(address) < 1 or (("Won't Beleive" not in address) and ("Secret" not in address) and ("Top" not in address) and ("Guess") not in address):
                raise ValueError('Title must be included')
            return address

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
