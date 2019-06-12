from os.path import join
from django.shortcuts import render, redirect

from django.views.generic import (
    ListView,
    DetailView,
)

from ticket_viewer.zendesk import ticket_apis as apis
from ticket_viewer import resp_status as status


def ret_handler(ret):
    """ hndle return from Zendesk module """

    context = {}

    if not ret.get('status', ''):
        context['status'] = status.ERROR
    else:
        # response status
        context['status'] = ret['status']

        if context['status'] != status.OK:
            # add configurated hints for end user while error occur

            if ret.get('hint', ""):
                # ret already with hint
                context['hint'] = ret['hint']
            else:
                # go to default config file 'resp_status' for hint
                details = status.STATUS_CODE.get(ret['status'], {})
                context['hint'] = details.get('hint', "")

            context['hint'] += status.FURTHER_HELP

    if ret.get('content', ''):
        # content is the main part of the response when success,
        # or error message when request failed
        context['content'] = ret['content']
    else:
        # error by zendesk.py
        context['content'] = "INTERNAL_ERROR"

    return context


class TicketListView(ListView):
    template_name = "tickets/ticket_list.html"

    def get(self, request, *args, **kwargs):
        if request.path == '/':
            return redirect(join(request.build_absolute_uri(), 'tickets'))

        ret = apis().ticket_list(request.GET.get('page'))
        context = ret_handler(ret)

        # replace returned prev/next urls with prev/next page number, if exist
        prev_page = context.get('content', {}).get('previous_page', None)
        next_page = context.get('content', {}).get('next_page', None)
        if prev_page:
            context['content']['previous_page'] = prev_page.split('=')[-1]
        if next_page:
            context['content']['next_page'] = next_page.split('=')[-1]

        return render(request, self.template_name, context)


class TicketDetailView(DetailView):
    template_name = "tickets/ticket_detail.html"

    def get(self, request, id, *args, **kwargs):
        ret = apis().ticket_detail(id)
        context = ret_handler(ret)

        return render(request, self.template_name, context)
