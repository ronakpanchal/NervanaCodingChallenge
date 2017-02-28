from __future__ import absolute_import
from celery import Celery
from db import Session
import sqlite3 as sqlite
import sys
import time as time
import subprocess as sb
from base import Command
import os
import signal
from celery import Task
from celery.utils.log import get_task_logger


celery = Celery("Shell_Proessor", broker='amqp://',backend='amqp', CELERYD_LOG_FILE='celery.log')
celery.conf.update(result_expires = 3600)
celery.conf.update(task_soft_time_limit = 100)
celery.conf.update(worker_concurrency = 4)



class call_back_on_completion(Task):
	def on_success(self, retval, task_id, args, kwargs):
		pass
	def on_failure(self, exc, task_id, args, kwargs, einfo):
		pass

@celery.task(name="Shell_Processor.process_shell_command", base=call_back_on_completion)
def process_shell_command(command_name):
	logger = get_task_logger(__name__)
	start_time = time.time()
	logger.info('Command currently being executed is {}'.format(command_name))
	try:
		process = sb.Popen(command_name, shell=True, stdin=sb.PIPE, stdout=sb.PIPE, stderr=sb.PIPE, preexec_fn=os.setsid)
		process_Terminated = False
		# The below code snippet handles the case for  taks that take longer then usual(>1 min  to be precise)
		# As we are setting shell=True in Popen call, calling process.kill() may kill the shell itself
		# but not its child process (i.e command itself)
		# As a result we need to assign a session id to the shell(), making it the leader of all the proesses in the group
		# so when we send  'SIGTERM'  singal to group leader(i.e shel), it is propogated to all its children(i.e commands)
		while process.poll() is  None:
			elapsed_time = time.time()-start_time
			if elapsed_time>60:
				logger.info('Total time elapsed while executing task is {}'.format(elapsed_time))
				process_Terminated = True
				os.killpg(os.getpgid(process.pid), signal.SIGTERM)


		pipe_output = process.communicate()
		command_output = pipe_output[0]
		command_error = pipe_output[1]	
		logger.info('{} generated  {}'.format(command_name, command_output))
		duration = (time.time() - start_time)

		
		'''
		If the output value is empty and 
		the error string is non empty, the executed command errored out
		'''
		if not command_output and command_error:
			command_output = command_error
		
		'''
		If the process was terminated forcefully,set the output to reflect that
		Also set the duration to 0 to signify that it was terminated abruptly
		'''
	
		if process_Terminated:
			duration = 0
			logger.debug('The process was terminated due to long running time')
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
