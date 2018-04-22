import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from mainapp.models import Individu, Message
from mainapp.forms import MessageForm


@login_required
def message(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            try:
                destinataire = form.data['destinataire']
                message = form.data['message']
                user2 = Individu(id=destinataire.split('#')[-1])
                Message(user1=request.user.individu, user2=user2, message=message).save()
            except ValueError:
                messages.add_message(request, messages.ERROR, "Le destinataire n'existe pas.")
        else:
            messages.add_message(request, messages.ERROR, "Le message ou l'utilisateur n'ont pas été saisis.")
    list_messages = Message.objects.filter(user1=request.user.individu) | Message.objects.filter(user2=request.user.individu)
    list_messages = list_messages.order_by('date')
    all_user = Individu.objects.all()
    return render(request, 'mainapp/messages.html', {"list_messages": list_messages, "all_user": all_user})


@csrf_exempt
@login_required
def supprimer_message(request):
    if request.method == 'POST':
        post = request.POST['message']
        message = json.loads(post)
        Message.objects.get(id=message).delete()
        json_data = json.dumps({"message": message})
        return HttpResponse(json_data)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
