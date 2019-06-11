from os.path import join
from django.shortcuts import render, redirect

from django.views.generic import (
    ListView,
    DetailView,
)

from tools.zendesk import ticket_apis as apis


def ret_handler(ret):
    context = {}
    if ret.get('status', ''):
        # response status
        context['status'] = ret['status']
    if ret.get('content', ''):
        # main part of the request when success
        # error message when request failed
        context['content'] = ret['content']
    if ret.get('hint', ''):
        # optional hint for end user while error occur
        context['hint'] = ret['hint'] + " Any further concerns please \
                            contact the website maintainer: +61 xxx-xxx-xxx"

    return context


class TicketListView(ListView):
    template_name = "tickets/ticket_list.html"

    def get(self, request, *args, **kwargs):
        if request.path == '/':
            return redirect(join(request.build_absolute_uri(), 'tickets'))

        ret = apis().ticket_list()
        context = ret_handler(ret)

        return render(request, self.template_name, context)


class TicketDetailView(DetailView):
    template_name = "tickets/ticket_detail.html"

    def get(self, request, id, *args, **kwargs):
        ret = apis().ticket_detail(id)
        context = ret_handler(ret)

        return render(request, self.template_name, context)
