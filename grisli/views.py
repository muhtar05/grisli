import urllib.request as urllib2
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    res = urllib2.urlopen('http://driantina.ru')
    soup = BeautifulSoup(res)
    links = []

    for link in soup.find_all('a'):
        links.append(link.get('href'))

    return render(request, 'grisli/home.html', {'links': links})
