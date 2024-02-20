from django.utils import timezone
from datetime import *
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Visitor, ExcelFile, Purpose
from .forms import VisitorForm, PurposeForm
import pandas as pd
from django.conf import settings

from io import BytesIO

# Create your views here.
def base(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def visitor_create_view(request):
    purpose = Purpose.objects.all()
    context = {
        'purpose': purpose,
    }

    if request.method == 'POST':
        form = VisitorForm(request.POST)
        context['form'] = form

        if form.is_valid():
            form.save()
            return redirect('visitor')
    else:
        form = VisitorForm()
        context['form'] = form


    return render(request, 'visitoradd.html', context)



def dashboard(request):
    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render())



def visitor(request):
    visitors = Visitor.objects.all()
    template = loader.get_template('visitor.html')
    context = {
        'visitors' : visitors,
    }
    return HttpResponse(template.render(context, request))

def checkout(request, pk):
    visitor = Visitor.objects.get(id=pk)
    current_time = datetime.now(timezone.utc)
    visitor.check_out = current_time
    visitor.save()
    return redirect('visitor')



def import_data_to_db(request):
    if request.method == 'POST':
        file = request.FILES['files']
        visitor_data = ExcelFile.objects.create(
            file = file
        )
        path = str(visitor_data.file)
        print(f'{settings.BASE_DIR} + {path}')
        excel_read = pd.read_excel(path)
        for data in excel_read.values:
            Visitor.objects.create(
                first_name=data[0],
                last_name=data[1],
                email=data[2],
                phone=data[3],
                address=data[4],
                company=data[5],
                purpose=Purpose.objects.get(name=data[6]),
                check_in=data[7],
                check_out=data[8],
                host=data[9]
            )     
    return render(request, 'import.html')



def export_data_to_excel(request):
    # Retrieve data from the database
    visitors = Visitor.objects.all()
    # Create a pandas DataFrame with the data

    data = {
        'First Name': [visitor.first_name for visitor in visitors],
        'Last Name': [visitor.last_name for visitor in visitors],
        'Email': [visitor.email for visitor in visitors],
        'Phone': [visitor.phone for visitor in visitors],
        'Address': [visitor.address for visitor in visitors],
        'Company': [visitor.company for visitor in visitors],
        'Purpose': [visitor.purpose for visitor in visitors],
        'Check-In': [visitor.check_in.replace(tzinfo=None) for visitor in visitors],
        'Check-Out': [visitor.check_out.replace(tzinfo=None) for visitor in visitors],
        'Host': [visitor.host for visitor in visitors],
    }
    df = pd.DataFrame(data)
    # Create an Excel file in memory
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Visitors', index=False)
    writer.close()
    output.seek(0)
    # Set response headers
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=visitors.xlsx'
    # Write the Excel file to the response
    response.write(output.getvalue())

    return response
    




def qr(request):
    temp = loader.get_template('qr.html')
    return HttpResponse(temp.render())


def details(request,id):
    visitor = Visitor.objects.get(id=id)
    temp = loader.get_template('details.html')
    context = {
        'visitor':visitor,
    }

    return HttpResponse(temp.render(context,request))

def update(request, id):
    visitor = Visitor.objects.get(id=id)

    context={
        'visitor':visitor
    }
    
    if request.method =='POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        company = request.POST.get('company')
        purpose = request.POST.get('purpose')
        host = request.POST.get('host')

        visitor.first_name = first_name
        visitor.last_name = last_name
        visitor.email = email
        visitor.phone = phone
        visitor.address = address
        visitor.company = company
        visitor.purpose = purpose
        visitor.host = host
        visitor.save()

        return redirect('/visitor')
    
    return render(request, 'update.html', context)




def delete(request,id):
    visitor = Visitor.objects.get(id=id)
    visitor.delete()
    return redirect('/visitor')




def purpose(request):
    form = PurposeForm()
    purpose = Purpose.objects.all()
    context = {
        'purpose': purpose,
        'form':form
    }

    if request.method == "POST":
        form = PurposeForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'purpose/purpose.html', context)

    return render(request, 'purpose/purpose.html', context)

def edit_purpose(request, id):
    purpose = Purpose.objects.get(id=id)

    context = {
        'purpose' : purpose
    }

    if request.method == "POST":
        name= request.POST.get("name")
        description = request.POST.get('description')

        purpose.name = name
        purpose.description = description

        purpose.save()
        return redirect('/purpose')

    return render(request, 'purpose/edit_purpose.html', context)


def delete_purpose(request,id):
    purpose = Purpose.objects.get(id=id)
    purpose.delete()
    return redirect('/purpose')




