from django.shortcuts import render



def about(request):
    return render(request, "index.html")

def louis(request):
    return render(request, "louis.html")

def roy(request):
    return render(request, "roy.html")

def sungjun(request):
    return render(request, "sungjun.html")

def antoine(request):
    return render(request, "antoine.html")