"""
Handles the work of validating and processing command input.
"""
import configparser
from base import Command
from db import Session
from datetime import datetime
import subprocess as sb
import sqlite3 as sqlite
import time as time
import logging
import sys

logging.basicConfig(level=logging.INFO, filename='applogs.log', filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger('app_logger') 

def get_valid_commands(queue, fi):
    # TODO: efficiently evaluate commands
    file_config = configparser.ConfigParser(allow_no_value=True, strict=False, delimiters="*")
    file_config.read(fi)
    sections = file_config.sections()
    commands = set()
    valid_commands = set()
    logger.info("Available sections in given configuration file are {}".format(sections))
    logger.info(" List of keys in  COMMAND_LIST are :")
    logger.info("-----------------------------------------------------")
    for key in file_config['COMMAND LIST']:
        logger.info(key)
        commands.add(key)
    logger.info("-----------------------------------------------------")
    logger.info(" List of keys in  VALID_COMMANDS are :")
    for key in file_config['VALID COMMANDS']:
        logger.info(key)
        valid_commands.add(key)
    logger.info("------------------------------------------------------")
    commands_to_ptocess = commands.intersection(valid_commands)
    logger.info("List of valid commands are as follows")
    for command in commands_to_ptocess:
        logger.info(command)
        queue.put(command)
    logger.info("------------------------------------------------------")


def process_command_output(queue):
    # TODO: run the command and put its data in the db
    command = queue.get()
    data = command.split()
    start_time = time.time()
    logger.info('Command currently being executed is {}'.format(command))
    try:
    	process = sb.Popen(command, shell=True, stdin=sb.PIPE, stdout=sb.PIPE, stderr=sb.PIPE)
	while process.poll() == None:
	   logger.info('command standard output {}'.format(process.stdout.readline()))
           sys.stdout.write(process.stdout.readline())
	   if time.time()-start_time>40:
		session = Session()	 
                session.add(Command(command, len(command),0,sqlite.Binary('NO_OUTPUT')))
                session.commit()
                session.close()
		return
	   time.sleep(1)
	   process.poll()
    	pipe_output = process.communicate()
    	command_output = pipe_output[0]
    	command_error = pipe_output[1]
    	logger.info('{} generated  {}'.format(command, command_output))
    	duration = (time.time() - start_time)
    	length = len(command)
    	new_command = Command(command, length, duration, sqlite.Binary(command_output))
    	session = Session()
    	session.add(new_command)
    	session.commit()
    except Exception, e:
	logger.error('Error generated while executing [{}], generated error is '.format(command, str(e)))
