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

    def request(self, api, url):
        """ Handle requests """

        try:
            response = requests.get(url, auth=(self.user, self.passwd))
            response.raise_for_status()

            status = self.OK
            try:
                content = response.json()
            except Exception:
                status = self.ERROR
                content = "Unexpected return from the server"

        except HTTPError as http_err:
            # unsuccessful status code
            self.record_error(api, http_err)
            status = self.ERROR

            if response.status_code == 401:
                status += "_AUTH_FAILURE"
            elif response.status_code == 404:
                status += "_PAGE_NOT_FOUND"

            content = str(http_err)

        except RequestException as request_err:
            # unexpected error caused by requests
            self.record_error(api, request_err)
            status, content = self.ERROR, str(request_err)
        except Exception as err:
            # catch all unexpected errors
            self.record_error(api, err)
            status, content = self.ERROR, str(err)

        return (status, content)

    def record_error(self, api, err_msg):
        """ Currently only print to terminal """
        time = strftime(self.TIME_FORMAT, gmtime())
        err_header = f"[ERROR({time})] - {api} -"

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
        assert(isinstance(id, int) or id.isdigit())

        url = f"{self.MOD_URL}/{id}.json"
        return self.request("ticket_detail", url)


def ticket_apis():
    assert(isinstance(cfg.SUBDOMAIN, str))
    assert(isinstance(cfg.USER, str))
    assert(isinstance(cfg.PASSWD, str))
    return ZendeskTickets(cfg.SUBDOMAIN, cfg.USER, cfg.PASSWD)
