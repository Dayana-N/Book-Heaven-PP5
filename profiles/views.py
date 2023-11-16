from django.shortcuts import get_object_or_404, render

from .models import UserProfile


# Create your views here.
def profile_page(request, pk):
    profile = get_object_or_404(UserProfile, id=pk)
    context = {
        'profile': profile,
    }
    return render(request, 'profiles/profile.html', context)
