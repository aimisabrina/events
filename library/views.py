from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from library.models import Program,Student,Staff,Event,Attendance
from django.contrib.auth import authenticate


# Create your views here.
def index(request):
    return render (request, "index.html")

def signup(request):
    if request.method == 'POST':
        vid = request.POST.get('id')
        vname = request.POST.get('name')
        vphone = request.POST.get('phone')
        vpass1 = request.POST.get('password1')
        vpass2 = request.POST.get('password2')
        vrole = request.POST.get('role')

        #validate inputs
        if vpass1 != vpass2:
            messages.error(request,"Password does not match")
            return redirect('signup')

        if vrole == 'student':
            vgender = request.POST.get('gender')
            vprogram = request.POST.get('program')
            a = Program.objects.get(code=vprogram)
            data=Student(studid=vid, studname=vname, studpassword=vpass2, studgender=vgender, studphone=vphone, code=a)
            data.save()
        elif vrole == 'staff':
            vposition = request.POST.get('position')
            data=Staff(fid=vid, fname=vname, fpass=vpass2, fposition=vposition, fphno=vphone)
            data.save()

        messages.success(request, "Signup successful!")
        return redirect('login')
    return render (request,"signup.html")

def login(request):
    if request.method == 'POST':
        uid = request.POST['id']
        upassw = request.POST['password']
        role = request.POST['role']

        if role == 'student':
            student = Student.objects.filter(studid=uid, studpassword=upassw).first()
            if student:
                request.session['student_id'] = student.studid  # Store in session
                return redirect('main')
            else:
                messages.error(request, "Invalid credentials")
        elif role == 'staff':
            staff = Staff.objects.filter(fid=uid, fpass=upassw).first()
            if staff:
                request.session['staff_id'] = staff.fid
                return redirect('staffmain')
            else:
                messages.error(request, "Invalid credentials")

    return render(request, "login.html")

def main(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    # Get the events joined by the student
    joined_events = Event.objects.filter(attendance__studentid=student_id)

    context = {'join_event': joined_events}
    return render(request, "main.html", context)


def staffmain(request):
    e = Event.objects.select_related('fid').all()
    dict = {'events': e}
    return render (request,"staffmain.html", dict)

def manageevent(request):
    if request.method == 'POST':
        vid = request.POST.get('id')
        vname = request.POST.get('name')
        vdate = request.POST.get('date')
        vvenue = request.POST.get('venue')
        vsid = request.POST.get('sid')

        try:
            staff_member = Staff.objects.get(fid=vsid)
        except Staff.DoesNotExist:
            messages.error(request, "Invalid Staff ID")
            return redirect('manageevent')

        # Save Event Data
        data = Event(eventid=vid, eventname=vname, eventdate=vdate,
                     fid=staff_member, eventvenue=vvenue)
        data.save()

        messages.success(request, "Event created successfully!")
        return redirect('staffmain')

    return render (request,"manageevent.html")

def supdate(request,eventid):
    events=Event.objects.get(eventid=eventid)
    dict = {
        'data':events
    }
    return render(request,"supdate.html",dict)

def save_supdate(request, eventid):
    vname = request.POST.get('name')
    vdate = request.POST.get('date')
    vvenue = request.POST.get('venue')
    vsid = request.POST.get('sid')

    data = Event.objects.get(eventid=eventid)

    # Retrieve the staff object based on the submitted ID
    ffid = Staff.objects.get(fid=vsid)

    # Update the event object with new data
    data.eventname = vname
    data.eventdate = vdate
    data.eventvenue = vvenue
    data.fid = ffid
    data.save()

    messages.success(request, "Event updated successfully!")

    return HttpResponseRedirect(reverse('staffmain'))

def sdelete(request,eventid):
    data = Event.objects.get(eventid=eventid)
    data.delete()
    return HttpResponseRedirect(reverse('staffmain'))

def join_event(request, eventid):
    student_id = request.session.get('student_id') 
    event = get_object_or_404(Event, eventid=eventid)

    # Check if the student has already joined the event
    is_joined = Attendance.objects.filter(studentid=student_id, eventid=event.eventid).exists()

    if not is_joined:
        # Create a new Attendance entry if not already joined
        Attendance.objects.create(studentid_id=student_id, eventid=event)

    return redirect('main') 

def event(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    # Get the events the student has already joined
    joined_event_ids = Attendance.objects.filter(studentid_id=student_id).values_list('eventid', flat=True)
    
    # Exclude already joined events
    available_events = Event.objects.exclude(eventid__in=joined_event_ids).values()

    context = {
        'events': available_events,
    }
    return render(request, "event.html", context)


def search_results(request):
    query = request.GET.get('query', '')
    results = Event.objects.filter(eventid__icontains=query)  # Adjust field name based on your model
    return render(request, 'search.html', {'results': results})

def logout(request):
    return redirect('login') 