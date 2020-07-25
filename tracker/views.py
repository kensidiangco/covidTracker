from django.shortcuts import render, get_object_or_404, redirect
from .models import country
import requests
from .forms import countryForm
from django.http import HttpResponse

def GlobalCovid(request):
    url = 'https://api.covid19api.com/world/total'
    
    rGlobal = requests.get(url).json()
    
    covid = {
        'TotalConfirmed' : rGlobal['TotalConfirmed'],
        'TotalDeaths' : rGlobal['TotalDeaths'],
        'TotalRecovered' : rGlobal['TotalRecovered'],
    }
    
    context = {
        'covid' : covid
    }
    
    return render(request, 'GlobalCovid.html', context)
    
    
def PHCovid(request):
    url = 'https://api.covid19api.com/summary'
    
    if request.method == "POST":
        form = countryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('PH')
    try:
     countries = country.objects.all()
     
     country_data = []
     
     for c in countries:
         r = requests.get(url).json()
         i = 0
         while i < len(r['Countries']):
             i += 1
             if r['Countries'][i]["Country"] == c.name:
                 covid = {
                     'Country': r['Countries'][i]['Country'],
                     'CountryCode': r['Countries'][i]['CountryCode'],
                     'NewConfirmed': r['Countries'][i]['NewConfirmed'],
                     'TotalConfirmed': r['Countries'][i]['TotalConfirmed'],
                     'NewDeaths': r['Countries'][i]['NewDeaths'],
                     'TotalDeaths': r['Countries'][i]['TotalDeaths'],
                     'NewRecovered': r['Countries'][i]['NewRecovered'],
                     'TotalRecovered': r['Countries'][i]['TotalRecovered'],
                 }
                 country_data.append(covid)
                 break
    except:
     if c.name != r['Countries'][1]['Country']:
      c.delete()
      return HttpResponse('%s is invalid country name. please reload the page.'%(c.name))
      
            
    form = countryForm()
    context = {
        'country_data': country_data,
        'form': form,
    }
    return render(request, 'PHCovid.html', context)
