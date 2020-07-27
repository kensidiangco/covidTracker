from django.shortcuts import render
from .models import country
import requests
from django.contrib import messages

def GlobalCovid(request):
    url = 'https://api.covid19api.com/world/total'
    url2 = 'https://api.covid19api.com/summary'

    rGlobal = requests.get(url).json()
    covidKey = requests.get(url2).json()


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
            messages.error(request, 'Sorry, unable to fetch %s due to updating data. try to fetch again later.'%(c.name))

        elif cntry.cleaned_data.get("country") in country_data:
            messages.error(request, '%s already fetched. look at it below'%(c.name))

    covid = {
        'TotalConfirmed' : rGlobal['TotalConfirmed'],
        'TotalDeaths' : rGlobal['TotalDeaths'],
        'TotalRecovered' : rGlobal['TotalRecovered'],
    }
    context = {
        'country_data': country_data,
        'covidKey': covidKey,
        'covid' : covid,
    }

    return render(request, 'GlobalCovid.html', context)