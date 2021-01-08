from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models import F
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from .forms import UserRegisterForm, UserUpdateForm
from .models import Website, Voucher, Account, Job
from . import utils


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created, please log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form':form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account')
        # else:
            # messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })


@login_required
def account(request):
    if request.method == 'POST':
        if 'update-account' in request.POST:
            update_form = UserUpdateForm(request.POST, instance=request.user)
            if update_form.is_valid():
                update_form.save()
                messages.success(request, 'Your account information has been updated.')
                return redirect('account')
        elif 'redeem-voucher' in request.POST:
            vouchers = Voucher.objects.filter(code=request.POST.get('code', ''))
            if vouchers.exists():
                voucher = vouchers.first()
                credits_to_add = voucher.amount
                voucher.delete()
                Account.objects.filter(user=request.user).update(credit=F('credit') + credits_to_add)
                messages.success(request, f'Voucher redeemed, added {credits_to_add} credits to your account.')
            else:
                messages.warning(request, 'Voucher invalid or already redeemed')

            return redirect('account')
        else:
            return HttpResponse('Invalid request')

    else:
        update_form = UserUpdateForm(instance=request.user)

    user_id = request.user.id

    paypal_dict_30 = {
        "business": "rs.systems@derkad.es",
        "amount": "5.00",
        "item_name": "30 Named Hosting Credits",
        "item_number": "credits_30",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment-complete')),
        "cancel_return": request.build_absolute_uri(reverse('payment-cancelled')),
        "custom": str(user_id),
    }

    paypal_dict_100 = {
        "business": "rs.systems@derkad.es",
        "amount": "10.00",
        "item_name": "100 Named Hosting Credits",
        "item_number": "credits_100",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment-complete')),
        "cancel_return": request.build_absolute_uri(reverse('payment-cancelled')),
        "custom": str(user_id),
    }

    form_30 = PayPalPaymentsForm(initial=paypal_dict_30)
    form_100 = PayPalPaymentsForm(initial=paypal_dict_100)

    context = {
        "update_form": update_form,
        "buy_form_30": form_30,
        "buy_form_100": form_100,
    }

    return render(request, 'users/account.html', context)


class WebsiteListView(LoginRequiredMixin, ListView):
    model = Website
    #template_name =
    context_object_name = 'websites'
    ordering = ['date_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_create_button'] = not utils.is_over_website_limit(self.request.user)
        return context

    def get_queryset(self):
        return Website.objects.filter(owner=self.request.user)


class WebsiteDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Website
    context_object_name = 'website'

    def test_func(self):
        website = self.get_object()
        return self.request.user == website.owner or self.request.user.is_superuser


class WebsiteCreateView(LoginRequiredMixin, CreateView):
    model = Website
    fields = ['name', 'domain', 'version']

    def form_valid(self, form):
        form.instance.owner = self.request.user

        if utils.is_over_website_limit(self.request.user):
            return HttpResponse('Too many websites')

        return super().form_valid(form)


class WebsiteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Website
    fields = ['name', 'domain', 'www', 'version', 'use_https']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        website = self.get_object()
        return self.request.user == website.owner or self.request.user.is_superuser


class WebsiteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Website
    context_object_name = 'website'
    success_url = '/websites'

    def test_func(self):
        website = self.get_object()
        return self.request.user == website.owner or self.request.user.is_superuser


@login_required
def website_reset(request, pk):
    if request.method == 'POST':
        # Clicked OK
        if request.user == Website.objects.filter(pk=pk).first().owner:
            if Job.objects.filter(type=Job.RESET_WEBSITE, content=pk, done=False, running=False).exists():
                print('Skipped creating job to prevent duplicates')
            else:
                Job.objects.create(type=Job.RESET_WEBSITE, priority=Job.NORMAL, content=pk)
            return redirect('website-detail', pk)
        else:
            return HttpResponse("Invalid request")
    else:
        # Display 'Are you sure?'
        websites = Website.objects.filter(pk=pk)
        if not websites.exists():
            return HttpResponseNotFound()

        return render(request, 'users/website_reset.html', context={'website': websites.first()})


@login_required
def website_db_pass_regen(request, pk):
    website = Website.objects.get(pk=pk)
    print(website.owner, flush=True)
    print(request.user, flush=True)
    if website.owner != request.user:
        return HttpResponse('Permission denied')

    website.db_password = utils.pass_gen()
    website.save()
    return redirect('website-detail', pk=pk)


@csrf_exempt
def payment_complete(request):
    return render(request, template_name='users/payment_complete.html')
