from django.test import TestCase

from . import api_secret_config as cfg
from .zendesk import ZendeskTickets as ZendeskTickets


class ZendeskTicketsTest(TestCase):
    """ Test cases for Zendesk apis """
    OK = 'OK'
    ERROR = 'ERROR'

    RESPONSE_ELEMS_SUCC = ['status', 'content']
    RESPONSE_ELEMS_FAIL = ['status', 'hint', 'content']

    TICKET_LIST_ELEMS = ['tickets', 'next_page', 'previous_page', 'count']

    exist_ticket_id = 1

    def test_ticket_list(self):
        api = ZendeskTickets(cfg.SUBDOMAIN, cfg.USER, cfg.PASSWD)
        res = api.ticket_list()
        # better way? what if returned list of tickets are empty?
        self.exist_ticket_id = res['content']['tickets'][0]['id']

        self.assertEqual(list(res.keys()), self.RESPONSE_ELEMS_SUCC)
        self.assertIs(res['status'], self.OK)
        self.assertEqual(list(res['content'].keys()),
                         self.TICKET_LIST_ELEMS)

    def test_empty_subdomain(self):
        api = ZendeskTickets("", cfg.USER, cfg.PASSWD)
        res = api.ticket_list()

        self.assertEqual(list(res.keys()), self.RESPONSE_ELEMS_FAIL)
        self.assertIs(res['status'], self.ERROR)

    def test_wrong_subdomain(self):
        api = ZendeskTickets("incorrect_subdomain", cfg.USER, cfg.PASSWD)
        res = api.ticket_list()

        self.assertEqual(list(res.keys()), self.RESPONSE_ELEMS_FAIL)
        self.assertIs(res['status'], 'ERROR_PAGE_NOT_FOUND')

    def test_auth_failure_by_empty_username(self):
        api = ZendeskTickets(cfg.SUBDOMAIN, "", cfg.PASSWD)
        res = api.ticket_list()

        self.assertEqual(list(res.keys()), self.RESPONSE_ELEMS_FAIL)
        self.assertIs(res['status'], 'ERROR_AUTH_FAILURE')

    def test_auth_failure_by_username(self):
        api = ZendeskTickets(cfg.SUBDOMAIN, "incorrect_user", cfg.PASSWD)
        res = api.ticket_list()

        self.assertEqual(list(res.keys()), self.RESPONSE_ELEMS_FAIL)
        self.assertIs(res['status'], 'ERROR_AUTH_FAILURE')

    def test_auth_failure_by_password(self):
        api = ZendeskTickets(cfg.SUBDOMAIN, cfg.USER, "incorrect_passwd")
        res = api.ticket_list()

        self.assertEqual(list(res.keys()), self.RESPONSE_ELEMS_FAIL)
        self.assertIs(res['status'], 'ERROR_AUTH_FAILURE')

    def test_ticket_detail(self):
        api = ZendeskTickets(cfg.SUBDOMAIN, cfg.USER, cfg.PASSWD)
        res = api.ticket_detail(self.exist_ticket_id)

        self.assertEqual(list(res.keys()), self.RESPONSE_ELEMS_SUCC)
        self.assertIs(res['status'], self.OK)
        self.assertEqual(list(res['content'].keys()), ['ticket'])

    def test_ticket_detail_with_not_exist_digit_id(self):
        api = ZendeskTickets(cfg.SUBDOMAIN, cfg.USER, cfg.PASSWD)
        res = api.ticket_detail(1298734912374)  # a randaom number

        self.assertIs(res['status'], 'ERROR_PAGE_NOT_FOUND')

    def test_ticket_detail_with_non_digit_id(self):
        api = ZendeskTickets(cfg.SUBDOMAIN, cfg.USER, cfg.PASSWD)
        res = api.ticket_detail("not_digit")

        self.assertIs(res['status'], self.ERROR)
