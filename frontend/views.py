from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect

import datetime, pytz
from datetime import timedelta
from django.utils import timezone


import xlwt

from api.models import *

from .summaryview.summary1view import summary_1_view
from .summaryview.summary2view import summary_2_view
from .summaryview.summary3view import summary_3_view
from .summaryview.summary4view import summary_4_view, summary_4_view_all
from .summaryview.summary5view import summary_5_view
from .summaryview.summary6view import summary_6_view
from .summaryview.summary7view import summary_7_view
from .summaryview.summary8view import summary_8_view
from .summaryview.home_view import excel_response, home_response


# Create your views here.    
@login_required(login_url='/')
def home(request):
    if request.user.is_superuser:
        return redirect('/admin')
    htmlfile, homedic = home_response(request) 
    return render(request, 'frontend/' + htmlfile, homedic)

@login_required(login_url = '/')
def home_xls(request):
    if request.user.is_superuser:
        return redirect('/admin')
    return excel_response(request)




@login_required(login_url='/')
def summary(request):
    if request.user.is_superuser:
        return redirect('/admin')
    return render(request, 'frontend/summary.html', {"summary_name": "MIS SUMMARY REPORT", "machine": Machine.objects.filter(user=request.user)})





@login_required(login_url='/')
def summary_1(request):
    if request.user.is_superuser:
        return redirect('/admin')
    htmlfile, summary_1_dic = summary_1_view(request)
    return render(request, 'frontend/' + htmlfile, summary_1_dic)


@login_required(login_url='/')
def summary_2(request):
    if request.user.is_superuser:
        return redirect('/admin')
    htmlfile, summary2dic = summary_2_view(request)
    return render(request, 'frontend/' + htmlfile, summary2dic)


@login_required(login_url='/')
def summary_4(request):
    if request.user.is_superuser:
        return redirect('/admin')
    htmlfile, summary_4_dic = summary_4_view(request)
    return render(request, 'frontend/' + htmlfile, summary_4_dic)


@login_required(login_url='/')
def summary_7(request):
    if request.user.is_superuser:
        return redirect('/admin')
    htmlfile, summary7dic = summary_7_view(request)
    return render(request, 'frontend/' + htmlfile, summary7dic)


@login_required(login_url='/')
def summary_8(request):
    if request.user.is_superuser:
        return redirect('/admin')
    htmlfile, summary8dic = summary_8_view(request)
    return render(request, 'frontend/' + htmlfile, summary8dic)







@login_required(login_url='/')
def summary_format(request):
    if request.user.is_superuser:
        return redirect('/admin')
    summarytype = request.GET.get('summarytype')
    if request.method == 'POST':
        # try:
            startdate = request.POST['startdate']
            enddate = request.POST['enddate']
            viewformat = request.POST['viewformat'] 
            if summarytype == 'summary_3':
                htmlfile, summarydic = summary_3_view(request.user, startdate, enddate, viewformat)
            elif summarytype == 'summary_4':
                htmlfile, summarydic = summary_4_view_all(request.user, startdate, enddate, viewformat)
            elif summarytype == 'summary_5':
                htmlfile, summarydic = summary_5_view(request.user, startdate, enddate, viewformat)
            elif summarytype == 'summary_6':
                htmlfile, summarydic = summary_6_view(request.user, startdate, enddate, viewformat)
            else:
                raise Exception("Wrong Summary")
            return render(request, 'frontend/' + htmlfile, summarydic)
        # except Exception as ex:
        #     print(ex)
        #     return render(request, 'frontend/summary_format.html', {"message": str(ex), "summarytype": summarytype})
    return render(request, 'frontend/summary_format.html', {"summarytype": summarytype})












@csrf_protect
@login_required(login_url='/')
def pipeshiftduration_summary_1(request):
    if request.user.is_superuser:
        return redirect('/admin')
    shiftdate = request.POST['shiftdate']
    shift1 = request.POST['shift1']
    shift2 = request.POST['shift2']
    shift3 = request.POST['shift3']
    shift1 = datetime.timedelta(seconds = int(shift1[0 : 2]) * 3600 + int(shift1[3 : 5]) * 60 )
    shift2 = datetime.timedelta(seconds = int(shift2[0 : 2]) * 3600 + int(shift2[3 : 5]) * 60 )
    shift3 = datetime.timedelta(seconds = int(shift3[0 : 2]) * 3600 + int(shift3[3 : 5]) * 60 )
    shift_1_downtime = datetime.timedelta(minutes=480) - shift1
    shift_2_downtime = datetime.timedelta(minutes=480) - shift2
    shift_3_downtime = datetime.timedelta(minutes=480) - shift3
    try:
        PipeShiftDuration.objects.create(user = request.user, shift_date = shiftdate, shift_1 = shift1, shift_1_downtime = shift_1_downtime, shift_2 = shift2, shift_2_downtime = shift_2_downtime, shift_3 = shift3, shift_3_downtime = shift_3_downtime)  
    except:
        pass
    try:
        PipeShiftDuration.objects.filter(user = request.user, shift_date = shiftdate).update(shift_1 = shift1, shift_1_downtime = shift_1_downtime, shift_2 = shift2, shift_2_downtime = shift_2_downtime, shift_3 = shift3, shift_3_downtime = shift_3_downtime)
    except:
        pass
    return HttpResponseRedirect('summary_1?shiftdate=' + shiftdate)



@csrf_protect
@login_required(login_url='/')
def material_issue_summary_4(request):
    if request.user.is_superuser:
        return redirect('/admin')
    shiftdate = request.POST['shiftdate']
    try:
        shift1 = int(request.POST['shift1'])
        shift2 = int(request.POST['shift2'])
        shift3 = int(request.POST['shift3'])
    except:
        shift1 = 0
        shift2 = 0
        shift3 = 0
    try:
        MetarialIssueShift.objects.create(user = request.user, shift_date = shiftdate, shift_1 = shift1, shift_2 = shift2, shift_3 = shift3)  
    except:
        pass
    try:
        MetarialIssueShift.objects.filter(user = request.user, shift_date = shiftdate).update(shift_1 = shift1, shift_2 = shift2, shift_3 = shift3)
    except Exception as ex:
        print(ex)
    return HttpResponseRedirect('summary_4?shiftdate=' + shiftdate)




















@csrf_protect
def index(request):
    from django.contrib.auth import authenticate, login
    wrongUser = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                wrongUser = {"message": "Wrong username or password"}
            else:
                login(request, user)
        else: 
            wrongUser = {"message": "Wrong username or password"}
    if request.user.is_authenticated:
        return redirect('/home')
    return render(request, 'frontend/index.html', wrongUser)


@login_required(login_url='/')
def log_out(request):
    from django.contrib.auth import logout
    if request.user.is_superuser:
        return redirect('/admin')
    logout(request)
    return redirect('/')