# Nervana Cloud Coding Challenge #

You are to build a server that processes valid bash command strings.
Your server takes the command strings from commands.txt and does the following:

1. Checks that the command strings in the COMMAND_LIST section are valid command strings by cross-checking with the VALID_command strings section. Regardless of the command itself, the command string needs to exactly match a command in the valid command strings list.
   Ex: `grep "tacos" commands.txt` isn't valid, but `grep "pwd" commands.txt` is.

Assuming the command is valid:
2. Stores metadata about each command:
    - actual command itself as a string
    - length of command string
    - time to complete (up to 1 min, else mark as 0)
    - eventual output (see below)
3. Grabs the command output from each command if possible.
4. Stores the output in the db provided.
5. Enables the data to be fetched via the endpoint provided in the code.

The basics of the project have already been flushed out for you.
Approach this project as if this were production code, with time and space complexity in mind.
Also keep in mind edge cases; what about command strings that don't terminate in time? Invalid bash and "malicious" command strings have already been screened out for you.
Write a few tests for your code as well.
Finally, when you're done, send us the link to where we can see the code on your Github/Bitbucket/etc.
Good luck!

## Full-time challenge ##
In addition to the main challenge above, extend your project with the following:

Regarding #3, Grabs all command strings at once and queue them up to be run, and then run each of them individually inside their own docker container (for isolation).
Some tools that might prove useful: Redis, Celery, bashlex, htcondor/Kubernetes, PostgreSQL/MySQL/MongoDB, Docker, cronjobs, python's `schedule` module, bash.
When you're done, host it and send us the link of where it's at!


### For how to run either project ###
1. `make run` to start the project; see the `Makefile` for other helpful things like `make swagger`
2. You can then hit it to either drop the db, init the db, fetch results, input data (curl or python requests).
   - Sample request to feed in the data: requests.post("http://127.0.0.1:8080/commands", params={'filename': 'commands.txt'})
