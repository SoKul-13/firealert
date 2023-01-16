from django.http import HttpResponse
from logging import log
from .apps import FileReloader
from .apps import FireLocator

# Create your views here.
def home(request):
    return HttpResponse("We are home!")

def data(request):
    fl = FileReloader()     
    #count = fl.reloadCsvFile()
    count = fl.reloadFromService()
    return HttpResponse("Data Reloaded." + str(count) +" records added to database")

def zip(request):
    fl = FileReloader()
    count = fl.reloadZipData()
    return HttpResponse("Zip data Reloaded." + str(count) +" records added to database")

def alertdata(request):
    print(" Getting alert.................................... ")
    print(request.POST)
    l1 = request.POST['Longitude']
    l2 = request.POST['Lattitude']
    z= request.POST['zcode']
    print(l1,l2,z)

    f = FireLocator()
    results = f.findFires(l1,l2,z)
    if len(results) == 0:
        return HttpResponse("Found no fires in a 25 mile radius. You are safe!")
    else:
        fires = results[0]
        time = results[1]
        return HttpResponse("Found "+ str(fires)+ " fires in a 25 mile radius. You have "+ str(time)+ " hours to escape the fire.")