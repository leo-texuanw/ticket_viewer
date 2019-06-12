import requests
from requests.exceptions import HTTPError, RequestException
from time import gmtime, strftime

from . import api_secret_config as cfg


class Zendesk():
    """ Base class for Zendesk APIs """

    def __init__(self, subdomain, user, passwd):
        API_VERSION = "v2"

        self.user = user
        self.passwd = passwd
        self.API_URL = f"https://{subdomain}.zendesk.com/api/{API_VERSION}"

        self.OK = "OK"
        self.ERROR = "ERROR"
        self.TIME_FORMAT = "%m/%d/%Y %H:%M:%S"

    def request(self, api_name, url):
        """ Handle requests """

        ret = {}
        try:
            response = requests.get(url, auth=(self.user, self.passwd))
            response.raise_for_status()

            ret['status'] = self.OK
            try:
                ret['content'] = response.json()
            except Exception:
                ret['status'] = self.ERROR
                ret['content'] = "Unexpected return from the server"

        except HTTPError as http_err:
            # unsuccessful status code
            self.record_error(api_name, http_err)

            if response.status_code == 401:
                ret['status'] = "ERROR_AUTH_FAILURE"
                ret['hint'] = "Incorrect username and password."
            elif response.status_code == 404:
                ret['status'] = "ERROR_PAGE_NOT_FOUND"
                ret['hint'] = "What you want to look up may not exist."
            elif response.status_code >= 500:
                ret['status'] = "ERROR_SERVICE_NOT_AVAILABLE"
                ret['hint'] = "The server is busy or not available currently.\
                        Please try again later."
            else:
                print(response.status_code)
            ret['content'] = str(http_err)

        except RequestException as request_err:
            # unexpected error caused by requests
            self.record_error(api_name, request_err)
            ret['status'], ret['content'] = self.ERROR, str(request_err)
        except UnicodeError as unicode_err:
            self.record_error(api_name, unicode_err)
            ret['status'] = self.ERROR
            ret['hint'] = "Failed encode the url. Have you setup \
                           your SUBDOMAIN correctly?"
            ret['content'] = str(unicode_err)
        except Exception as err:
            # catch all unexpected errors
            self.record_error(api_name, err)
            ret['status'], ret['content'] = self.ERROR, str(err)

        return ret

    def record_error(self, api_name, err_msg):
        """ Currently only print to terminal """

        time = strftime(self.TIME_FORMAT, gmtime())
        err_header = f"[ERROR({time})] - {api_name} -"

        print(err_header, err_msg)


class ZendeskTickets(Zendesk):
    """ Tickets module of Zendesk APIs """

    def __init__(self, subdomain, user, passwd):
        Zendesk.__init__(self, subdomain, user, passwd)

        API_MODULE = "tickets"
        self.MOD_URL = f"{self.API_URL}/{API_MODULE}"

    def ticket_list(self):
        url = f"{self.API_URL}/tickets.json"
        return self.request("ticket_list", url)

    def ticket_detail(self, id):
        if not (isinstance(id, int) or id.isdigit()):
            return {
                'status': self.ERROR,
                'content': "ticket_id must be numbers"
            }

        url = f"{self.MOD_URL}/{id}.json"
        return self.request("ticket_detail", url)


def ticket_apis():
    return ZendeskTickets(cfg.SUBDOMAIN, cfg.USER, cfg.PASSWD)
