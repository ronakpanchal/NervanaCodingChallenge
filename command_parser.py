"""
Handles the work of validating and processing command input.
"""
import configparser
from base import Command
from db import Session
from datetime import datetime
import subprocess as sb
import sqlite3 as sqlite


def get_valid_commands(queue, fi):
    # TODO: efficiently evaluate commands
    file_config = configparser.ConfigParser(allow_no_value=True, strict=False, delimiters="*")
    file_config.read(fi)
    sections = file_config.sections()
    commands = set()
    valid_commands = set()
    print("Available sections in given configuration file are", sections)
    print(" List of keys in  COMMAND_LIST are :")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    for key in file_config['COMMAND LIST']:
        print(key)
        commands.add(key)
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(" List of keys in  VALID_COMMANDS are :")
    for key in file_config['VALID COMMANDS']:
        print(key)
        valid_commands.add(key)
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    commands_to_ptocess = commands.intersection(valid_commands)
    print("List of valid commands are as follows")
    for command in commands_to_ptocess:
        print(command)
        queue.put(command)
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")


def process_command_output(queue):
    # TODO: run the command and put its data in the db
    command = queue.get()
    print("Command name is ", command)
    # data = command.split()
    '''
    start_time = datetime.now()
    process = sb.Popen(command, stdout=sb.PIPE)
    command_output = process.communicate()[0]
    print('Command output is ', command_output)
    command_error = process.communicate()[1]
    print('Command error  is ', command_error)
    duration = (datetime.now() - start_time)*1000
   '''
    length = len(command)
    new_command = Command(command, length, 0, memoryview(b'nothing'))
    Session.add(new_command)
    Session.commit()
    # Session.close()


