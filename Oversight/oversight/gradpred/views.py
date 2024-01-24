from django.shortcuts import render
import joblib
import csv
# Create your views here.


def predict(request):
    output = 99
    model = joblib.load('gradpredmodel.sav')
    gre = float(request.POST.get("gre",-1))
    toefl = float(request.POST.get("toefl",-1))
    uni = float(request.POST.get("uni",-1))
    sop = float(request.POST.get("sop",-1))
    lor = float(request.POST.get("lor",-1))
    cgpa = float(request.POST.get("cgpa",-1))
    research = request.POST.get("research",-1)
    
    if lor == 1:
        lor = 2
    elif lor == 2:
        lor = 3
    elif lor == 3 :
        lor = 4
    elif lor>3:
        lor = 5
    
    if research == "yes":

        research = 1
    else:
        research = 0
    
    if(gre == -1 or toefl == -1 or uni == -1 or sop == -1 or lor == -1 or cgpa == -1 or research == -1):
        return render(request, 'form.html',{'output' : output})
    else:
        lst=[]
        with open('gradpred/collegelist.csv', 'r') as record:
            csvreader_object=csv.DictReader(record)
            for row in csvreader_object:
                if float(row["Gre"])<gre and float(row["Toefl"])<toefl and float(row["Cgpa"])<cgpa:
                    lst.append(row["Universities"])   
        count = len(lst)  
        output = round(model.predict([[gre,toefl,uni,sop,lor,cgpa,research]])[0]) 
    
    return render(request, 'form.html',{'output' : output , 'lst' : lst,'count':count})