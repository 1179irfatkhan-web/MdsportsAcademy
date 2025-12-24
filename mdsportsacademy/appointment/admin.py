from django.contrib import admin
from django.contrib import admin
from django.http import HttpResponse
from django.template import response
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table,TableStyle
from .models import *

def export_to_pdf(modeladmin, request, queryset):
    response =HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment';
    filename="report.pdf"
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 14),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])
# Create the table headers
    headers = ['user', 'appointment', 'full_name']
# Create the table data
    data = []
    for obj in queryset:
        data.append([obj.user, obj.appointment,obj.full_name])
        t = Table([headers] + data, style=style)
        elements.append(t)
        doc.build(elements)
        return response
export_to_pdf.short_description = "Export to PDF"

class appointment(admin.ModelAdmin):
    list_display = ["user","full_name","image","location","start_time","end_time","qualification_name","institute_name",
                    "academy_name","department","created_at","fees"]
    actions = [export_to_pdf]
admin.site.register(Appointment,appointment)

class TakeAppointmen(admin.ModelAdmin):
    list_display = ["user","appointment","full_name","message","phone_number","date"]
    actions = [export_to_pdf]
admin.site.register(TakeAppointment,TakeAppointmen)






# admin.site.register(Appointment)
# actions = [export_to_pdf]
# admin.site.register(TakeAppointment)
# Register your models here.