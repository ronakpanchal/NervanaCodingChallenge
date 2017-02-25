from __future__ import absolute_import
from celery import Celery
from db import Session
import sqlite3 as sqlite
import sys
import time as time
import subprocess as sb
from base import Command
from celery.utils.log import get_task_logger


celery = Celery("tasks", broker='amqp://',backend='amqp', CELERYD_LOG_FILE='celery.log')


@celery.task(name="tasks.process_shell_command")
def process_shell_command(command_name):
	logger = get_task_logger(__name__)
	logger.info('inside process request async')
	start_time = time.time()
	logger.info('Command currently being executed is {}'.format(command_name))
	try:
		process = sb.Popen(command_name, shell=True, stdin=sb.PIPE, stdout=sb.PIPE, stderr=sb.PIPE)
		process_Terminated = False
		while process.poll() == None:
			if time.time()-start_time>60:
				process_Terminated = True
				break;
			time.sleep(1)
			process.poll()
		pipe_output = process.communicate()
		command_output = pipe_output[0]
		logger.info('Output value for {} command is {}'.format(command_name, command_output))
		command_error = pipe_output[1]	
		logger.info('{} generated  {}'.format(command_name, command_output))
		duration = (time.time() - start_time)
		if process_Terminated:
			duration = 0
			logger.debug('The process was terminated as taking more time then 1 minute')
			command_output = 'Process was terminated'
		length = len(command_name)
		new_command = Command(command_name, length, duration, sqlite.Binary(command_output))
		session = Session()
		session.add(new_command)
		session.commit()
	except Exception, e:
		logger.error('Error generated while executing [{}], generated error is {}'.format(command_name, str(e)))

		
if __name__ == "__main__":
    celery.start()
