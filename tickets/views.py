from os.path import join
from django.shortcuts import render, redirect
from django.urls import reverse

from django.views.generic import (
    ListView,
    DetailView,
)

from tools.zendesk import ticket_apis as apis


class TicketListView(ListView):
    template_name = "tickets/ticket_list.html"

    def get(self, request, *args, **kwargs):
        if request.path == '/':
            return redirect(join(request.build_absolute_uri(), 'tickets'))

        status, content = apis().ticket_list()

        context = {
            "status": status,
            "content": content
        }

        return render(request, self.template_name, context)


class TicketDetailView(DetailView):
    template_name = "tickets/ticket_detail.html"

    def get(self, request, id, *args, **kwargs):
        status, content = apis().ticket_detail(id)

        context = {
            "status": status,
            "content": content
        }

        return render(request, self.template_name, context)
