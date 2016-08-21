from urllib import quote_plus
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Post
from .forms import PostForm
from django.contrib import  messages
from django.db.models import Q

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.utils import timezone


def posts_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated:
        raise Http404

    form  = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get('title'))
        instance.user = request.user
        instance.save()
        messages.success(request, "<a href='#'>Post</a> Created", extra_tags='html_safe')
        return  HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Error happend")
    context = {
        'form': form,
    }
    # if request.method == "POST":
    #     print(request.POST.get('content'))
    #     print(request.POST.get('title'))
    return render(request, 'post_form.html', context)



def posts_detail(request, slug = None):
    # data = Post.objects.get(id=100)
    data = get_object_or_404(Post, slug=slug)
    share_string = quote_plus(data.content)
    if data.draft or data.publish > timezone.now():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    context = {
        "title": "detail",
        "i" : data,
        "share_string": share_string,
    }
    return render( request, 'post_detail.html', context)


def posts_list(request):
    context = {}
    today = timezone.now()
    data_list= Post.objects.active()         #.order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        data_list = Post.objects.all()
    query = request.GET.get("q")
    if query:
        data_list = data_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__username__icontains=query)

        ).distinct()

    paginator = Paginator(data_list, 5) # Show 25 contacts per page
    page_reques_var = "page"
    page = request.GET.get(page_reques_var)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        data = paginator.page(paginator.num_pages)

    context['posts'] = data
    context['page_reques_var'] = page_reques_var
    context['today'] = today
    return render(request, 'post_list.html', context=context)




def posts_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form  = PostForm(request.POST or None, request.FILES  or None, instance=instance) #instance here populates the feilds.
    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get('title'))
        instance.save()
        messages.success(request, "<a href='#'>Post</a> Updated", extra_tags='html_safe')
        return  HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title': instance.title,
         "i": instance,
        'form': form,
    }

    return render(request, 'post_form.html', context)



def posts_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance =  get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Post deleted")
    return redirect("posts:list")

