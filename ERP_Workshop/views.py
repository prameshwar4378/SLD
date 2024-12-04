from django.shortcuts import render

def dashboard(request):
    return render(request, "workshop_dashboard.html")

def breakdown_alerts(request):
    return render(request, "workshop_breakdown_alerts.html")

def job_card_management(request):
    return render(request, "workshop_job_card_management.html")

def maintenance_logs(request):
    return render(request, "workshop_maintenance_logs.html")

def maintenance_schedule(request):
    return render(request, "workshop_maintenance_schedule.html")

def reports(request):
    return render(request, "workshop_reports.html")
