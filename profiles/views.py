from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import Http404
from .models import Profile
from .forms import ProfileForm

# Create your views here.

def profile_update_view(request,*args,**kwargs):
    if not request.user.is_authenticated:
        return redirect("/login?next=/profile/update")
    user = request.user
    my_profile =user.profile
    form = ProfileForm(request.POST or None,
                       instance=my_profile,initial={"first_name":"ephraim",
                                                                         "last_name":"njogu"})
    if form.is_valid():
        profile_obj = form.save(commit=False)
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        profile_obj.save()
    context = {
        "form":form,
    }
    return render(request,"profiles/detail.html",context)


def profile_detail_view(request,username):
    qs = Profile.objects.filter(user__username = username)
    if not qs.exists():
        raise Http404
    profile_obj = qs.first()
    context = {
        "profile":profile_obj,
        "username":username

    }
    return render(request,'profile.html',context)