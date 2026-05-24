from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import CustomUser, Post
from .forms import UserCreateForm, PostForm


class LoginView(View):
    def get(self, request):
        return render(request, 'blog/login.html')

    def post(self, request):
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user is not None:
            login(request, user)
            return redirect('post_list')
        messages.error(request, 'Неверный логин или пароль')
        return render(request, 'blog/login.html')


class LogoutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        return redirect('login')


class RegisterUserView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role != 'admin':
            messages.error(request, 'Доступ запрещён')
            return redirect('post_list')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = UserCreateForm()
        users = CustomUser.objects.all()
        return render(request, 'blog/register.html', {'form': form, 'users': users})

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь создан')
            return redirect('register')
        users = CustomUser.objects.all()
        return render(request, 'blog/register.html', {'form': form, 'users': users})


class DeleteUserView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role != 'admin':
            messages.error(request, 'Доступ запрещён')
            return redirect('post_list')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        if user == request.user:
            messages.error(request, 'Нельзя удалить себя')
            return redirect('register')
        user.delete()
        return redirect('register')


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role not in ['admin', 'poster']:
            messages.error(request, 'Доступ запрещён')
            return redirect('post_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if request.user.is_authenticated:
            if request.user.role != 'admin' and post.author != request.user:
                messages.error(request, 'Доступ запрещён')
                return redirect('post_list')
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if request.user.is_authenticated:
            if request.user.role != 'admin' and post.author != request.user:
                messages.error(request, 'Доступ запрещён')
                return redirect('post_list')
        return super().dispatch(request, *args, **kwargs)


class HomeRedirectView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('post_list')
        return redirect('login')
