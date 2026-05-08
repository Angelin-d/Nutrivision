from datetime import datetime

from django.contrib.auth import authenticate, login
# from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect


# Create your views here.
# from django.utils.regex_helper import Group

from myapp.models import *


def main(request):
    return render(request,'main.html')

def logout(request):
    return render(request,'loginpage.html')

def login_get(request):
    return render(request,'loginpage.html')


def login_post(request):
    username = request.POST['username']
    password = request.POST['password']
    print(request.POST)

    obj = authenticate(request, username=username, password=password)

    if obj is not None:
        if obj.groups.filter(name='admin').exists():
            login(request, obj)
            return redirect('/myapp/adminhome')
        elif obj.groups.filter(name='user').exists():
            login(request, obj)
            print(request.user.id)
            return redirect('/myapp/userhome')
        else:
            messages.error(request, "Invalid user group.")
            return redirect('/myapp/login_get')
    else:
        messages.error(request, "Invalid username or password.")
        return redirect('/myapp/login_get')



def adminhome(request):
    return render(request,'adminn/index.html')


@login_required(login_url='/myapp/login_get/')
def add_healthtips(request):
    return render(request,'adminn/add_health.html')

@login_required(login_url='/myapp/login_get/')
def add_healthtips_post(request):
    title=request.POST['title']
    tip=request.POST['tip']
    description=request.POST['description']
    # date=request.POST['date']

    ob=tips_table()
    ob.title=title
    ob.tip=tip
    ob.description=description
    ob.date=datetime.now().today()
    ob.save()
    return redirect('/myapp/view_healthtip/')

@login_required(login_url='/myapp/login_get/')
def view_healthtip(request):
    ab=tips_table.objects.all()
    return render(request,'adminn/view_healthtips.html',{'data':ab})

@login_required(login_url='/myapp/login_get/')
def view_history(request):
    ab=PredictionHistory.objects.filter(USER__LOGIN__id=request.user.id).order_by("-id")
    return render(request,'user/view_history.html',{'data':ab})

# def edit_healthtips(request):
#     return render(request,'adminn/edit_healthtips.html')

@login_required(login_url='/myapp/login_get/')
def edit_healthtips(request,id):
    a=tips_table.objects.get(id=id)
    request.session['eid']=id
    return render(request,'adminn/edit_healthtips.html',{'data':a})

@login_required(login_url='/myapp/login_get/')
def delete_dataset(request,id):
    a=dataset.objects.get(id=id)
    a.delete()
    return redirect("/myapp/viewdataset/")
@login_required(login_url='/myapp/login_get/')
def edit_healthtips_post(request):
    title=request.POST['title']
    tip=request.POST['tip']
    description=request.POST['description']
    # date=request.POST['date']
    obj=tips_table.objects.get(id=request.session['eid'])
    obj.name=title
    obj.tip=tip
    obj.description=description
    obj.date=datetime.now().today()
    obj.save()
    return redirect('/myapp/view_healthtip/')

@login_required(login_url='/myapp/login_get/')
def viewdataset(request):
    if request.method == "POST":
        qus=request.POST['qus']
        ans=request.POST['ans']
        ob=dataset()
        ob.question=qus
        ob.answer=ans
        ob.save()
        return redirect("/myapp/viewdataset/")
    ob=dataset.objects.all()
    return render(request,"adminn/managedataset.html",{"data":ob})

@login_required(login_url='/myapp/login_get/')
def delete_tips(request,id):
    a=tips_table.objects.get(id=id)
    a.delete()
    return redirect('/myapp/view_healthtip/')

@login_required(login_url='/myapp/login_get/')
def view_feedback(request):
    ab=Feedback_table.objects.all()
    return render(request,'adminn/view_feedback.html',{'data':ab})

def view_user(request):
    ab=User_table.objects.all()
    return render(request,'adminn/view_user.html',{'data':ab})

def viewpersonaldetails(request,id):
    ab=personaldetails.objects.filter(USER__id=id)
    return render(request,'adminn/view_personaldetails.html',{'data':ab})


########################user#######################################



def user_re(request):
    return render(request,'user/registration.html')


def user_reg_post(request):
    name=request.POST['name']
    email=request.POST['email']
    # phone=request.POST['phone']
    age=request.POST['age']
    gender=request.POST['gender']
    try:
        image=request.FILES['image']
        fs=FileSystemStorage()
        path=fs.save(image.name,image)
    except:
        path="person.png"
    # pin=request.POST['pin']
    # place=request.POST['place']
    # district=request.POST['district']

    username=request.POST['username']
    password=request.POST['password']


    log=User.objects.create(username=username,password=make_password(password),first_name=name,email=email)
    log.save()

    log.groups.add(Group.objects.get(name='user'))


    obj=User_table()
    obj.name=name
    obj.email=email

    obj.age=age
    obj.gender=gender
    obj.image=path

    obj.LOGIN=log
    obj.save()

    return redirect('/myapp/user_re/')

