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
    # process_shell_command.apply_async(kwargs={'command_name':command}, expires=datetime.now()+timedelta(minutes=2)) 
    process_shell_command.delay(command)

