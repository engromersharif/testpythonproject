from ast import Pass
from django.db.models import Count
from pandasdemo.models import Ethanol
from django.db.models.functions import Round
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from itertools import count
from math import ceil, floor
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.contrib import messages
from numpy import integer
from .forms import EthanolForm
from .models import*
import datetime
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd
pd.options.display.float_format = '{:,}'.format


# Login View
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully !!')
                    return HttpResponseRedirect('/')
        else:
            fm = AuthenticationForm()
        return render(request, 'pandasdemo/userlogin.html', {'form': fm})
    else:
        return HttpResponseRedirect('/')


# Logout View
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        item = Ethanol.objects.all().values()
        try:
            by_year = Ethanol.objects.filter(Year__gte='2017').values('Year').order_by(
                'Year').annotate(QTYMT=(Sum('QTYMT')),VALUEUSD=Sum('VALUEUSD'))

            list_items = Ethanol.objects.filter(
                Date__gte=datetime.date(2022, 6, 1))

            my_count = Ethanol.objects.filter(Year__gte='2013').values(
                'Year').order_by('Year').annotate(TotalCount=Count('QTYMT'))

            labels = []
            Values = []

            for item in my_count:
                labels.append(item['Year'])

            for item in my_count:
                Values.append(item['TotalCount'])

        except:
            pass

        mydict = {
            "list_items": list_items,
            "by_year": by_year,
            "my_count": my_count,
            "labels": labels,
            "Values": Values
        }
        return render(request, 'pandasdemo/index.html', context=mydict)
    else:
        return HttpResponseRedirect('login')


