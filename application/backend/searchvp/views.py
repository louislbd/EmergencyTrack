from django.shortcuts import render
from .models import Countys, Users
from django.db.models import Q


def search_results(request):
    if request.method == "POST":
        searched = request.POST['searched']
        category = request.POST['search_category']
        if category == "countys":
            if searched == "":
                results = Countys.objects.all()
            else:
                results = Countys.objects.filter(county_name__icontains=searched)
        elif category == "users":
            if searched == "":
                results = Users.objects.all()
            else:
                results = Users.objects.filter(Q(first_name__icontains=searched) |
                                               Q(last_name__icontains=searched))
        return render(request, 'search_results.html',
                      {'searched': searched,
                       'results': results,
                       'category': category})
    return render(request, 'search.html', {})


def search(request):
    return render(request, 'search.html', {})
