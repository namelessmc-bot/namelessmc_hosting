from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from .models import Website
from .utils import pass_gen


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created, please log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form':form})


@login_required
def account(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account information has been updated.')
            return redirect('account')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'users/account.html', {'form': form})


class WebsiteListView(LoginRequiredMixin, ListView):
    model = Website
    # login_required = True
    #template_name =
    context_object_name = 'websites'
    ordering = ['date_created']

    def get_queryset(self):
        return Website.objects.filter(owner=self.request.user)


class WebsiteDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Website
    context_object_name = 'website'

    def test_func(self):
        website = self.get_object()
        return self.request.user == website.owner


class WebsiteCreateView(LoginRequiredMixin, CreateView):
    model = Website
    fields = ['name', 'domain']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class WebsiteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Website
    # fields = ['name', 'domain', 'use_https']
    fields = ['name', 'domain']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        website = self.get_object()
        return self.request.user == website.owner


class WebsiteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Website
    context_object_name = 'website'
    success_url = '/websites'

    def test_func(self):
        website = self.get_object()
        return self.request.user == website.owner


def website_db_pass_regen(request, pk):
    website = Website.objects.get(pk=pk)
    website.db_password = pass_gen()
    website.save()
    return redirect('website-detail', pk=pk)
