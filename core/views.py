from django.shortcuts import render
import requests
import json
import os



RAPID_API_KEY =  os.environ['RAPID_API_KEY']

url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
    'x-rapidapi-key': RAPID_API_KEY,
    'x-rapidapi-host': "covid-193.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers).json()

# Create your views here.


def indexView(request):
    listNations = []
    noofresults = int(response['results'])

    for x in range(0, noofresults):

        listNations.append(response['response'][x]['country'])
    valueBrazil = listNations.index('Brazil')
    if request.method == "POST":
        selectedcountry = request.POST['selectedcountry']

        for x in range(0, noofresults):
            if selectedcountry == response['response'][x]['country']:
                new = response['response'][x]['cases']['new']
                active = response['response'][x]['cases']['active']
                critical = response['response'][x]['cases']['critical']
                recovered = response['response'][x]['cases']['recovered']
                total = response['response'][x]['cases']['total']
                if new == None:
                    new = '-'
                if active == None:
                    active = '-'
                if critical == None:
                    critical = '-'
                if recovered == None:
                    recovered = '-'
                if total == None:
                    total = '-'
                try:
                    deaths = int(total)-int(active)-int(recovered)
                except:
                    deaths = '-'

        context = {'selectedcountry': selectedcountry, 'listNations': listNations, 'new': new, 'active': active,
                   'critical': critical, 'recovered': recovered, 'deaths': deaths, 'total': total}
        return render(request, 'index.html', context)

    
    new = response['response'][valueBrazil]['cases']['new']
    active = response['response'][valueBrazil]['cases']['active']
    critical = response['response'][valueBrazil]['cases']['critical']
    recovered = response['response'][valueBrazil]['cases']['recovered']
    total = response['response'][valueBrazil]['cases']['total']
    deaths = int(total)-int(active)-int(recovered)

    context = {'selectedcountry': 'Brazil', 'listNations':listNations, 'new': new, 'active': active,
                   'critical': critical, 'recovered': recovered, 'deaths': deaths, 'total': total}

    return render(request, 'index.html', context)
