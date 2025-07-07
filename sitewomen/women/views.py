from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.urls import Resolver404, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import AddPostForm, UploadFileForm
from .models import TagPost, UploadFiles, Women
from .utils import DataMixin


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Women.published.all().select_related('cat')


# def handle_upload_file(f):
#     with open(f'uploads/{f.name}', mode='wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def about(request: HttpRequest):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'women/about.html',
                  {'title': 'О сайте', 'form': form})


class ShowPost(DataMixin, DetailView):
    template_name = 'women/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super(ShowPost, self).get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=...):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')  # get_absolute_url
    title_page = 'Добавление статьи'


class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'


def contact(request: HttpRequest):
    return HttpResponse('Feedback')


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
