import copy
from unittest import mock

from django.db import DatabaseError
from django.test import TestCase
from django.urls import reverse

from .demo import DEMO_CARDS, DEMO_TEXT
from .models import Flashcard, Source
from .services import GenerationError, validate_cards


class TeachMeFlowTests(TestCase):
    def post_demo(self, text=DEMO_TEXT):
        return self.client.post(reverse('home'), {'title': 'Компьютерные сети', 'text': text})

    def test_valid_demo_post_saves_source_and_three_cards(self):
        response = self.post_demo()
        source = Source.objects.get()
        self.assertRedirects(response, reverse('source_detail', args=[source.pk]))
        self.assertEqual(Source.objects.count(), 1)
        self.assertEqual(Flashcard.objects.count(), 3)
        self.assertEqual(source.generation_mode, 'demo')

    def test_short_text_does_not_call_provider(self):
        with mock.patch('study.views.generate_cards') as provider:
            response = self.post_demo(text='IP-адрес бул адрес!!')
        provider.assert_not_called()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Source.objects.count(), 0)

    def test_wrong_quote_rejects_whole_answer(self):
        cards = copy.deepcopy(DEMO_CARDS)
        cards[2]['source_quote'] = 'Этого предложения нет в конспекте.'
        with self.assertRaises(GenerationError):
            validate_cards({'cards': cards}, DEMO_TEXT)

    def test_provider_error_returns_bound_form_without_db_rows(self):
        with mock.patch('study.views.generate_cards', side_effect=GenerationError('Провайдер қатесі')):
            response = self.post_demo()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Провайдер қатесі')
        self.assertEqual(response.context['form'].data['title'], 'Компьютерные сети')
        self.assertEqual(Source.objects.count(), 0)
        self.assertEqual(Flashcard.objects.count(), 0)

    def test_database_error_on_second_card_rolls_back_everything(self):
        real_create = Flashcard.objects.create
        calls = {'n': 0}

        def flaky_create(**kwargs):
            calls['n'] += 1
            if calls['n'] == 2:
                raise DatabaseError('disk full')
            return real_create(**kwargs)  # the first card is really written

        with mock.patch.object(Flashcard.objects, 'create', side_effect=flaky_create):
            response = self.post_demo()
        self.assertEqual(calls['n'], 2)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'сақтау мүмкін болмады')
        self.assertEqual(Source.objects.count(), 0)
        self.assertEqual(Flashcard.objects.count(), 0)

    def test_detail_get_twice_does_not_call_provider_or_change_db(self):
        self.post_demo()
        source = Source.objects.get()
        url = reverse('source_detail', args=[source.pk])
        with mock.patch('study.views.generate_cards') as provider:
            first = self.client.get(url)
            second = self.client.get(url)
        provider.assert_not_called()
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertContains(second, 'Жауапты көрсету')
        self.assertEqual(Source.objects.count(), 1)
        self.assertEqual(Flashcard.objects.count(), 3)
