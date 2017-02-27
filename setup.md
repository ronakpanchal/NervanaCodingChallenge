<h2>Instructions for setting up Project</h2>
<ul>Before running "make run" or python main.py please perform following steps<ul>
   <li>We need to install configparser, RabbitMQ and Celery</li>
   <li>The above requirements are mentioned in requirements.txt along with their version numbers
   <li>To start the RabbitMQ server execute "sudo rabbitmq-server -detached"</li>
   <li>Start up the Celery worker by executing below command<br> <b>celery -A Task worker --loglevel=info --logfile=celery.log -Ofair</b></li>
   <li>Now in a different terminal window ,run make run</li>


 <p><h3>Notes for Bonus # 3 </h3></p>
 <ul></ul>
 <li>I am posting two JSON arrays 'COMMAND_lIST' and 'VALID_COMMANDS' as parameter values using file_data parameter when calling  '/commands' endpoint</li>
 <li>For Example.<br><b>data = {'COMMAND_LIST':['ls','ls -al'],'VALID_COMMANDS': ['ls','ls -al']}</li>json_data = json.dumps(data)<br>
  requests.post("localhost:8080/commands", params={'file_data':json_data})


 <p><h5>A note on logs and test cases </h5></p>
 <ul></ul>
 <li>Two different log files will be genrated after starting app</li>
 <li>One for application logs and other for logging celery task queue</li>
 <li>File 'applogs.log' corresponds to application logs and celery.log to task queue</li>
 <li>The file AppTest.py has some test cases written to test the app.</li>