@login_required(login_url='/myapp/login_get/')
def edit_details(request,id):
    a = personaldetails.objects.get(id=id)
    request.session['eid'] = id
    return render(request,'user/edit_personaldetails.html',{'data':a})


def edit_details_post(request):
    healthconditions = request.POST['healthconditions']
    dietry_prefer = request.POST['dietry_prefer']
    allergies = request.POST['allergies']
    supplements_taken = request.POST['supplements_taken']
    smoking_habit = request.POST['smoking_habit']
    physical_conditions = request.POST['physical_conditions']
    # medical_history=request.POST['medical_history']
    alcohol_consumption = request.POST['alcohol_consumption']
    height = request.POST['height']
    weight = request.POST['weight']
    image = request.FILES['image']
    fs = FileSystemStorage()
    path = fs.save(image.name, image)

    ob = personaldetails.objects.get(id=request.session['eid'])

    ob.USER = User_table.objects.get(LOGIN_id=request.user.id)
    ob.healthconditions = healthconditions
    ob.dietry_prefer = dietry_prefer
    # ob.bmi=bmi
    ob.allergies = allergies
    ob.supplements_taken = supplements_taken
    ob.smoking_habit = smoking_habit
    ob.physical_conditions = physical_conditions
    # ob.medical_history=medical_history
    ob.alcohol_consumption = alcohol_consumption
    ob.height = height
    ob.weight = weight
    ob.image = path
    ob.save()
    return redirect('/myapp/view_personaldetails/')




