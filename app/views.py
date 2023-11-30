from django.http import HttpResponseRedirect
from django.urls import reverse


# redirect 'home' view to posts_top
def home(_):
    return HttpResponseRedirect(reverse("posts:top"))
