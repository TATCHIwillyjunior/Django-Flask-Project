from django.shortcuts import redirect
from django.contrib import messages

def author_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        profile = getattr(request.user, 'profile', None)
        if not profile:
            messages.error(request, "No profile associated with this account.")
            return redirect('story_list')
        if profile.role != 'author' and not request.user.is_staff:
            messages.error(request, "You are not allowed to access this page.")
            return redirect('story_list')
        return view_func(request, *args, **kwargs)
    return wrapper
