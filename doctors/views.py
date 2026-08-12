from django.shortcuts import render


def index(request):
    return render(request, 'doctors/index.html', {
        'title': 'Спеціалісти',
        'page': 'index',
        'app': 'doctors'
    })


