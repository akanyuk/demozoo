from django.contrib.auth.models import User
from django.test import TestCase

from bbs.models import BBS
from demoscene.models import Edit
from productions.models import Production


class TestIndex(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        response = self.client.get('/bbs/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "StarPort")


class TestShow(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        bbs = BBS.objects.get(name='StarPort')
        response = self.client.get('/bbs/%d/' % bbs.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "StarPort")


class TestCreate(TestCase):
    fixtures = ['tests/gasman.json']

    def setUp(self):
        User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_get(self):
        response = self.client.get('/bbs/new/')
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post('/bbs/new/', {
            'name': 'Eclipse',
            'location': '',
        })
        self.assertRedirects(response, '/bbs/%d/' % BBS.objects.get(name='Eclipse').id)


class TestEdit(TestCase):
    fixtures = ['tests/gasman.json']

    def setUp(self):
        User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.bbs = BBS.objects.get(name='StarPort')

    def test_get(self):
        response = self.client.get('/bbs/%d/edit/' % self.bbs.id)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post('/bbs/%d/edit/' % self.bbs.id, {
            'name': 'StarWhisky',
            'location': 'Oxford',
        })
        self.assertRedirects(response, '/bbs/%d/' % self.bbs.id)


class TestEditNotes(TestCase):
    fixtures = ['tests/gasman.json']

    def setUp(self):
        User.objects.create_superuser(username='testsuperuser', email='testsuperuser@example.com', password='12345')
        self.client.login(username='testsuperuser', password='12345')
        self.bbs = BBS.objects.get(name='StarPort')

    def test_non_superuser(self):
        User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/bbs/%d/edit_notes/' % self.bbs.id)
        self.assertRedirects(response, '/bbs/%d/' % self.bbs.id)

    def test_get(self):
        response = self.client.get('/bbs/%d/edit_notes/' % self.bbs.id)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post('/bbs/%d/edit_notes/' % self.bbs.id, {
            'notes': 'purple motion ad lib music etc',
        })
        self.assertRedirects(response, '/bbs/%d/' % self.bbs.id)


class TestDelete(TestCase):
    fixtures = ['tests/gasman.json']

    def setUp(self):
        User.objects.create_superuser(username='testsuperuser', email='testsuperuser@example.com', password='12345')
        self.client.login(username='testsuperuser', password='12345')
        self.bbs = BBS.objects.get(name='StarPort')

    def test_non_superuser(self):
        User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/bbs/%d/delete/' % self.bbs.id)
        self.assertRedirects(response, '/bbs/%d/' % self.bbs.id)

    def test_get(self):
        response = self.client.get('/bbs/%d/delete/' % self.bbs.id)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post('/bbs/%d/delete/' % self.bbs.id, {
            'yes': 'yes'
        })
        self.assertRedirects(response, '/bbs/')
        self.assertFalse(BBS.objects.filter(name='StarPort').exists())

    def test_cancel(self):
        response = self.client.post('/bbs/%d/delete/' % self.bbs.id, {
            'no': 'no'
        })
        self.assertRedirects(response, '/bbs/%d/' % self.bbs.id)
        self.assertTrue(BBS.objects.filter(name='StarPort').exists())


class TestEditBBStros(TestCase):
    fixtures = ['tests/gasman.json']

    def setUp(self):
        User.objects.create_superuser(username='testsuperuser', email='testsuperuser@example.com', password='12345')
        self.client.login(username='testsuperuser', password='12345')
        self.bbs = BBS.objects.get(name='StarPort')
        self.pondlife = Production.objects.get(title='Pondlife')

    def test_get(self):
        response = self.client.get('/bbs/%d/edit_bbstros/' % self.bbs.id)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post('/bbs/%d/edit_bbstros/' % self.bbs.id, {
            'form-TOTAL_FORMS': 1,
            'form-INITIAL_FORMS': 0,
            'form-MIN_NUM_FORMS': 0,
            'form-MAX_NUM_FORMS': 1000,
            'form-0-production_id': self.pondlife.id,
            'form-0-production_title': 'Pondlife',
            'form-0-production_byline_search': '',
        })
        self.assertRedirects(response, '/bbs/%d/' % self.bbs.id)
        self.assertEqual(self.bbs.bbstros.count(), 1)

        edit = Edit.for_model(self.bbs, True).first()
        self.assertEqual("Set BBStros to Pondlife", edit.description)

        # no change => no edit log entry added
        edit_count = Edit.for_model(self.bbs, True).count()
        response = self.client.post('/bbs/%d/edit_bbstros/' % self.bbs.id, {
            'form-TOTAL_FORMS': 1,
            'form-INITIAL_FORMS': 1,
            'form-MIN_NUM_FORMS': 0,
            'form-MAX_NUM_FORMS': 1000,
            'form-0-production_id': self.pondlife.id,
            'form-0-production_title': 'Pondlife',
            'form-0-production_byline_search': '',
        })
        self.assertRedirects(response, '/bbs/%d/' % self.bbs.id)
        self.assertEqual(edit_count, Edit.for_model(self.bbs, True).count())
