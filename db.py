from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

engine = create_engine('sqlite:///commands.db', convert_unicode=True)
Session = scoped_session(sessionmaker(bind=engine))

