OK = "OK"
ERROR = "ERROR"

STATUS_CODE = {
    200: {
        'info': "OK",
    },
    401: {
        'info': "ERROR_AUTH_FAILURE",
        'hint': "Please check username and password."
    },
    404: {
        'info': "ERROR_PAGE_NOT_FOUND",
        'hint': "What you want to look up may not exist."
    },
    500: {
        'info': "ERROR_SERVICE_NOT_AVAILABLE",
        'hint': "The server is busy or not available currently.\
                 Please try again later."
    },
}

FURTHER_HELP = "Any further concerns please contact \
                the website maintainer: +61 xxx-xxx-xxx"
