from django.shortcuts import render
from eventex.subscriptions.forms import SubscriptionForm
from django.http import HttpResponseRedirect
from django.core import mail
from django.template.loader import render_to_string
from django.conf import settings
from eventex.subscriptions.models import Subscription
from django.http import Http404

def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def create(request):
    form = SubscriptionForm(request.POST)
    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form': form})

    subscription = Subscription.objects.create(**form.cleaned_data)

    _send_mail(
        template_name = 'subscriptions/subscription_email.txt',
        context = {'subscription': subscription},
        subject = 'Confirmação de inscrição',
        from_ = settings.DEFAULT_FROM_EMAIL,
        to = subscription.email,
    )

    return HttpResponseRedirect('/inscricao/{}/'.format(subscription.pk))


def new(request):
    return render(request, 'subscriptions/subscription_form.html', {'form': SubscriptionForm()})


def detail(request, pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404
    return render(request, 'subscriptions/subscription_detail.html', { 'subscription': subscription })


def _send_mail(template_name, context, subject, from_, to):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
