import secrets

import requests
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render

from .models import Table, Log
from config import API_TOKEN


# Create your views here.
def index(request):
    return HttpResponse('<h1>Главная</h1>')


class CallView(View):

    def get(self, request, *args, **kwargs):
        data = kwargs['data']
        table = Table.objects.filter(url=f'https://servemepls.ru/caller/{data}').first()
        return render(request, 'button_page.html', {
            'rest': table.rest.restaurant,
            'vk': table.rest.vk,
            'inst': table.rest.inst,
            'table': table.url,
            'fake_table': secrets.token_hex(16)
        })


class SendNotification(View):

    def post(self, request, *args, **kwargs):
        table = request.POST['session']
        table = Table.objects.filter(url=table).first()
        response = requests.post(
            url=f'https://api.telegram.org/bot{API_TOKEN}/sendMessage',
            data={'chat_id': table.waiter.telegram_id, 'text': f'Столик №{table.number} просит подойти.'}
        ).json()
        log = Log()
        log.table = table.number
        log.restaurant = table.rest.back_ident
        log.save()
        return JsonResponse({
            "result": "success"
        })