def analysis1(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            selected_year = int(request.POST["yearofthedragon"])
            item = Ethanol.objects.all().values()

            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()

            New_Ethanol_df = Ethanol_df[Ethanol_df['Year'] == selected_year]
            New_Ethanol_df['Month'] = pd.Categorical(New_Ethanol_df['Month'], categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                                                                          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                                                     ordered=True)
            try:
                summ = New_Ethanol_df.groupby(['Month'])[
                    ['QTYMT', 'VALUEUSD']].sum()
                summ.rename(columns={'QTYMT': 'Total QTYMT',
                            'VALUE USD': 'TotalValueUSD'}, inplace=True)

                maximum = New_Ethanol_df.groupby(
                    ['Month'])[['QTYMT', 'VALUEUSD']].max()
                maximum.rename(columns={'QTYMT': 'MaximumQTYMT',
                                        'VALUEUSD': 'Maximum VALUEUSD'}, inplace=True)

                minimum = New_Ethanol_df.groupby(
                    ['Month'])[['QTYMT', 'VALUEUSD']].min()
                minimum.rename(columns={'QTYMT': 'MinimumQTYMT',
                                        'VALUEUSD': 'Minimum VALUEUSD'}, inplace=True)

                intermediate_join = pd.merge(
                    summ, maximum, how='inner', on=["Month"])

                df_y_m = pd.merge(intermediate_join, minimum,
                                  how='inner', on=["Month"])

                df_y_m = df_y_m.fillna(0).astype(float).round(1)
            except:
                pass

            dict = {'selected_year': selected_year, 'year_dropdown': year_dropdown,
                    'df_y_m': df_y_m.to_html(
                        classes="table table-bordered")}
            return render(request, 'pandasdemo/analysis1.html', dict)

        else:
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()
            dict = {'selected_year': "Waiting for Selection...",
                    'year_dropdown': year_dropdown, }
            return render(request, 'pandasdemo/analysis1.html', dict)

    else:
        return HttpResponseRedirect('/')


def analysis2(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            selected_year = int(request.POST["analysis2"])
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()

            New_Ethanol_df = Ethanol_df[Ethanol_df["Year"] == selected_year]
            New_Ethanol_df['Month'] = pd.Categorical(New_Ethanol_df['Month'], categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                                                                          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                                                     ordered=True)
            try:
                summ = New_Ethanol_df.groupby(['REGION'])[
                    ['QTYMT', 'VALUEUSD']].sum()
                summ.rename(columns={'QTYMT': 'Total QTY(MT)',
                            'VALUEUSD': 'Total Value(USD)'}, inplace=True)

                maximum = New_Ethanol_df.groupby(
                    ['REGION'])[['QTYMT', 'VALUEUSD']].max()
                maximum.rename(columns={'QTYMT': 'Maximum QTY(MT)',
                                        'VALUEUSD': 'Maximum VALUE(USD)'}, inplace=True)

                minimum = New_Ethanol_df.groupby(
                    ['REGION'])[['QTYMT', 'VALUEUSD']].min()
                minimum.rename(columns={'QTYMT': 'Minimum QTY(MT)',
                                        'VALUEUSD': 'Minimum VALUE(USD)'}, inplace=True)

                intermediate_join = pd.merge(
                    summ, maximum, how='inner', on=["REGION"])

                df_region = pd.merge(intermediate_join, minimum,
                                     how='inner', on=["REGION"])
                df_region = df_region.sort_values(
                    by='Total QTY(MT)', ascending=False)
                df_region = df_region.fillna(0).astype(float).round(2)

            except:
                pass

            dict = {'df_region': df_region.to_html(
                classes="table table-bordered"), 'selected_year': selected_year, 'year_dropdown': year_dropdown}
            return render(request, 'pandasdemo/analysis2.html', dict)

        else:
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()
            dict = {'selected_year': "Waiting For Selection...",
                    'year_dropdown': year_dropdown}
            return render(request, 'pandasdemo/analysis2.html', dict)
    else:
        return HttpResponseRedirect('/')


def analysis3(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            selected_year = int(request.POST["analysis3"])
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()

            New_Ethanol_df = Ethanol_df[Ethanol_df["Year"] == selected_year]
            New_Ethanol_df['Month'] = pd.Categorical(New_Ethanol_df['Month'], categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                                                                          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                                                     ordered=True)
            try:
                summ = New_Ethanol_df.groupby(['Product'])[
                    ['QTYMT', 'VALUEUSD']].sum()
                summ.rename(columns={'QTYMT': 'Total QTY(MT)',
                            'VALUEUSD': 'Total Value(USD)'}, inplace=True)

                maximum = New_Ethanol_df.groupby(
                    ['Product'])[['QTYMT', 'VALUEUSD']].max()
                maximum.rename(columns={'QTYMT': 'Maximum QTY(MT)',
                                        'VALUEUSD': 'Maximum VALUE(USD)'}, inplace=True)

                minimum = New_Ethanol_df.groupby(
                    ['Product'])[['QTYMT', 'VALUEUSD']].min()
                minimum.rename(columns={'QTYMT': 'Minimum QTY(MT)',
                                        'VALUEUSD': 'Minimum VALUE(USD)'}, inplace=True)

                intermediate_join = pd.merge(
                    summ, maximum, how='inner', on=["Product"])

                df_product = pd.merge(intermediate_join, minimum,
                                      how='inner', on=["Product"])
                df_product = df_product.sort_values(
                    by='Total QTY(MT)', ascending=False)
                df_product = df_product.fillna(0).astype(float).round(2)
            except:
                pass

            dict = {'df_product': df_product.to_html(
                classes="table table-bordered"), 'selected_year': selected_year, 'year_dropdown': year_dropdown}
            return render(request, 'pandasdemo/analysis3.html', dict)
        else:
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()
            dict = {'selected_year': "Waiting For Selection...",
                    'year_dropdown': year_dropdown}
            return render(request, 'pandasdemo/analysis3.html', dict)
    else:
        return HttpResponseRedirect('/')


def analysis4(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            selected_year = int(request.POST["analysis4"])
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()

            New_Ethanol_df = Ethanol_df[Ethanol_df["Year"] == selected_year]
            New_Ethanol_df['Month'] = pd.Categorical(New_Ethanol_df['Month'], categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                                                                          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                                                     ordered=True)
            try:
                summ = New_Ethanol_df.groupby(['COUNTRY'])[
                    ['QTYMT', 'VALUEUSD']].sum()
                summ.rename(columns={'QTYMT': 'Total QTY(MT)',
                            'VALUEUSD': 'Total Value(USD)'}, inplace=True)

                maximum = New_Ethanol_df.groupby(
                    ['COUNTRY'])[['QTYMT', 'VALUEUSD']].max()
                maximum.rename(columns={'QTYMT': 'Maximum QTY(MT)',
                                        'VALUEUSD': 'Maximum VALUE(USD)'}, inplace=True)

                minimum = New_Ethanol_df.groupby(
                    ['COUNTRY'])[['QTYMT', 'VALUEUSD']].min()
                minimum.rename(columns={'QTYMT': 'Minimum QTY(MT)',
                                        'VALUEUSD': 'Minimum VALUE(USD)'}, inplace=True)

                intermediate_join = pd.merge(
                    summ, maximum, how='inner', on=["COUNTRY"])

                df_country = pd.merge(intermediate_join, minimum,
                                      how='inner', on=["COUNTRY"])
                df_country = df_country.sort_values(
                    by='Total QTY(MT)', ascending=False)
                df_country = df_country.fillna(0).astype(float).round(2)
            except:
                pass

            dict = {'df_country': df_country.to_html(
                classes="table table-bordered"), 'selected_year': selected_year, 'year_dropdown': year_dropdown}
            return render(request, 'pandasdemo/analysis4.html', dict)
        else:
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()
            dict = {'selected_year': "Waiting For Selection...",
                    'year_dropdown': year_dropdown}
            return render(request, 'pandasdemo/analysis4.html', dict)
    else:
        return HttpResponseRedirect('/')


def analysis5(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            selected_year = int(request.POST["analysis5"])
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()

            New_Ethanol_df = Ethanol_df[Ethanol_df["Year"] == selected_year]
            New_Ethanol_df['Month'] = pd.Categorical(New_Ethanol_df['Month'], categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                                                                          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                                                     ordered=True)
            try:

                summ = New_Ethanol_df.groupby(['EXPORTER'])[
                    ['QTYMT', 'VALUEUSD']].sum()
                summ.rename(columns={'QTYMT': 'Total QTY(MT)',
                            'VALUEUSD': 'Total Value(USD)'}, inplace=True)

                maximum = New_Ethanol_df.groupby(
                    ['EXPORTER'])[['QTYMT', 'VALUEUSD']].max()
                maximum.rename(columns={'QTYMT': 'Maximum QTY(MT)',
                                        'VALUEUSD': 'Maximum VALUE(USD)'}, inplace=True)

                minimum = New_Ethanol_df.groupby(
                    ['EXPORTER'])[['QTYMT', 'VALUEUSD']].min()
                minimum.rename(columns={'QTYMT': 'Minimum QTY(MT)',
                                        'VALUEUSD': 'Minimum VALUE(USD)'}, inplace=True)

                intermediate_join = pd.merge(
                    summ, maximum, how='inner', on=["EXPORTER"])

                df_exporter = pd.merge(
                    intermediate_join, minimum, how='inner', on=["EXPORTER"])

                df_exporter = df_exporter.sort_values(
                    by='Total QTY(MT)', ascending=False)
                df_exporter = df_exporter.fillna(0).astype(float).round(2)
            except:
                pass

            dict = {'df_exporter': df_exporter.to_html(
                classes="table table-bordered"), 'selected_year': selected_year, 'year_dropdown': year_dropdown}

            return render(request, 'pandasdemo/analysis5.html', dict)
        else:
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()
            dict = {'selected_year': "Waiting For Selection...",
                    'year_dropdown': year_dropdown}
            return render(request, 'pandasdemo/analysis5.html', dict)
    else:
        return HttpResponseRedirect('/')


def analysis6(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            selected_year = int(request.POST["analysis6"])
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()

            New_Ethanol_df = Ethanol_df[Ethanol_df["Year"] == selected_year]
            New_Ethanol_df['Month'] = pd.Categorical(New_Ethanol_df['Month'], categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                                                                          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                                                     ordered=True)
            try:
                summ = New_Ethanol_df.groupby(['IMPORTER'])[
                    ['QTYMT', 'VALUEUSD']].sum()
                summ.rename(columns={'QTYMT': 'Total QTY(MT)',
                            'VALUEUSD': 'Total Value(USD)'}, inplace=True)

                maximum = New_Ethanol_df.groupby(
                    ['IMPORTER'])[['QTYMT', 'VALUEUSD']].max()
                maximum.rename(columns={'QTYMT': 'Maximum QTY(MT)',
                                        'VALUEUSD': 'Maximum VALUE(USD)'}, inplace=True)

                minimum = New_Ethanol_df.groupby(
                    ['IMPORTER'])[['QTYMT', 'VALUEUSD']].min()
                minimum.rename(columns={'QTYMT': 'Minimum QTY(MT)',
                                        'VALUEUSD': 'Minimum VALUE(USD)'}, inplace=True)

                intermediate_join = pd.merge(
                    summ, maximum, how='inner', on=["IMPORTER"])

                df_importer = pd.merge(
                    intermediate_join, minimum, how='inner', on=["IMPORTER"])

                df_importer = df_importer.sort_values(
                    by='Total QTY(MT)', ascending=False)

                df_importer = df_importer.fillna(0).astype(float).round(2)
            except:
                pass

            dict = {'df_importer': df_importer.to_html(
                classes="table table-bordered"), 'selected_year': selected_year, 'year_dropdown': year_dropdown}
            return render(request, 'pandasdemo/analysis6.html', dict)
        else:
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()
            dict = {'selected_year': "Waiting For Selection...",
                    'year_dropdown': year_dropdown}
            return render(request, 'pandasdemo/analysis6.html', dict)
    else:
        return HttpResponseRedirect('/')


def analysis7(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            selected_year = int(request.POST["analysis7y"])
            selected_month = request.POST['analysis7m']
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)

            year_dropdown = Ethanol_df['Year'].unique()
            month_dropdown = Ethanol_df['Month'].unique()

            New_Ethanol_df = Ethanol_df[Ethanol_df["Year"] == selected_year]
            New_Ethanol_dff = New_Ethanol_df[New_Ethanol_df["Month"]
                                             == selected_month]

            try:
                summ = New_Ethanol_dff.groupby(['Product'])[
                    ['QTYMT', 'VALUEUSD']].sum()
                summ.rename(columns={'QTYMT': 'Total QTY(MT)',
                            'VALUEUSD': 'Total Value(USD)'}, inplace=True)

                maximum = New_Ethanol_dff.groupby(
                    ['Product'])[['QTYMT', 'VALUEUSD']].max()
                maximum.rename(columns={'QTYMT': 'Maximum QTY(MT)',
                                        'VALUEUSD': 'Maximum VALUE(USD)'}, inplace=True)

                minimum = New_Ethanol_dff.groupby(
                    ['Product'])[['QTYMT', 'VALUEUSD']].min()
                minimum.rename(columns={'QTYMT': 'Minimum QTY(MT)',
                                        'VALUEUSD': 'Minimum VALUE(USD)'}, inplace=True)

                intermediate_join = pd.merge(
                    summ, maximum, how='inner', on=["Product"])

                df_product_m = pd.merge(
                    intermediate_join, minimum, how='inner', on=["Product"])
                df_product_m = df_product_m.sort_values(
                    by='Total QTY(MT)', ascending=False)
                df_product_m = df_product_m.fillna(0).astype(float).round(2)
            except:
                pass

            dict = {'df_product_m': df_product_m.to_html(
                classes="table table-bordered"), 'selected_year': selected_year, 'selected_month': selected_month, 'year_dropdown': year_dropdown, 'month_dropdown': month_dropdown}
            return render(request, 'pandasdemo/analysis7.html', dict)
        else:
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()
            month_dropdown = Ethanol_df['Month'].unique()
            dict = {'selected_year': "Waiting For Selection...",
                    'year_dropdown': year_dropdown, 'month_dropdown': month_dropdown}
            return render(request, 'pandasdemo/analysis7.html', dict)
    else:
        return HttpResponseRedirect('/')


def analysis8(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            selected_year = int(request.POST["analysis8y"])
            selected_month = request.POST['analysis8m']
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()
            month_dropdown = Ethanol_df['Month'].unique()

            New_Ethanol_df = Ethanol_df[Ethanol_df["Year"] == selected_year]
            New_Ethanol_dff = New_Ethanol_df[New_Ethanol_df["Month"]
                                             == selected_month]
            try:

                summ = New_Ethanol_dff.groupby(['REGION'])[
                    ['QTYMT', 'VALUEUSD']].sum()
                summ.rename(columns={'QTYMT': 'Total QTY(MT)',
                            'VALUEUSD': 'Total Value(USD)'}, inplace=True)

                maximum = New_Ethanol_dff.groupby(
                    ['REGION'])[['QTYMT', 'VALUEUSD']].max()
                maximum.rename(columns={'QTYMT': 'Maximum QTY(MT)',
                                        'VALUEUSD': 'Maximum VALUE(USD)'}, inplace=True)

                minimum = New_Ethanol_dff.groupby(
                    ['REGION'])[['QTYMT', 'VALUEUSD']].min()
                minimum.rename(columns={'QTYMT': 'Minimum QTY(MT)',
                                        'VALUEUSD': 'Minimum VALUE(USD)'}, inplace=True)

                intermediate_join = pd.merge(
                    summ, maximum, how='inner', on=["REGION"])

                df_region_m = pd.merge(
                    intermediate_join, minimum, how='inner', on=["REGION"])
                df_region_m = df_region_m.sort_values(
                    by='Total QTY(MT)', ascending=False)
                df_region_m = df_region_m.fillna(0).astype(float).round(2)

            except:
                pass

            dict = {'df_region_m': df_region_m.to_html(
                    classes="table table-bordered"), 'selected_year': selected_year, 'selected_month': selected_month, 'year_dropdown': year_dropdown, 'month_dropdown': month_dropdown}
            return render(request, 'pandasdemo/analysis8.html', dict)
        else:
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()
            month_dropdown = Ethanol_df['Month'].unique()
            dict = {'selected_year': "Waiting For Selection...",
                    'year_dropdown': year_dropdown, 'month_dropdown': month_dropdown}
            return render(request, 'pandasdemo/analysis8.html', dict)
    else:
        return HttpResponseRedirect('/')


def analysis9(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            selected_year = int(request.POST["analysis9y"])
            selected_month = request.POST['analysis9m']
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()
            month_dropdown = Ethanol_df['Month'].unique()

            New_Ethanol_df = Ethanol_df[Ethanol_df["Year"] == selected_year]
            New_Ethanol_dff = New_Ethanol_df[New_Ethanol_df["Month"]
                                             == selected_month]
            try:
                summ = New_Ethanol_dff.groupby(['COUNTRY'])[
                    ['QTYMT', 'VALUEUSD']].sum()
                summ.rename(columns={'QTYMT': 'Total QTY(MT)',
                            'VALUEUSD': 'Total Value(USD)'}, inplace=True)

                maximum = New_Ethanol_dff.groupby(
                    ['COUNTRY'])[['QTYMT', 'VALUEUSD']].max()
                maximum.rename(columns={'QTYMT': 'Maximum QTY(MT)',
                                        'VALUEUSD': 'Maximum VALUE(USD)'}, inplace=True)

                minimum = New_Ethanol_dff.groupby(
                    ['COUNTRY'])[['QTYMT', 'VALUEUSD']].min()
                minimum.rename(columns={'QTYMT': 'Minimum QTY(MT)',
                                        'VALUEUSD': 'Minimum VALUE(USD)'}, inplace=True)

                intermediate_join = pd.merge(
                    summ, maximum, how='inner', on=["COUNTRY"])

                df_country_m = pd.merge(
                    intermediate_join, minimum, how='inner', on=["COUNTRY"])
                df_country_m = df_country_m.sort_values(
                    by='Total QTY(MT)', ascending=False)
                df_country_m = df_country_m.fillna(0).astype(float).round(2)

            except:
                pass

            dict = {'df_country_m': df_country_m.to_html(
                classes="table table-bordered"), 'selected_year': selected_year, 'selected_month': selected_month, 'year_dropdown': year_dropdown, 'month_dropdown': month_dropdown}
            return render(request, 'pandasdemo/analysis9.html', dict)
        else:
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()
            month_dropdown = Ethanol_df['Month'].unique()
            dict = {'selected_year': "Waiting For Selection...",
                    'year_dropdown': year_dropdown, 'month_dropdown': month_dropdown}
            return render(request, 'pandasdemo/analysis9.html', dict)
    else:
        return HttpResponseRedirect('/')


def analysis10(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            selected_year = int(request.POST["analysis10y"])
            selected_month = request.POST['analysis10m']
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()
            month_dropdown = Ethanol_df['Month'].unique()

            New_Ethanol_df = Ethanol_df[Ethanol_df["Year"] == selected_year]
            New_Ethanol_dff = New_Ethanol_df[New_Ethanol_df["Month"]
                                             == selected_month]

            try:
                summ = New_Ethanol_dff.groupby(['EXPORTER'])[
                    ['QTYMT', 'VALUEUSD']].sum()
                summ.rename(columns={'QTYMT': 'Total QTY(MT)',
                            'VALUEUSD': 'Total Value(USD)'}, inplace=True)

                maximum = New_Ethanol_dff.groupby(
                    ['EXPORTER'])[['QTYMT', 'VALUEUSD']].max()
                maximum.rename(columns={'QTYMT': 'Maximum QTY(MT)',
                                        'VALUEUSD': 'Maximum VALUE(USD)'}, inplace=True)

                minimum = New_Ethanol_dff.groupby(
                    ['EXPORTER'])[['QTYMT', 'VALUEUSD']].min()
                minimum.rename(columns={'QTYMT': 'Minimum QTY(MT)',
                                        'VALUEUSD': 'Minimum VALUE(USD)'}, inplace=True)

                intermediate_join = pd.merge(
                    summ, maximum, how='inner', on=["EXPORTER"])

                df_exporter_m = pd.merge(
                    intermediate_join, minimum, how='inner', on=["EXPORTER"])
                df_exporter_m = df_exporter_m.sort_values(
                    by='Total QTY(MT)', ascending=False)
                df_exporter_m = df_exporter_m.fillna(0).astype(float).round(2)
            except:
                pass
            dict = {'df_exporter_m': df_exporter_m.to_html(
                classes="table table-bordered"), 'selected_year': selected_year, 'selected_month': selected_month, 'year_dropdown': year_dropdown, 'month_dropdown': month_dropdown}
            return render(request, 'pandasdemo/analysis10.html', dict)
        else:
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()
            month_dropdown = Ethanol_df['Month'].unique()
            dict = {'selected_year': "Waiting For Selection...",
                    'year_dropdown': year_dropdown, 'month_dropdown': month_dropdown}
            return render(request, 'pandasdemo/analysis10.html', dict)
    else:
        return HttpResponseRedirect('/')


def analysis11(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            selected_year = int(request.POST["analysis11y"])
            selected_month = request.POST['analysis11m']
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()
            month_dropdown = Ethanol_df['Month'].unique()

            New_Ethanol_df = Ethanol_df[Ethanol_df["Year"] == selected_year]
            New_Ethanol_dff = New_Ethanol_df[New_Ethanol_df["Month"]
                                             == selected_month]

            try:
                summ = New_Ethanol_dff.groupby(['IMPORTER'])[
                    ['QTYMT', 'VALUEUSD']].sum()
                summ.rename(columns={'QTYMT': 'Total QTY(MT)',
                            'VALUEUSD': 'Total Value(USD)'}, inplace=True)

                maximum = New_Ethanol_dff.groupby(
                    ['IMPORTER'])[['QTYMT', 'VALUEUSD']].max()
                maximum.rename(columns={'QTYMT': 'Maximum QTY(MT)',
                                        'VALUEUSD': 'Maximum VALUE(USD)'}, inplace=True)

                minimum = New_Ethanol_dff.groupby(
                    ['IMPORTER'])[['QTYMT', 'VALUEUSD']].min()
                minimum.rename(columns={'QTYMT': 'Minimum QTY(MT)',
                                        'VALUEUSD': 'Minimum VALUE(USD)'}, inplace=True)

                intermediate_join = pd.merge(
                    summ, maximum, how='inner', on=["IMPORTER"])

                df_importer_m = pd.merge(
                    intermediate_join, minimum, how='inner', on=["IMPORTER"])

                df_importer_m = df_importer_m.sort_values(
                    by='Total QTY(MT)', ascending=False)
                df_importer_m = df_importer_m.fillna(0).astype(float).round(2)
            except:
                pass

            dict = {'df_importer_m': df_importer_m.to_html(
                classes="table table-bordered"), 'selected_year': selected_year, 'selected_month': selected_month, 'year_dropdown': year_dropdown, 'month_dropdown': month_dropdown}
            return render(request, 'pandasdemo/analysis11.html', dict)
        else:
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            year_dropdown = Ethanol_df['Year'].unique()
            month_dropdown = Ethanol_df['Month'].unique()
            dict = {'selected_year': "Waiting For Selection...",
                    'year_dropdown': year_dropdown, 'month_dropdown': month_dropdown}
            return render(request, 'pandasdemo/analysis11.html', dict)
    else:
        return HttpResponseRedirect('/')


def analysis12(request):
    if request.user.is_authenticated:
        item = Ethanol.objects.all().values()
        df = pd.DataFrame(item)

        df['Month'] = pd.Categorical(df['Month'], categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                                              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                                     ordered=True)
        try:
            summ = df.groupby(['Year', 'Month'])[['QTYMT', 'VALUEUSD']].sum()
            summ.rename(columns={'QTYMT': 'Total QTY(MT)',
                        'VALUEUSD': 'Total Value(USD)'}, inplace=True)

            maximum = df.groupby(['Year', 'Month'])[
                ['QTYMT', 'VALUEUSD']].max()
            maximum.rename(columns={'QTYMT': 'Maximum QTY(MT)',
                           'VALUEUSD': 'Maximum VALUE(USD)'}, inplace=True)

            minimum = df.groupby(['Year', 'Month'])[
                ['QTYMT', 'VALUEUSD']].min()
            minimum.rename(columns={'QTYMT': 'Minimum QTY(MT)',
                                    'VALUEUSD': 'Minimum VALUE(USD)'}, inplace=True)

            intermediate_join = pd.merge(
                summ, maximum, how='inner', on=["Year", "Month"])

            df = pd.merge(intermediate_join, minimum,
                          how='inner', on=["Year", "Month"])

            df = df.sort_values(by=['Year', 'Month'], ascending=False)
            df = df.fillna(0).astype(float).round(2)
        except:
            pass

        dict = {'df': df.to_html(classes="table table-bordered")}
        return render(request, 'pandasdemo/analysis12.html', dict)
    else:
        return HttpResponseRedirect('/')


def analysis13(request):
    if request.user.is_authenticated:
        item = Ethanol.objects.all().values()
        df = pd.DataFrame(item)

        df['Month'] = pd.Categorical(df['Month'], categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                                              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                                     ordered=True)
        try:
            summ = df.groupby(['Year', 'Month', 'REGION'])[
                ['QTYMT', 'VALUEUSD']].sum()
            summ.rename(columns={'QTYMT': 'Total QTY(MT)',
                        'VALUEUSD': 'Total Value(USD)'}, inplace=True)

            maximum = df.groupby(['Year', 'Month', 'REGION'])[
                ['QTYMT', 'VALUEUSD']].max()
            maximum.rename(columns={'QTYMT': 'Maximum QTY(MT)',
                                    'VALUEUSD': 'Maximum VALUE(USD)'}, inplace=True)

            minimum = df.groupby(['Year', 'Month', 'REGION'])[
                ['QTYMT', 'VALUEUSD']].min()
            minimum.rename(columns={'QTYMT': 'Minimum QTY(MT)',
                                    'VALUEUSD': 'Minimum VALUE(USD)'}, inplace=True)

            intermediate_join = pd.merge(summ, maximum, how='inner', on=[
                "Year", "Month", "REGION"])

            df = pd.merge(intermediate_join, minimum, how='inner',
                          on=["Year", "Month", "REGION"])

            df = df.sort_values(
                by=['Year', 'Month', 'Total QTY(MT)'], ascending=False)

            df = df.fillna(0).astype(float).round(2)
        except:
            pass

        dict = {'df': df.to_html(classes="table table-bordered")}
        return render(request, 'pandasdemo/analysis13.html', dict)
    else:
        return HttpResponseRedirect('/')


def analysis14(request):
    if request.user.is_authenticated:
        item = Ethanol.objects.all().values()
        df = pd.DataFrame(item)

        df['Month'] = pd.Categorical(df['Month'], categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                                              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                                     ordered=True)

        try:
            summ = df.groupby(['Year', 'Month', 'Product'])[
                ['QTYMT', 'VALUEUSD']].sum()
            summ.rename(columns={'QTYMT': 'Total QTY(MT)',
                        'VALUEUSD': 'Total Value(USD)'}, inplace=True)

            maximum = df.groupby(['Year', 'Month', 'Product'])[
                ['QTYMT', 'VALUEUSD']].max()
            maximum.rename(columns={'QTYMT': 'Maximum QTY(MT)',
                                    'VALUEUSD': 'Maximum VALUE(USD)'}, inplace=True)

            minimum = df.groupby(['Year', 'Month', 'Product'])[
                ['QTYMT', 'VALUEUSD']].min()
            minimum.rename(columns={'QTYMT': 'Minimum QTY(MT)',
                                    'VALUEUSD': 'Minimum VALUE(USD)'}, inplace=True)

            intermediate_join = pd.merge(summ, maximum, how='inner', on=[
                "Year", "Month", "Product"])

            df = pd.merge(intermediate_join, minimum, how='inner',
                          on=["Year", "Month", "Product"])

            df = df.sort_values(
                by=['Year', 'Month', 'Total QTY(MT)'], ascending=False)

            df = df.fillna(0).astype(float).round(2)
        except:
            pass

        dict = {'df': df.to_html(classes="table table-bordered")}
        return render(request, 'pandasdemo/analysis14.html', dict)
    else:
        return HttpResponseRedirect('/')


def analysis15(request):
    if request.user.is_authenticated:
        item = Ethanol.objects.all().values()
        df = pd.DataFrame(item)

        try:
            summ = df.groupby(['Year', 'COUNTRY'])[['QTYMT', 'VALUEUSD']].sum()
            summ.rename(columns={'QTYMT': 'Total QTY(MT)',
                        'VALUEUSD': 'Total Value(USD)'}, inplace=True)

            maximum = df.groupby(['Year', 'COUNTRY'])[
                ['QTYMT', 'VALUEUSD']].max()
            maximum.rename(columns={'QTYMT': 'Maximum QTY(MT)',
                                    'VALUEUSD': 'Maximum VALUE(USD)'}, inplace=True)

            minimum = df.groupby(['Year', 'COUNTRY'])[
                ['QTYMT', 'VALUEUSD']].min()
            minimum.rename(columns={'QTYMT': 'Minimum QTY(MT)',
                                    'VALUEUSD': 'Minimum VALUE(USD)'}, inplace=True)

            intermediate_join = pd.merge(
                summ, maximum, how='inner', on=["Year", "COUNTRY"])

            df = pd.merge(intermediate_join, minimum,
                          how='inner', on=["Year", "COUNTRY"])

            df = df.sort_values(
                by=['Year', 'Total QTY(MT)'], ascending=False)

            df = df.fillna(0).astype(float).round(2)
        except:
            pass

        dict = {'df': df.to_html(classes="table table-bordered")}
        return render(request, 'pandasdemo/analysis15.html', dict)
    else:
        return HttpResponseRedirect('/')


def analysis16(request):
    if request.user.is_authenticated:
        item = Ethanol.objects.all().values()
        df = pd.DataFrame(item)

        try:
            summ = df.groupby(['Year', 'EXPORTER'])[
                ['QTYMT', 'VALUEUSD']].sum()
            summ.rename(columns={'QTYMT': 'Total QTY(MT)',
                        'VALUEUSD': 'Total Value(USD)'}, inplace=True)

            maximum = df.groupby(['Year', 'EXPORTER'])[
                ['QTYMT', 'VALUEUSD']].max()
            maximum.rename(columns={'QTYMT': 'Maximum QTY(MT)',
                                    'VALUEUSD': 'Maximum VALUE(USD)'}, inplace=True)

            minimum = df.groupby(['Year', 'EXPORTER'])[
                ['QTYMT', 'VALUEUSD']].min()
            minimum.rename(columns={'QTYMT': 'Minimum QTY(MT)',
                                    'VALUEUSD': 'Minimum VALUE(USD)'}, inplace=True)

            intermediate_join = pd.merge(
                summ, maximum, how='inner', on=["Year", "EXPORTER"])

            df = pd.merge(intermediate_join, minimum,
                          how='inner', on=["Year", "EXPORTER"])

            df = df.sort_values(
                by=['Year', 'Total QTY(MT)'], ascending=False)

            df = df.fillna(0).astype(float).round(2)
        except:
            pass

        dict = {'df': df.to_html(classes="table table-bordered")}
        return render(request, 'pandasdemo/analysis16.html', dict)
    else:
        return HttpResponseRedirect('/')


def analysis17(request):
    if request.user.is_authenticated:
        item = Ethanol.objects.all().values()
        df = pd.DataFrame(item)

        try:
            summ = df.groupby(['Year', 'IMPORTER'])[
                ['QTYMT', 'VALUEUSD']].sum()
            summ.rename(columns={'QTYMT': 'Total QTY(MT)',
                        'VALUEUSD': 'Total Value(USD)'}, inplace=True)

            maximum = df.groupby(['Year', 'IMPORTER'])[
                ['QTYMT', 'VALUEUSD']].max()
            maximum.rename(columns={'QTYMT': 'Maximum QTY(MT)',
                           'VALUEUSD': 'Maximum VALUE(USD)'}, inplace=True)

            minimum = df.groupby(['Year', 'IMPORTER'])[
                ['QTYMT', 'VALUEUSD']].min()
            minimum.rename(columns={'QTYMT': 'Minimum QTY(MT)',
                           'VALUEUSD': 'Minimum VALUE(USD)'}, inplace=True)

            intermediate_join = pd.merge(
                summ, maximum, how='inner', on=["Year", "IMPORTER"])

            df = pd.merge(intermediate_join, minimum,
                          how='inner', on=["Year", "IMPORTER"])

            df = df.sort_values(
                by=['Year', 'Total QTY(MT)'], ascending=False)

            df = df.fillna(0).astype(float).round(2)
        except:
            pass

        dict = {'df': df.to_html(classes="table table-bordered")}
        return render(request, 'pandasdemo/analysis17.html', dict)
    else:
        return HttpResponseRedirect('/')


def analysis18(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            selected_year = int(request.POST["analysis18y"])
            selected_exporter = request.POST['analysis18e']
            display_exporter = selected_exporter  # display what value was selected

            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)

            year_dropdown = Ethanol_df['Year'].unique()
            exporter_dropdown = Ethanol_df['EXPORTER'].drop_duplicates()

            New_Ethanol_df = Ethanol_df[Ethanol_df["Year"] == selected_year]
            New_Ethanol_dff = New_Ethanol_df[New_Ethanol_df["EXPORTER"]
                                             == selected_exporter]
            try:
                summ = New_Ethanol_dff.groupby(['IMPORTER'])[
                    ['QTYMT', 'VALUEUSD']].sum()
                summ.rename(columns={'QTYMT': 'Total QTY(MT)',
                            'VALUEUSD': 'Total Value(USD)'}, inplace=True)

                maximum = New_Ethanol_dff.groupby(
                    ['IMPORTER'])[['QTYMT', 'VALUEUSD']].max()
                maximum.rename(columns={
                               'QTYMT': 'Maximum QTY(MT)', 'VALUEUSD': 'Maximum VALUE(USD)'}, inplace=True)

                minimum = New_Ethanol_dff.groupby(
                    ['IMPORTER'])[['QTYMT', 'VALUEUSD']].min()
                minimum.rename(columns={
                               'QTYMT': 'Minimum QTY(MT)', 'VALUEUSD': 'Minimum VALUE(USD)'}, inplace=True)

                intermediate_join = pd.merge(
                    summ, maximum, how='inner', on=["IMPORTER"])

                df_exporter_importer = pd.merge(
                    intermediate_join, minimum, how='inner', on=["IMPORTER"])

                df_exporter_importer = df_exporter_importer.sort_values(
                    by=['Total QTY(MT)'], ascending=False)

                df_exporter_importer = df_exporter_importer.fillna(
                    0).astype(float).round(2)

            except:
                pass

            dict = {'df_exporter_importer': df_exporter_importer.to_html(
                classes="table table-bordered"), 'selected_year': selected_year, 'selected_exporter': selected_exporter, 'exporter_dropdown': exporter_dropdown, 'display_exporter': display_exporter, 'year_dropdown': year_dropdown}
            return render(request, 'pandasdemo/analysis18.html', dict)
        else:
            item = Ethanol.objects.all().values()
            Ethanol_df = pd.DataFrame(item)
            exporter_dropdown = Ethanol_df['EXPORTER'].drop_duplicates()
            year_dropdown = Ethanol_df['Year'].unique()

            dict = {'exporter_dropdown': exporter_dropdown, 'year_dropdown': year_dropdown,
                    'display_exporter': "Wating for selection..."}
            return render(request, 'pandasdemo/analysis18.html', dict)
    else:
        return HttpResponseRedirect('/')


def analysis19(request):
    if request.user.is_authenticated:
        return render(request, 'pandasdemo/ethanoltableaudashboard.html')
    else:
        return HttpResponseRedirect('/')


def ethanolmenu(request):
    if request.user.is_authenticated:
        return render(request, 'pandasdemo/ethanolmenu.html')
    else:
        return HttpResponseRedirect('/')
    
    
class EthanolView(LoginRequiredMixin,UpdateView):
    model = Ethanol
    form_class = EthanolForm
    template_name= "pandasdemo/update_ethanol.html"
    success_url = ('/ethanollist')
    
    
    
def ethanolList(request):
    if request.user.is_authenticated:
                  
        list_items = Ethanol.objects.filter(Year__gte='2000').values(
                'Year').order_by('Year').distinct()
       
        dict = {'list_items': list_items}
        return render(request,'pandasdemo/ethanol_list.html',context = dict)
    else:
        return HttpResponseRedirect('/')
    
    

def ethanolList_yearwise(request,year):
    if request.user.is_authenticated:
        list_items = Ethanol.objects.filter(Year = year)
        
        unique_year = list_items.values('Year').order_by('Year').distinct()
        
        dict = {'list_items': list_items, 'unique_year': unique_year}
        return render(request, 'pandasdemo/ethanol_list_yearwise.html', context=dict)
    else:
        return HttpResponseRedirect('/')
             