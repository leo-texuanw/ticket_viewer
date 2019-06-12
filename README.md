# Structure:

- **templates:** General templates for the whole project, including  
    - `404.html`
    - `base.html`: a base template that every specific template can be built
        base on it
- **ticket_viewer:** Common settings, configurations, modules for the whole project.
    - `secret_config.py`: configure the secret key and your
        [Zendesk](https://zendesk.com) account for the project
    - `resp_status.py`: configure common response status with more informative
        names for integer status codes and optionally give default hint to each
        status for end users
    - `zendesk.py`: a common encapsulate module to interact with Zendesk servers
    - `test.py`: a test module for `zendesk.py`
    - `urls.py`: url dispatcher for the whole project
        (dispatch requests to corresponding apps)
- **tickets:** An app deals with everything that's related to tickets,
    currently only list all tickets and loop up a specific ticket for details
    - `urls.py`: url dispatcher for app **tickets**
        (dispatch requests to corresponding views)
    - `views.py`: actually deal with web request, calling zendesk API to get
        relevant information at back and display result to user screen


# Instruction:
This project requires python3 and Django
## Environment Setup
```shell
    $ brew install python3
    $ pip3 install Django
```
## Clone this project

`cd` to the path you want to place this project, then use the following
command to clone the project.

```shell
    $ git clone https://github.com/leo-texuanw/ticket_viewer.git
```

## Start server

**Notice:** Before you start the server make sure you have configure the
`ticket_viewer/secret_config.py` file by filling your zendesk account info it.
Click [here](<https://www.zendesk.com/register/free-trial/>) to register for
free trail, if you don't have a Zendesk account yet.  

Now let's start the server (Make sure your current directory is where `manage.py` stays).

### On local machine (Dev Mode)

```shell
    $ python manage.py runserver 8000
```

You can change the default port 8000 to be any available port, if this port is
already in use on your machine.  

### On a server (Product Mode)

1. Add your public ip or hostname into `ALLOWED_HOSTS` field in `ticket_viewer/settings.py`
2. Set `DEBUG` field in the same file as `False`
3. Start the server with command

```    shell
    $ python manage.py runserver 0:8000
```

After you start the server, now let's open browser and visit this website by
```
    http://127.0.0.1:8000/
```
if you are running at your local machine; or

```
    http://hostname:8000/
```
if you are running in a server.
