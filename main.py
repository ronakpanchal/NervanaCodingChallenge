"""
Details the various flask endpoints for processing and retrieving
command details as well as a swagger spec endpoint
"""

from multiprocessing import Process, Queue
import sys
from flask import Flask, request, jsonify
from flask_swagger import swagger
from db import Session, engine
from base import Base, Command
from command_parser import get_valid_commands, process_command_output
import logging


app = Flask(__name__)
logging.basicConfig(level=logging.INFO, filename='applogs.log', filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger('app_logger') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


@app.route('/commands', methods=['GET'])
def get_command_output():
    """
    Returns as json the command details that have been processed
    ---
    tags: [commands]
    responses:
      200:
        description: Commands returned OK
      400:
        description: Commands not found
    """
    logger.info('inside command query method')
    commands = Session().query(Command).all()
    command_list = list()
    for command in commands:
        command_list.append(Command(command.command_string, command.length, command.duration, str(command.output)))
    logger.info('The list of valid commands is  {}'.format(command_list))
    # TODO: format the query result
    return jsonify(eqtls=[cmd_obj.serialize() for cmd_obj in command_list])


@app.route('/commands', methods=['POST'])
def process_commands():
    """
    Processes commmands from a command list
    ---
    tags: [commands]
    parameters:
      - name: filename
        in: formData
        description: filename of the commands text file to parse
        required: true
        type: string
    responses:
      200:
        description: Processing OK
    """
    fi = request.args.get('filename')
    logger.info("Inside commands post method")
    queue = Queue()
    get_valid_commands(queue, fi)
    processes = [Process(target=process_command_output, args=(queue,))
                 for num in range(3)]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    return 'Successfully processed commands.'


@app.route('/database', methods=['POST'])
def make_db():
    """
    Creates database schema
    ---
    tags: [db]
    responses:
      200:
        description: DB Creation OK
    """
    logger.debug('creating commands table')
    Base.metadata.create_all(engine)
    return 'Database creation successful.'


@app.route('/database', methods=['DELETE'])
def drop_db():
    """
    Drops all db tables
    ---
    tags: [db]
    responses:
      200:
        description: DB table drop OK
    """
    logger.debug('dropping all tables')
    Base.metadata.drop_all(engine)
    return 'Database deletion successful.'

@app.errorhandler(404)
def page_not_found(error):
    logger.error('Requested URL not found')
    return jsonify(
        error='Requested URL not found',
        error_code=404,
    )

@app.errorhandler(500)
def internal_server_error(error):
    logger.error('An internal server error was generated, Error is  {}'.format(error))
    return jsonify(
        error='An internal error was generated',
    )
 
@app.errorhandler(Exception)
def unhandled_exception(e):
    logger.error('An internal server error was generated, Error is  {}'.format(e))
    return jsonify(
        error='An internal error was generated',
    )

if __name__ == '__main__':
    """
    Starts up the flask server
    """
    port = 8080
    use_reloader = True
    logger.info('starting app at 0.0.0.0')
    # provides some configurable options
    for arg in sys.argv[1:]:
        if '--port' in arg:
            port = int(arg.split('=')[1])
        elif '--use_reloader' in arg:
            use_reloader = arg.split('=')[1] == 'true'

    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=use_reloader)


@app.route('/spec')
def swagger_spec():
    """
    Display the swagger formatted JSON API specification.
    ---
    tags: [docs]
    responses:
      200:
        description: OK status
    """
    spec = swagger(app)
    spec['info']['title'] = "Nervana cloud challenge API"
    spec['info']['description'] = ("Nervana's cloud challenge " +
                                   "for interns and full-time hires")
    spec['info']['license'] = {
        "name": "Nervana Proprietary License",
        "url": "http://www.nervanasys.com",
    }
    spec['info']['contact'] = {
        "name": "Nervana Systems",
        "url": "http://www.nervanasys.com",
        "email": "info@nervanasys.com",
    }
    spec['schemes'] = ['http']
    spec['tags'] = [
        {"name": "db", "description": "database actions (create, delete)"},
        {"name": "commands", "description": "process and retrieve commands"}
    ]
    return jsonify(spec)
