from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from mylist.models import Mylist
# Create your views here.

@login_required
def change_item_status(request):
    choice = request.POST['choice']
    item_id = request.POST['item_id']
    item = Mylist.objects.get(id = item_id)

    if choice == 'done':
        item.status = True
        item.save()
    elif choice == 'redo':
        item.status = False
        item.save()
    elif choice == 'remove':
        item.delete()
    else:
        return HttpResponse('ERROR!')
    return HttpResponseRedirect('/')


@login_required
def add_item(request):
    item = request.POST['item']
    if item:
        Mylist.objects.create(
            user = request.user,
            item = item,
        )
    return HttpResponseRedirect('/')


@login_required
def view_of_item_list(request):
    if request.method == 'POST':
        #return HttpResponse(request.POST)
        if 'ok' in request.POST and 'choice' in request.POST:
            #return HttpResponse(request.POST)
            return change_item_status(request)
        if 'add' in request.POST:
            #return HttpResponse(request.POST)
            return add_item(request)

    items = Mylist.objects.filter(
        user = request.user,
        status = False,
    )

    done_items = Mylist.objects.filter(
        user = request.user,
        status = True,
    )

    context = {
        'items' : items,
        'done_items' : done_items,
    }

    return render(request, 'index.html', context)
