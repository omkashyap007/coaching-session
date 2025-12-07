from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, UTC, time
from account.models import Student, Expert
from coaching.models import CoachingSession, CoachingSessionStateChoices
from account.choices import UserTypeChoices
from django.db.models import Q

def homePage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to access home page")
        return redirect("login")
    
    user = request.user
    now = datetime.now()
    start = datetime.combine(now.date(), time.min)
    end = datetime.combine(now.date(), time.max)

    experts_list = []
    sessions_list = []
    if user.user_type == UserTypeChoices.student:
        sessions = CoachingSession.objects.filter(
            student=request.user,
            start_time__gte=start,
        )
    else:
        sessions = CoachingSession.objects.filter(
            expert=request.user,
            start_time__gte=start,
        )
    for session in sessions:
        sessions_list.append(
            {
                "id": session.id,
                "start_time": session.start_time,
                "end_time": session.end_time,
                "state": session.state
            }
        )
    if user.user_type == UserTypeChoices.student:
        experts = Expert.objects.all()
        experts_list = []
        for expert in experts:
            experts_list.append(
                {
                    "id": expert.id,
                    "email": expert.email
                }
            )
    context = {
        "experts": experts_list,
        "sessions": sessions_list,
    }
    return render(request, "coaching/homePage.html", context=context)


def createSessions(request, expert_id):
    if request.method == "POST":
        session_start_time = request.POST.get("start_time")
        session_end_time = request.POST.get("end_time")

        try:
            session_start_time = datetime.fromisoformat(session_start_time)
            session_end_time = datetime.fromisoformat(session_end_time)
        except Exception:
            messages.error(request, "Invalid date format")
            return redirect("create-session", expert_id=expert_id)

        overlap_filter = (
            (
                Q(expert_id=expert_id) | Q(student=request.user)
            ) & 
            (
                Q(start_time__lt=session_end_time) & Q(end_time__gt=session_start_time)
            )
        )
        print(f"Filter : {overlap_filter}")
        existing_sessions = CoachingSession.objects.filter(expert_id=expert_id).filter(overlap_filter)

        if existing_sessions.exists():
            messages.error(request, "There is existing session for this timeslot, choose another one.")
            return redirect("create-session", expert_id=expert_id)

        CoachingSession.objects.create(
            student=request.user,
            expert_id=expert_id,
            start_time=session_start_time,
            end_time=session_end_time
        )

        messages.success(request, "🎉 Your session was successfully scheduled.")
        return redirect("create-session", expert_id=expert_id)

    return render(request, "coaching/sessions.html", {"expert_id": expert_id})


def joinSession(request, session_id, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        messages.error("You have to be logged in to join session")
        return redirect("login")
    try:
        session = CoachingSession.objects.get(id=session_id)
    except CoachingSession.DoesNotExist:
        messages.error(request, "The session does not exist")
    
    if session.student == user or session.expert == user:
        messages.success(request, "Successfully joined the session")
    
    else:
        messages.error(request, "You cannot join this session")
    session.state = CoachingSessionStateChoices.started
    session.save()
    context = {
        "session_id": session_id,
        "expert": session.expert_id,
        "student": session.student_id,
        "student_email": session.student.email,
        "expert_email": session.expert.email,
        "session_state": session.state
    }
    return render(request, "coaching/joinSession.html", context=context)


def completeSession(request, session_id, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        messages.error("You have to be logged in to join session")
        return redirect("login")
    try:
        session = CoachingSession.objects.get(id=session_id)
    except CoachingSession.DoesNotExist:
        messages.error(request, "The session does not exist")
    
    if session.student == user or session.expert == user:
        messages.success(request, "Session completed successfully")
        # fire api for generating summary
    else:
        messages.error(request, "You cannot end this session")
    session.state = CoachingSessionStateChoices.completed
    session.save()
    return redirect("home")
