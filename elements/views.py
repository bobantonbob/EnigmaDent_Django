from django.shortcuts import render


def index(request):
    return render(request, 'elements/index.html', {
        'title': 'Галерея',
        'page': 'index',
        'app': 'elements'
    })

def certificate(request):
    return render(request, 'elements/certificate.html', {
        'title': 'Сертифікати',
        'page': 'certificate',
        'app': 'elements'
    })

def new1(request):
    return render(request, 'elements/new1.html', {
        'title': 'Новини',
        'page': 'new1',
        'app': 'elements'
    })

def new2(request):
    return render(request, 'elements/new2.html', {
        'title': 'Новини',
        'page': 'new2',
        'app': 'elements'
    })

def new3(request):
    return render(request, 'elements/new3.html', {
        'title': 'Новини',
        'page': 'new3',
        'app': 'elements'
    })