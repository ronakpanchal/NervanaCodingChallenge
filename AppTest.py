import unittest
from flask import request
from main import app, logger
import requests
import json

class AppTest(unittest.TestCase):

  def setUp(self):
    self.app = app.test_client()


  def test_database_created(self):
    response = self.app.post('/database') 
    self.assertEqual(response.status_code, 200)
    logger.debug('Response from post request to database url is {}'.format(response.data))
    logger.debug('Response code post  request to database is {}'.format(response.status_code))
    return response


  def test_commands_get_works(self): 
    response = self.app.get("/commands")
    self.assertEqual(response.status_code, 200)
    logger.debug('Response from get request to commands url is {}'.format(response.data))
    logger.debug('Response code get request to commands is {}'.format(response.status_code))
    self.assertEqual(response.status_code, 200)
    return response
  
  def test_post_command(self):
    # response = self.app.post('/commands', data=json.dumps({'filename': 'commands.txt'}), content_type='application/json')
    response = requests.post("http://ec2-52-34-173-11.us-west-2.compute.amazonaws.com:8080/commands", params={'filename': 'commands.txt'})
    self.assertEqual(response.status_code, 200)
    logger.debug('Response from post request to commands url is {}'.format(response.content))
    logger.debug('Response code post request to commands is {}'.format(response.status_code))
    return response
  
 
if __name__ == "__main__":
  logger.debug('Starting app in test mode')
  unittest.main()
