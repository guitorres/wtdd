from django.shortcuts import render
from eventex.subscriptions.forms import SubscriptionForm
from django.http import HttpResponseRedirect
from django.core import mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
from eventex.subscriptions.models import Subscription

def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def create(request):
    form = SubscriptionForm(request.POST)
    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form': form})
    
    _send_mail(
        template_name = 'subscriptions/subscription_email.txt',
        context = form.cleaned_data,
        subject = 'Confirmação de inscrição',
        from_ = settings.DEFAULT_FROM_EMAIL,
        to = form.cleaned_data['email'],        
    )

    Subscription.objects.create(**form.cleaned_data)

    messages.success(request, 'Inscrição realizada com sucesso!')
    return HttpResponseRedirect('/inscricao/')       


def new(request):
    return render(request, 'subscriptions/subscription_form.html', {'form': SubscriptionForm()})


def _send_mail(template_name, context, subject, from_, to):        
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
