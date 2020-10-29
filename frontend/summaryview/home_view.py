from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect

import datetime, pytz
from datetime import timedelta
from django.utils import timezone

from django.db.models import Sum, Avg, Count
from django.db.models.functions import TruncDay 

import xlwt

from api.models import *


def home_response(request):
    startdate = request.GET.get('startdate', None)
    enddate = request.GET.get('enddate', None)
    starttime = request.GET.get('starttime', None)
    endtime = request.GET.get('endtime', None)
    machine = Machine.objects.filter(user=request.user)
    machine_list = [] 
    for i in machine:
        machine_list.append(i.toDic()["machine_id"]) 
    if(startdate == None and enddate == None and starttime == None and endtime == None):
        timezone_localtime = timezone.localtime(timezone.now())
        enddate = startdate = timezone_localtime.strftime('%Y-%m-%d')  
        starttime = (timezone_localtime - timedelta(hours=2)).strftime('%H:%M')
        endtime = timezone_localtime.strftime('%H:%M')
    try:
        starttimestamp = timezone.make_aware(datetime.datetime.strptime(str(startdate) + ' ' + starttime + ':00', "%Y-%m-%d %H:%M:%S"))
        endtimestamp = timezone.make_aware(datetime.datetime.strptime(str(enddate) + ' ' + endtime + ':59', "%Y-%m-%d %H:%M:%S"))
        pipdataprocess = PipeDataProcessed.objects.filter(site_time__range=(starttimestamp, endtimestamp), machine_id__in = machine_list) 
    except Exception as excep:
        timezone_localtime = timezone.localtime(timezone.now())
        enddate = startdate = timezone_localtime.strftime('%Y-%m-%d')  
        starttime = (timezone_localtime - timedelta(hours=2)).strftime('%H:%M')
        endtime = timezone_localtime.strftime('%H:%M')
        starttimestamp = timezone.make_aware(datetime.datetime.strptime(str(startdate) + ' ' + starttime + ':00', "%Y-%m-%d %H:%M:%S"))
        endtimestamp = timezone.make_aware(datetime.datetime.strptime(str(enddate) + ' ' + endtime + ':59', "%Y-%m-%d %H:%M:%S"))
        pipdataprocess = PipeDataProcessed.objects.filter(site_time__range=(starttimestamp, endtimestamp), machine_id__in = machine_list) 
    machinestatus = MachineStatus.objects.filter(machine_id__in = machine)
    from itertools import zip_longest
    return 'home.html', {
        "machinewithstatus": zip_longest(machine, machinestatus), 
        "pipedata": pipdataprocess, 
        "startdate": startdate, "enddate": enddate, 
        "starttime": starttime, "endtime": endtime,
        "issue": str(MetarialIssueShift.objects.filter(shift_date = enddate, user=request.user).count()),
        "duration": str(PipeShiftDuration.objects.filter(shift_date = enddate, user=request.user).count())
    }
    


def excel_response(request):
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')
    starttime = request.GET.get('starttime')
    endtime = request.GET.get('endtime')
    if(startdate == None and enddate == None and starttime and endtime == None):
        return HttpResponse(status = 400)
    machine_list = [] 
    for i in Machine.objects.filter(user=request.user):
        machine_list.append(i.toDic()["machine_id"])
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="raw_data_' + startdate + '_' + starttime + '_to_' + enddate + '_' + endtime + '.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Raw_Pipe_Data')
    # Sheet header, first row
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Pipe Type', 'Outer Diameter', 'Length','Count', 'Weight (Gram)', 'Max Weight (Gram)', 'Min Weight (Gram)', 'Weight Gain (Gram)', 'Status', 'Weighing Time']
    row_num = 0
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    starttimestamp = timezone.make_aware(datetime.datetime.strptime(str(startdate) + ' ' + starttime + ':00', "%Y-%m-%d %H:%M:%S"))
    endtimestamp = timezone.make_aware(datetime.datetime.strptime(str(enddate) + ' ' + endtime + ':59', "%Y-%m-%d %H:%M:%S"))
    pipdataprocess = PipeDataProcessed.objects.filter(site_time__range=(starttimestamp, endtimestamp), machine_id__in = machine_list) 
    for row in pipdataprocess:
        row_num += 1
        rowtoDic = row.toDic()
        ws.write(row_num, 0, str(rowtoDic["basic_metarial"]) + ' ' + str(rowtoDic["standard_type_classification"]) + ' ' + str(rowtoDic["pressure_type_specification"]), font_style)
        ws.write(row_num, 1, str(rowtoDic["outer_diameter"]) + ' ' + str(rowtoDic["outer_diameter_unit"]), font_style)
        ws.write(row_num, 2, str(rowtoDic["length"]) + ' ' + str(rowtoDic["length_unit"]), font_style)
        ws.write(row_num, 3, str(rowtoDic["count"]), font_style)
        ws.write(row_num, 4, str(rowtoDic["weight"]), font_style)
        ws.write(row_num, 5, str(rowtoDic["maxweight"]), font_style)
        ws.write(row_num, 6, str(rowtoDic["minweight"]), font_style)
        if rowtoDic["weightgain"] == 0:
            ws.write(row_num, 7, str(rowtoDic["weightloss"]), font_style)
        else:
            ws.write(row_num, 7, str(rowtoDic["weightgain"]), font_style)
        ws.write(row_num, 8, str(rowtoDic["pass_status"]), font_style)
        ws.write(row_num, 9, timezone.localtime(rowtoDic["site_time"]).strftime("%A, %B %d, %Y %I:%M %p"), font_style)
    wb.save(response)
    return response
