from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import country
import requests
from .forms import countryForm
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse

def GlobalCovid(request):
    url = 'https://api.covid19api.com/world/total'
    url2 = 'https://api.covid19api.com/summary'
    countries = country.objects.all()
    rGlobal = requests.get(url).json()

    if request.method == "POST":
        cntry = request.POST['country']

        country.objects.get_or_create(name=cntry)

    try:
        countries = country.objects.all()
        country_data = []
        for c in countries:
            r = requests.get(url2).json()
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
                        'Date': r['Countries'][i]['Date'],
                    }
                    country_data.append(covid)
                    break
    except:
        if c.name != r['Countries'][1]['Country']:
            c.delete()
            messages.error(request, 'Sorry, unable to fetch %s data.'%(c.name))
            form = countryForm()
            context = {
                'country_data': country_data,
                'form': form,
                'covidKey': covidKey
            }
            return render(request, 'countriesCases.html', context)
    
    covid = {
        'TotalConfirmed' : rGlobal['TotalConfirmed'],
        'TotalDeaths' : rGlobal['TotalDeaths'],
        'TotalRecovered' : rGlobal['TotalRecovered'],
    }
    covidKey = requests.get(url2).json()

    form = countryForm()
    context = {
        'country_data': country_data,
        'form': form,
        'covidKey': covidKey,
        'covid' : covid
    }
    
    return render(request, 'GlobalCovid.html', context)
    
    
def countriesCases(request):
    url2 = 'https://api.covid19api.com/summary'
    
    if request.method == "POST":
        cntry = request.POST['country']

        country.objects.get_or_create(name=cntry)



    try:
     countries = country.objects.all()
     
     country_data = []
     
     for c in countries:
         r = requests.get(url2).json()
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
                     'Date': r['Countries'][i]['Date'],
                 }
                 country_data.append(covid)
                 break
    except:
        if c.name != r['Countries'][1]['Country']:
            c.delete()
            messages.error(request, 'Sorry, unable to fetch %s data.'%(c.name))
            form = countryForm()
            context = {
                'country_data': country_data,
                'form': form,
                'covidKey': covidKey
            }
            return render(request, 'countriesCases.html', context)
      
    covidKey = requests.get(url2).json()

    form = countryForm()
    context = {
        'country_data': country_data,
        'form': form,
        'covidKey': covidKey
    }
    return render(request, 'countriesCases.html', context)
