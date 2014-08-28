from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from newzuul.models import consumer, items

# Create your views here.


def purchase_item(person, item_id, ammount):
    try:
        item = get_object_or_404(items, pk=item_id)
    except (ValueError):
        return False
    else:
        person.bank -= item.price * int(ammount)
        person.save()
        return True


def creat_item(name_in, price_in):
    new_item = items(name=name_in, price=price_in)
    new_item.save()


def create_consumer(name_in, bank_in):
    new_consumer = consumer(name=name_in, bank=bank_in)
    new_consumer.save()


def index(request):
    consumer_list = consumer.objects.order_by('name')
    item_list = items.objects.order_by('price')
    context = {'consumer_list': consumer_list,
               'item_list': item_list}
    return render(request, 'newzuul/index.html', context)


def purchaselist(request, user_id):
    person = get_object_or_404(consumer, pk=user_id)
    item_list = items.objects.order_by('price')
    context = {'item_list': item_list, 'person': person}
    return render(request, 'newzuul/purchaselist.html', context)


def purchaseaction(request, user_id):
    try:
        person = get_object_or_404(consumer, pk=user_id)
    except (ValueError):
        return HttpResponse(" he's dead Jim (ValueError on person object)")
    else:
        for key in request.POST:
            purchase_item(person, key, request.POST[key]):
                #print exception error on webpage
                return HttpResponse('Hes dead Jim (purchase_item f)')
        #return HttpResponse('did it!')
        return redirect('newzuul:purchaselist.html')  # causes 400 error on runserver