@login_required(login_url='/myapp/login_get/')
def add_personaldetails(request):
    return render(request,'user/manage_personaldetails.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User_table, PredictionHistory, tips_table, personaldetails
import random


@login_required(login_url='/myapp/login_get/')
def userhome(request):
    # Get the user object linked to the login
    user_data = User_table.objects.get(LOGIN=request.user)

    # Fetch Prediction History (Recent 3)
    history = PredictionHistory.objects.filter(USER=user_data).order_by('-id')[:2]

    # Calculate Total Scans
    total_scans = PredictionHistory.objects.filter(USER=user_data).count()

    # Fetch Health Tip (Random or Latest)
    tip = tips_table.objects.order_by('-id')
    if len(tip)>4:
        tip=tip[:4]
    # tip1 = tips_table.objects.order_by('-id').first()

    # Fetch Personal Stats (Height, Weight)
    stats = personaldetails.objects.filter(USER=user_data).first()

    # Calculate Health Points (Simple logic: 50 points per scan + 100 for profile completion)
    health_points = (total_scans * 50) + (150 if stats else 0)

    context = {
        'user_data': user_data,
        'history': history,
        'total_scans': total_scans,
        'tip': tip,
        'stats': stats,
        'health_points': health_points,
    }

    return render(request, 'user/userhome.html', context)

@login_required(login_url='/myapp/login_get/')
def add_personaldetails_post(request):
    healthconditions=request.POST['healthconditions']
    dietry_prefer=request.POST['dietary_prefer']
    allergies=request.POST['allergies']
    supplements_taken=request.POST['supplements_taken']
    smoking_habit=request.POST['smoking_habit']
    physical_conditions=request.POST['physical_conditions']
    # medical_history=request.POST['medical_history']
    alcohol_consumption=request.POST['alcohol_consumption']
    height=request.POST['height']
    weight=request.POST['weight']
    try:
        image=request.FILES['image']
        fs = FileSystemStorage()
        path = fs.save(image.name,image)
    except:
        path="nofile.jpg"

    ob=personaldetails()
    ob.USER = User_table.objects.get(LOGIN_id=request.user.id)
    ob.healthconditions=healthconditions
    ob.dietry_prefer=dietry_prefer
    # ob.bmi=bmi
    ob.allergies=allergies
    ob.supplements_taken=supplements_taken
    ob.smoking_habit=smoking_habit
    ob.physical_conditions=physical_conditions
    # ob.medical_history=medical_history
    ob.alcohol_consumption=alcohol_consumption
    ob.height=height
    ob.weight=weight
    ob.image=path
    ob.save()
    return redirect('/myapp/view_personaldetails/')

@login_required(login_url='/myapp/login_get/')
def send_feedback(request):
    return render(request,'user/send_feedback.html')

@login_required(login_url='/myapp/login_get/')
def send_feedback_post(request):
    feedback=request.POST['feedback']
    rating=request.POST['rating']

    ob=Feedback_table()
    ob.USER=User_table.objects.get(LOGIN_id=request.user.id)
    ob.feedback=feedback
    ob.rating=rating
    ob.date=datetime.now().today()
    ob.save()
    return redirect('/myapp/send_feedback/')

@login_required(login_url='/myapp/login_get/')
def view_healthtips(request):
    ab=tips_table.objects.all()
    return render(request,'user/view_healthtips.html',{'data':ab})

@login_required(login_url='/myapp/login_get/')
def view_personaldetails(request):
    ab=personaldetails.objects.all()
    return render(request,'user/view_personaldetails.html',{'data':ab})

# @login_required(login_url='/myapp/login_get/')
# def userhome(request):
#     return render(request,'user/userhome.html')

@login_required(login_url='/myapp/login_get/')
def delete_personaldetails(request,id):
    a=personaldetails.objects.get(id=id)
    a.delete()
    return redirect('/myapp/view_personaldetails/')

def chat_ui(request):
    return render(request, 'user/chat.html')


import json
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Configure Google Gemini API
GOOGLE_API_KEY = 'API_key'
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash')

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        # try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            if not user_message:
                return JsonResponse({'response': 'Please enter a valid question.'})
            res=cb(user_message)
            if res=="na":
                qry="answer me as a nutritionist chatbot based on nutrient deficiency ,the question is "+user_message + "i need 4 or 5 statement answers,make it simple which should be user friendly and include recommendations about food and lifestyle to the user.only if the" +user_message+ "is not medical or nutrition related please respond to the user with a single statement asking to enter a valid question related to the topic "
                ob=personaldetails.objects.filter(USER__LOGIN__id=request.user.id).order_by("-id")
                if len(ob)>0:
                    ob=ob[0]
                    qry+="answer considering the persons health conditions " + ob.healthconditions + "allergies" + ob.allergies + "dietary preference" + ob.dietry_prefer + " supplements taken" + ob.supplements_taken + " habits " + ob.alcohol_consumption + ob.smoking_habit + "physical conditions" + ob.physical_conditions + "please keep the answers short unless they ask to"
                gemini_response = model.generate_content(qry)
                ob=dataset()
                ob.question=user_message
                ob.answer=gemini_response.text.strip().replace("*","")
                ob.save()
                return JsonResponse({'response': gemini_response.text.strip().replace("*","")})
            return JsonResponse({'response': res})

        # except json.JSONDecodeError:
        #     return JsonResponse({'response': 'Invalid JSON format.'}, status=400)
        # except Exception as e:
        #     return JsonResponse({'response': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'response': 'Invalid request method. Use POST.'}, status=405)

import subprocess
from .predict1 import predict_nail_fn
from .predict1eye import predict_eye_fn
def predict_nail(request):
    return render(request,"user/predict_nail.html")
def predict_nail_post(request):
    img=request.FILES['img']
    pc=request.POST['pc']
    fs=FileSystemStorage()
    fn=fs.save(img.name,img)

    subprocess.run([
        r"C:\Users\angel\AppData\Local\Programs\Python\Python36\python.exe",
        r"C:\Users\angel\OneDrive\Desktop\NUTRITION_DEFICIENCY (3)\NUTRITION_DEFICIENCY\object_detection.py",

        r"C:\Users\angel\OneDrive\Desktop\NUTRITION_DEFICIENCY (3)\NUTRITION_DEFICIENCY\media/"+fn
    ])

    with open("example.txt", "r") as file:
        content = file.read()
        if content=="invalid":
            return render(request, "user/nail_res.html", {"s": 0, "res": "Invalid", "sol": "", "img": "/media/" + fn})
    res,confidence=predict_nail_fn(r"C:\NUTRITION_DEFICIENCY (3)\NUTRITION_DEFICIENCY\media/"+fn)
    print(res)
    if confidence > 0.85:
        explanation = "The model detected strong visual patterns associated with this nutritional deficiency."
    elif confidence > 0.60:
        explanation = "Moderate visual indicators influenced the prediction."
    else:
        explanation = "Only subtle nail features contributed to the prediction."

    st=0
    sol=""

    if res=="invalid":
        st = 1
        sol = ""
        explanation="Upload an appropriate image"
    elif res!="healthy":
        st=1
        print("i have " + res + " and pre condition " + pc + " solution(diet planning , food recommendations, lifestyle planning  that are good for the deficiency and pre conditions ) for this ")
        sol = solution("i have " + res  + " and pre condition " + pc + " solution(diet planning , food recommendations, lifestyle planning  that are good for the deficiency and pre conditions ) for this ")

    print(sol)
    ob = PredictionHistory()
    ob.USER = User_table.objects.get(LOGIN__id=request.user.id)
    ob.precondition = pc
    ob.result = res
    ob.suggestion = sol
    ob.confidence = round(confidence*100,2)
    ob.image = fn
    ob.date = datetime.today()
    ob.save()
    return render(request,"user/nail_res.html",{"s":st,"res":res,"sol":sol,"img":"/media/"+fn,"ex":explanation})

def predict_eye(request):
    return render(request,"user/predict_eye.html")
def predict_eye_post(request):
    img = request.FILES['img']
    pc = request.POST['pc']
    fs = FileSystemStorage()
    fn = fs.save(img.name, img)
    subprocess.run([
        r"C:\Users\angel\AppData\Local\Programs\Python\Python36\python.exe",
        r"C:\\NUTRITION_DEFICIENCY (3)\NUTRITION_DEFICIENCY\object_detection.py",

        r"C:\NUTRITION_DEFICIENCY (3)\NUTRITION_DEFICIENCY\media/" + fn
    ])
    with open("example.txt", "r") as file:
        content = file.read()
        if content == "invalid":
            return render(request, "user/eye_res.html", {"s": 0, "res": "Invalid", "sol": "", "img": "/media/" + fn})

    res,confidence = predict_eye_fn(r"C:\NUTRITION_DEFICIENCY (3)\NUTRITION_DEFICIENCY\media/" + fn)
    print(res)
    st = 0
    sol = ""
    if confidence > 0.85:
        explanation = "The model detected strong visual patterns associated with this nutritional deficiency."
    elif confidence > 0.60:
        explanation = "Moderate visual indicators influenced the prediction."
    else:
        explanation = "Only subtle eye features contributed to the prediction."
    if res == "glass" or res == "Closed_Eyes":
        st = 1
        explanation = "Upload an appropriate image"
        sol = ""
    elif res == "invalid":
        st = 1
        explanation = "Upload an appropriate image"
        sol = ""
    elif res != "normal":
        st = 1
        sol = solution("i have " + res + " and pre condition"+pc+" solution for this ")

    else:
        res="healthy"
    ob=PredictionHistory()
    ob.USER=User_table.objects.get(LOGIN__id=request.user.id)
    ob.precondition=pc
    ob.result=res
    ob.suggestion =sol
    ob.confidence =round(confidence*100,2)
    ob.image=fn
    ob.date=datetime.today()
    ob.save()
    print({"s": st, "res": res, "sol": sol, "img": "/media/" + fn,"ex":explanation})
    return render(request, "user/eye_res.html", {"s": st, "res": res, "sol": sol, "img": "/media/" + fn,"ex":explanation})



def solution(txt):

        try:

            user_message = txt.strip()



            gemini_response = model.generate_content(" i need chatbot based on vitamin deficiency if question not based on it please make sure about the question and question is "+user_message+" i only need a para including food recommendation as solution no other details")

            return gemini_response.text.strip()

        except Exception as e:
            print(e)
            return "No Result"
def solution1(txt):

        try:

            user_message = txt.strip()



            gemini_response = model.generate_content(" i need chatbot based on vitamin deficiency if question not based on it please make sure about the question and question is "+user_message+ " i only need a para including food recommendation as solution no other details")

            return gemini_response.text.strip()

        except Exception as e:
            print(e)
            return "No Result"
from werkzeug.utils import secure_filename
import re, math
def cb(qus):
    WORD = re.compile(r'\w+')

    from collections import Counter
    def text_to_vector(text):
        words = WORD.findall(text)
        return Counter(words)

    def get_cosine(vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    vector1 = text_to_vector(qus.lower())
    s=dataset.objects.all()


    res = []
    for d in s:
        vector2 = text_to_vector(str(d.question.lower()))
        cosine = get_cosine(vector1, vector2)
        # print("cosine",cosine)

        res.append([cosine,d.id])

    print("res---" ,res)

    ss = 0
    cnt = -1
    i = 0
    for s in res:
        print(s)
        print(s)
        if s[0] > 0.75:
            if ss <= float(s[0]):
                cnt = s[1]
                ss = float(s[0])
        i = i + 1

    print("ss", ss)
    print("cnt", cnt)

    q=dataset.objects.filter(id=cnt)
    print(q)
    if len(q)==0:
        return "na"
    else:
        print(q[0].answer)
        return q[0].answer

def profile(request):
    return render(request,"profile.html")









