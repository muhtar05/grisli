import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.views import generic
from .models import Link

class LinkList(generic.ListView):
    model = Link

class LinkDetail(generic.DetailView):
    model = Link

    def get_context_data(self, **kwargs):
        context = super(LinkDetail,self).get_context_data(**kwargs)
        req = requests.get(self.object.url)
        soup = BeautifulSoup(req.text,'html.parser')

        h1_markup = soup.select('h1')
        context['encoding'] = req.encoding
        context['status_code'] = req.status_code
        context['h1_title'] = h1_markup
        context['title'] = soup.title.string
        return context

