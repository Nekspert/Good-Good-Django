from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import Resolver404, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, UpdateView
from django.core.cache import cache

from .forms import AddPostForm, ContactForm
from .models import TagPost, Women
from .utils import DataMixin


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        w_list = cache.get('women_posts')
        if not w_list:
            w_list = Women.published.all().select_related('cat')
            cache.set('women_posts', w_list, 30)
        return w_list


# def handle_upload_file(f):
#     with open(f'uploads/{f.name}', mode='wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


@login_required
def about(request: HttpRequest):
    women = Women.published.all()
    paginator = Paginator(women, 3)

    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    return render(request, 'women/about.html',
                  {'title': 'О сайте', 'page_obj': page_obj})


class ShowPost(PermissionRequiredMixin, DataMixin, DetailView):
    template_name = 'women/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'
    permission_required = 'women.view_women'

    def get_context_data(self, **kwargs):
        context = super(ShowPost, self).get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=...):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class DeletePage(PermissionRequiredMixin, DeleteView):
    model = Women
    slug_url_kwarg = 'post_slug'
    success_url = reverse_lazy('home')
    permission_required = 'women.delete_women'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return HttpResponsePermanentRedirect(reverse_lazy('home'))


class AddPage(PermissionRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')  # get_absolute_url
    title_page = 'Добавление статьи'
    permission_required = 'women.add_women'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super(AddPage, self).form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    permission_required = 'women.change_women'
    slug_url_kwarg = 'post_slug'


class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')
    title_page = 'Обратная связь'

    def form_valid(self, form):
        return super(ContactFormView, self).form_valid(form)


def login(request: HttpRequest):
    return HttpResponse('Authorization')


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super(WomenCategory, self).get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk)

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


class WomenTagList(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super(WomenTagList, self).get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context,
                                      title=f'Тег: {tag.tag}')

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


def page_not_found(request: HttpRequest, exception: Resolver404):
    return HttpResponseNotFound('<h1>Page not found</h1>')
