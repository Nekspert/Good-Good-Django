from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.models import User
from women.models import Women


class GetPagesTestCase(TestCase):
    fixtures = ['women_women.json', 'women_category.json', 'women_husband.json', 'women_tagpost.json', ]

    def setUp(self):
        """Инициализация перед выполнением каждого теста"""
        self.user = User.objects.create_superuser(
                username='neksper',
                password='1234'
        )

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path=path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # self.assertIn('women/index.html', response.template_name)
        self.assertTemplateUsed(response, 'women/index.html')
        self.assertEqual(response.context_data['title'], 'Главная страница')

    def test_redirect_addpage(self):
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path=path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_data_mainpage(self):
        w = Women.published.all().select_related('cat')
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerySetEqual(response.context_data['posts'], w[:5])

    def test_paginate_mainpage(self):
        path = reverse('home')
        page = 2
        paginate_by = 5
        response = self.client.get(path + f'?page={page}')
        w = Women.published.all().select_related('cat')
        self.assertQuerySetEqual(response.context_data['posts'], w[(page - 1) * paginate_by: paginate_by * page])

    def test_content_post(self):
        w = Women.published.get(pk=1)
        path = reverse('post', args=(w.slug,))
        response = self.client.get(path)
        data = {
            'username': 'neksper',
            'password': 1234,
        }
        response = self.client.post(response.url, data, follow=True)
        self.assertEqual(w.content, response.context_data['post'].content)

    def tearDown(self):
        """Действия после выполнения каждого теста"""
        ...
