from django.shortcuts import render
import json
import csv
from DailyUpdate import models
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
import matplotlib.pyplot as plt
from .forms import forms
import numpy as np
import datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
import urllib
import base64
from django.views.decorators import csrf
from django.core.files.images import ImageFile
# from StringIO import S


# Create your views here.
def show_homepage(request):

    response = {}

    data1 = models.Country.objects.filter(fullName='World').order_by('-date')[:1]
    total_num = data1[0].total_case
    total_death = data1[0].total_death
    response['total_num'] = total_num
    response['total_death'] = total_death

    confirmed_list = []
    last_date = models.Country.objects.order_by('-date')[:1]
    response['today'] = last_date[0].date
    print("last_date: ", last_date[0].date)
    data3 = models.Country.objects.filter(~Q(fullName='World') & Q(date=last_date[0].date)).order_by('-total_case')
    print(data3.count())

    death_list = []
    data4 = models.Country.objects.filter(~Q(fullName='World') & Q(date=last_date[0].date)).order_by('-total_death')

    for item in data3:
        # print(item.fullName, item.date)
        dic = {}
        dic['country'] = item.fullName
        dic['num'] = item.total_case
        confirmed_list.append(dic)
    response['country_confirmed_list'] = confirmed_list

    for item in data4:
        dic = {}
        dic['country'] = item.fullName
        dic['num'] = item.total_death
        death_list.append(dic)
    response['death_list'] = death_list

    country_num = models.Country.objects.values('fullName').distinct()
    response['country_num'] = country_num.count()

    return JsonResponse(response)


# current solution:
# when click the country, use plot to create the today's charts and save to database, then show the chart from the db;
# if the country has been called before today, then we do not need to plot again, call the chart from database directly
# Tasks:
# 1. save path or file to the db?
# 2. how to save plot?
# 3. how to call the image from db?
def draw_charts(request):
    # to get the parameter of the request
    country = request.GET.get('country')
    state = request.GET.get('chart_state')
    print("country", country)
    print("state", state)
    response = {}
    confirmed = {}
    daily = {}
    month = []

    data = models.Country.objects.filter(fullName=country)
    for item in data:
        # revise the format of the date so that only month information can be seen in te chart
        time = datetime.datetime.strftime(item.date, '%b')
        confirmed[time] = item.total_case
        daily[item.date] = item.new_case
        if time not in month:
            month.append(time)
    print("month:", month)

    # start plotting
    # according to the state of daily or confirmed
    fig = plt.figure(figsize=(7, 4.5))
    plt.rcParams['axes.facecolor'] = '#00b383'

    if state == 'confirmed':
        print("country:", country)
        cons = list(confirmed.values())
        y_lims = (cons[0], cons[-1])
        plt.ylim(y_lims)
        plt.plot(*zip(*confirmed.items()))

        line = plt.legend().get_lines()
        plt.setp(line, linewidth=4)

        # store image in a byte buffer?
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        string = base64.b64encode(buffer.read())
        # uri = urllib.parse.quote(string)
        buffer.close()
        # fig.savefig('/Users/Shawn/PycharmProjects/Covid19_project/images/confirm/' + country.lower() + '.png')

        ta = models.DailySituation.objects.get(name=country)
        ta.confirm_img = string
        ta.save()
        plt.clf()

    elif state == 'daily':
        cons = sorted(list(daily.values()))
        y_lims = (cons[0], cons[-1])
        plt.bar(*zip(*daily.items()))
        plt.ylim(y_lims)
        # store image in a byte buffer?
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        string = base64.b64encode(buffer.read())
        # uri = urllib.parse.quote(string)
        buffer.close()

        ta = models.DailySituation.objects.get(name=country)
        ta.daily_img = string
        ta.save()

        # add this method plot will delete the current curve,
        # without this method, there will be multiple curves in the same page
        plt.clf()

    response['country'] = country
    response['state'] = state
    response['chart'] = str(models.DailySituation.objects.get(name=country).confirm_img)

    return JsonResponse(response)


def import_newest_data(request):
    response = {}

    file = '/Users/Shawn/PycharmProjects/Covid19_project/DailyUpdate/owid-covid-data.json'
    f = open(file)
    data = json.loads(f.read())

    for item in data:
        contents = data[item]
        daily = models.DailySituation(
            name=contents[-1]["location"],
            date=contents[-1]["date"],
        )
        daily.save()

        for ele in contents:
            try:
                if item == 'OWID_WRL':
                    ele['continent'] = 'World'
                    # print("new: ", ele)
                elif not ele['total_cases']:
                    ele['total_cases'] = 0
                elif not ele['new_cases']:
                    ele['new_cases'] = 0
                elif not ele['total_deaths']:
                    ele['total_deaths'] = 0
                elif not ele['new_deaths']:
                    ele['new_deaths'] = 0
                country = models.Country(
                    fullName=ele['location'],
                    shortName=item,
                    continent=ele['continent'],
                    date=ele['date'],
                    total_case=ele['total_cases'],
                    new_case=ele['new_cases'],
                    total_death=ele['total_deaths'],
                    new_death=ele['new_deaths']
                )
                country.save()
            except Exception as e:
                response['msg'] = str(e)
                response['error_num'] = 1

    num = models.Country.objects.count()
    response['data'] = num
    response['msg'] = 'success'
    response['error_num'] = 0

    return JsonResponse(response)


def import_coordinate(request):
    response = {}

    file = '/Users/Shawn/PycharmProjects/Covid19_project/DailyUpdate/country_coordinate.csv'

    with open(file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            record = models.DailySituation.objects.filter(name=row[3])
            if record:
                record[0].lat = row[1]
                record[0].lon = row[2]
                record[0].save()


def delete_data(request):
    models.Country.objects.all().delete()
    models.DailySituation.objects.all().delete()

    return HttpResponse("all the data has been deleted")


def query_data(request):
    response = {}
    pos = []

    country = request.GET.get('country')
    result = models.DailySituation.objects.get(name=country)
    pos = [result.lat, result.lon]

    print("country:", country, "position:", pos)

    response['pos'] = pos
    return JsonResponse(response)
