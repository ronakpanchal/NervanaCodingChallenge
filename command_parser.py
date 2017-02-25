"""
Handles the work of validating and processing command input.
"""
import configparser
from base import Command
from db import Session
from datetime import datetime, timedelta 
import subprocess as sb
import sqlite3 as sqlite
import time as time
import logging
import sys
import multiprocessing
from celery import Celery
from Task import process_shell_command


logging.basicConfig(level=logging.INFO, filename='applogs.log', filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger('app_logger') 

def get_valid_commands(queue, fi, file_data):
    logger.info('Inside get valid commands')    
    commands =set()
    valid_commands =set()

    if file_data:
	commands = set(file_data['COMMAND_LIST'])
	valid_commands = set(file_data['VALID_COMMANDS'])
	# logger.info('List of commands from post request is ', commands)
	# logger.info('List of vali commands from post request is ', valid_commands)
    else:
    # TODO: efficiently evaluate commands
    	file_config = configparser.ConfigParser(allow_no_value=True, strict=False, delimiters="*")
    	file_config.read(fi)
    	sections = file_config.sections()
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
    commands_to_process = commands.intersection(valid_commands)
    logger.info("List of valid commands are as follows")
    for command in commands_to_process:
        logger.info(command)
        queue.put(command)
    logger.info("------------------------------------------------------")


def process_command_output(queue):
    # TODO: run the command and put its data in the db
    command = queue.get()
    # process_shell_command.apply_async(kwargs={'command_name':command}, expires=datetime.now()+timedelta(minutes=2)) 
    process_shell_command.delay(command)

