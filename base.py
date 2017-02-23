from sqlalchemy import Column, Integer, String, BLOB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Command(Base):
    __tablename__ = "commands"
    id = Column(Integer, primary_key=True)
    command_string = Column(String, nullable=False)
    length = Column(Integer, nullable=False)
    # store duration of command run time in seconds, rounded to nearest second
    duration = Column(Integer, nullable=False, default=0)
    output = Column(BLOB)

    def __repr__(self, *args, **kwargs):
        string = 'Command: Name:{} Length:{} Duration:{} Output:{}'.format(self.command_string, self.length, self.duration, self.output)
        # print('object string value is ', string)
        return string

    def __init__(self, command_string, length, duration, output):
        self.command_string = command_string
        self.length = length
        self.duration = duration
        self.output = output

    def serialize(self):
        return {
            'command_string': self.command_string,
            'length': self.length,
            'duration': self.duration,
            'output': self.output
        }
