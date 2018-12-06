"""
	Developers: Kenny Jarnagin(2019), 
				Graham Wood(2019)
				Collin Beauchamp-Umphrey(2019)
"""

# Sets up database
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from json import dumps

Base = declarative_base()

class Bucket(Base):
   __tablename__ = 'buckets'
   # TODO Will need to add the fields for the Bucket class here
   id = Column(String, nullable=False,primary_key=True)
   description = Column(String)
   passwordHash= Column(String, nullable=False)

   shortcuts = relationship("Shortcut",back_populates="bucket")
   def __repr__(self):
      return "Shortcut<%s %s %s>" % (self.id,self.description,self.passwordHash)


class Shortcut(Base):
   __tablename__ = 'shortcuts'
   # TODO Will need to add the fields for the Shortcut class here

   linkHash = Column(String,nullable=False,primary_key=True)
   bucketId = Column(String,ForeignKey('buckets.id',ondelete="CASCADE"),nullable=False,primary_key=True)
   link = Column(String, nullable=False)
   description = Column(String)

   bucket = relationship("Bucket", back_populates='shortcuts')

   def __repr__(self):
      return "Shortcut<%s %s %s %s>" % (self.linkHash,self.bucketId,self.link,self.description)

# Represents the database and our interaction with it
class Db:
   def __init__(self):
      engineName = 'sqlite:///test.db'   # Uses in-memory database
      self.engine = create_engine(engineName)
      self.metadata = Base.metadata
      self.metadata.bind = self.engine
      self.metadata.drop_all(bind=self.engine)
      self.metadata.create_all(bind=self.engine)
      Session = sessionmaker(bind=self.engine)
      self.session = Session()

   def commit(self):
      self.session.commit()

   def rollback(self):
      self.session.rollback()

   # TODO Must implement the following methods
   def getBuckets(self):
      return self.session.query(Bucket).all()

   def getBucket(self, id):
      return self.session.query(Bucket)\
               .filter_by(id=id)\
               .one_or_none()

   def addBucket(self, id, passwordHash, description=None):
      bucket = Bucket(id=id, description=description, passwordHash=passwordHash)
      self.session.add(bucket)
      return bucket

   def deleteBucket(self, bucket):
      self.session.delete(bucket)

   def getShortcut(self, linkHash, bucket):
      return self.session.query(Shortcut)\
               .filter_by(linkHash=linkHash)\
               .filter_by(bucket=bucket)\
               .one_or_none()

   def addShortcut(self, linkHash, bucket, link, description=None):
      shortcut = Shortcut(linkHash=linkHash, bucket=bucket, link=link, description=description)
      self.session.add(shortcut)
      return shortcut

   def deleteShortcut(self, shortcut):
      self.session.delete(shortcut)

   # TODO: May need to add your own db functions here