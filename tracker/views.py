from django.shortcuts import render, redirect
from .models import country
import requests
from django.contrib import messages
from django.urls import reverse

def GlobalCovid(request):
    url = 'https://api.covid19api.com/world/total'
    url2 = 'https://api.covid19api.com/summary'

    rGlobal = requests.get(url).json()
    covidKey = requests.get(url2).json()

    if request.method == "POST":
        cntry = request.POST['country']
        country.objects.get_or_create(name=cntry)
        c = country.objects.get(name=cntry)
        return redirect('Country', id=c.id)

    try:
        countries = country.objects.all()
        country_data = []

        for c in countries:
            r = requests.get(url2).json()
            i = -1
            while i < len(r['Countries']):
                i += 1
                if r['Countries'][i]["Country"] == c.name:
                    covid = {
                        'id': c.id,
                        'Country': r['Countries'][i]['Country'],
                        'CountryCode': r['Countries'][i]['CountryCode'],
                        'NewConfirmed': r['Countries'][i]['NewConfirmed'],
                        'TotalConfirmed': r['Countries'][i]['TotalConfirmed'],
                        'NewDeaths': r['Countries'][i]['NewDeaths'],
                        'TotalDeaths': r['Countries'][i]['TotalDeaths'],
                        'NewRecovered': r['Countries'][i]['NewRecovered'],
                        'TotalRecovered': r['Countries'][i]['TotalRecovered'],
                        'Date': r['Countries'][i]['Date'],
                        'ActiveCases': r['Countries'][i]['TotalConfirmed'] - r['Countries'][i]['TotalRecovered'] - r['Countries'][i]['TotalDeaths'] 
                    }
                    country_data.append(covid)
                    break
                
    except KeyError:
        if c.name != r['Countries'][i]['Country']:
            c.delete()
            messages.error(request, 'Sorry, unable to fetch %s due to updating data. try to fetch again later.'%(c.name))
            
        
    covid = {
        'TotalConfirmed' : rGlobal['TotalConfirmed'],
        'TotalDeaths' : rGlobal['TotalDeaths'],
        'TotalRecovered' : rGlobal['TotalRecovered'],
        'ActiveCases': rGlobal['TotalConfirmed'] - rGlobal['TotalRecovered'] - rGlobal['TotalDeaths']
    }
    context = {
        'country_data': country_data,
        'covidKey': covidKey,
        'covid' : covid,
    }

    return render(request, 'GlobalCovid.html', context)

def countryCases(request, id):
    url = 'https://api.covid19api.com/summary'
    covidKey = requests.get(url).json()

    Country = country.objects.get(id=id)
    data = []

    r = requests.get(url).json()
    i = -1
    while i < len(r['Countries']):
        i += 1
        if r['Countries'][i]["Country"] == Country.name:
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
                'ActiveCases': r['Countries'][i]['TotalConfirmed'] - r['Countries'][i]['TotalRecovered'] - r['Countries'][i]['TotalDeaths'] 
            }
            data.append(covid)
            break

    if request.method == "POST":
        cntry = request.POST['country']
        country.objects.get_or_create(name=cntry)
        c = country.objects.get(name=cntry)
        return redirect('Country', id=c.id)

    context={
        'covid': covid,
        'covidKey': covidKey,
        'Country': Country,
    }
    return render(request, 'countryCases.html', context)