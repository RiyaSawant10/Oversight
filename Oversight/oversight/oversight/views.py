from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from .forms import NewUserForm
from .models import user as User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
import openai


# Create your views here.

def chatbot_response(user_input):
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=user_input,
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
    return response["choices"][0]["text"]

def index(request):
    return render(request,'home.html')
    
def forums(request):
    if request.method == 'POST':
        input_text = request.POST['input']
        response = chatbot_response("is "+input_text+"related to science answer in yes or no")
        response2 = chatbot_response("is "+input_text+"a form of greeting answer in yes or no")
        response = response.strip()
        response2 = response2.strip()
        if response == "Yes" or response2 == "Yes" or "college" in input_text or "engineering" in input_text or "engg" in input_text:
            response = chatbot_response(input_text)
        else:
            response = "Please enter engineering related queries"
        return JsonResponse({'response':response})
    else:
        return render(request,'for.html')
    
def pro_ideas(request):
    response = ""
    r=[]
    if request.method == 'POST':
        if request.POST.get("submit"):
            degree = float(request.POST.get("degree",-1))
            type = float(request.POST.get("type",-1))
            domain = request.POST.get("domain",-1)
            
            if degree != -1 and type != -1 and domain != -1:
                if degree == 1:
                    degree = "Bachelors"
                else:
                    degree = "Masters"
                
                if type == 1:
                    type = "Mini"
                else:
                    type = "Major"
                
                if chatbot_response("Is"+ domain +"related to science or engineering? answer in yes or no").strip() == "No":
                    response="Enter a valid domain"
                    r = ["Enter a valid domain"]
                else:
                    response = chatbot_response("List projects in bullet points that can be made for a "+type+" project "+"in the domain of "+domain+" for a "+degree+" degree student with their online examples")
                    r=response.split("•")
                    if "\n\n" in r:
                        r.remove("\n\n")
            else:
                response = ""
        if request.POST.get("save"):
            current_user = request.user.email
            print(current_user)
            response2 = request.POST.get("savecontent","")
            u = User.objects.get(email = current_user)
            u.ideas += ",>"+response2
            u.save()
    return render(request,'project_ideas.html',{'response' : response,'r':r})

def notes(request):
    response = ""
    r=[]
    type = -1
    if request.method == 'POST':
        if request.POST.get("submit"):
            type = float(request.POST.get("type",-1))
            chp = request.POST.get("chp","")
            sub = request.POST.get("sub","")
            sem = request.POST.get("sem","")
            branch = request.POST.get("branch","")
            if type != -1 and chp!="" and sub!="" and sem!="" and branch!="":
                if int(sem)>8:
                    response = "Enter Valid Semester"
                else:  
                    if type==1:
                        response = chatbot_response("notes on "+chp+","+sub+" for sem"+sem+branch+"engineering")        
                    elif type==2:
                        response = chatbot_response("generate 10 practice questions on "+chp+","+sub+" for sem"+sem+branch+"engineering")
                        r=response.split("\n")
                        if "" in r:
                            r.remove("")
                
            else:
                response = ""
                
        if request.POST.get("save"):
            if float(request.POST.get("savecontenttype",-1)) == 1:
                current_user = request.user.email
                response2 = request.POST.get("savecontent","")
                u = User.objects.get(email = current_user)
                u.notes += ",>"+response2
                u.save()
        
            if float(request.POST.get("savecontenttype",-1)) == 2:
                current_user = request.user.email
                response2 = request.POST.get("savecontent","")
                u = User.objects.get(email = current_user)
                u.questions += ",>"+response2
                u.save()
            
    
    return render(request,'notes1.html',{'response' : response,'type':type,'r':r})

def saved(request):
    current_user = request.user.email
    u = User.objects.get(email = current_user)
    
    if request.POST.get("proj"):
        ideas = u.ideas.split(',>')
        if ' ' in ideas:
            ideas.remove(' ')
        return render(request,'display.html',{'ideas':ideas ,'t':1})
    
    if request.POST.get("deleteideas"):
        ideas = u.ideas.split(',>')
        u.ideas = " "
        u.save()
        return render(request,'display.html',{'ideas':ideas ,'t':1})
        
    if request.POST.get("que"):        
        questions = u.questions.split(',>')
        if ' ' in questions:
            questions.remove(' ')
        return render(request,'display.html',{'questions':questions ,'t':2})
        
    if request.POST.get("deleteque"):
        questions = u.questions.split(',>')
        u.questions = " "
        u.save()
        return render(request,'display.html',{'questions':questions ,'t':2})
    
    if request.POST.get("notes"):  
        notes = u.notes.split(',>')
        if ' ' in notes:
            notes.remove(' ')
        return render(request,'display.html',{'notes':notes ,'t':3})
        
    if request.POST.get("deletenotes"):
        notes = u.notes.split(',>')
        u.notes = " "
        u.save()
        return render(request,'display.html',{'notes':notes ,'t':3})
        
    return render(request,'saved.html')

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            current_user = request.user.email
            User.objects.get_or_create(email=current_user,ideas="")
            return redirect("login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="index.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("login")

def contact(request):
    return HttpResponse("This Is contact page")
