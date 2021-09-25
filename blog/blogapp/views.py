from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import ContextMixin

from .models import Post, Tag
from .forms import ContactForm, PostForm
from django.core.mail import send_mail


# Create your views here.
def main_view(request):
    posts = Post.objects.all()
    return render(request, 'blogapp/index.html', context={'posts': posts})


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Получить данные из форы
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']

            send_mail(
                'Contact message',
                f'Ваш сообщение {message} принято',
                'from@example.com',
                [email],
                fail_silently=True,
            )
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            return render(request, 'blogapp/contact.html', context={'form': form})
    else:
        form = ContactForm()
        return render(request, 'blogapp/contact.html', context={'form': form})


# можт читать только админ
@user_passes_test(lambda u: u.is_superuser)
def post(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blogapp/post.html', context={'post': post})


@login_required
def create_post(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'blogapp/create.html', context={'form': form})
    else:
        form = PostForm(request.POST, files=request.FILES)
        if form.is_valid():
            # Добавить в форму текущего пользователя request.user - текущий пользователь
            form.instance.user = request.user
            form.save()
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            return render(request, 'blogapp/create.html', context={'form': form})


class NameContextMixin(ContextMixin):

    def get_context_data(self, *args, **kwargs):
        """
        Отвечает за передачу параметров в контекст
        :param args:
        :param kwargs:
        :return:
        """
        context = super().get_context_data(*args, **kwargs)
        context['name'] = 'Теги'
        return context


# CRUD CREATE, READ (LIST, DETAIL), UPDATE, DELETE
# список тегов
class TagListView(ListView, NameContextMixin):
    model = Tag
    template_name = 'blogapp/tag_list.html'
    context_object_name = 'tags'

    def get_queryset(self):
        """
        Получение данных
        :return:
        """
        return Tag.objects.all()


# детальная информация
class TagDetailView(UserPassesTestMixin, DetailView, NameContextMixin):
    model = Tag
    template_name = 'blogapp/tag_detail.html'
    raise_exception = False

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        """
        Метод обработки get запроса
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.tag_id = kwargs['pk']
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """
        Получение этого объекта
        :param queryset:
        :return:
        """
        return get_object_or_404(Tag, pk=self.tag_id)


# создание тега
# Важно LoginRequiredMixin - он должен идти 1-ым
class TagCreateView(LoginRequiredMixin, CreateView, NameContextMixin):
    # form_class =
    fields = '__all__'
    model = Tag
    success_url = reverse_lazy('blog:tag_list')
    template_name = 'blogapp/tag_create.html'

    def post(self, request, *args, **kwargs):
        """
        Пришел пост запрос
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Метод срабатывает после того как форма валидна
        :param form:
        :return:
        """
        # self.request.user - текущий пользователь
        # form.instance.user = self.request.user
        return super().form_valid(form)


class TagUpdataView(UpdateView):
    fields = '__all__'
    model = Tag
    success_url = reverse_lazy('blog:tag_list')
    template_name = 'blogapp/tag_create.html'


class TagDeleteView(DeleteView):
    template_name = 'blogapp/tag_delete_confirm.html'
    model = Tag
    success_url = reverse_lazy('blog:tag_list')
