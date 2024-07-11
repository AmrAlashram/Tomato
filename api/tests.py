from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import json
from .models import ristorante, ingrediente, ricetta

################## Ristorante APIs Testing ##################

class creare_un_ristorante_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.ristorante_payload = {
            'nome': 'test ristorante 1',
            'indirizzo': '1 via testing',
        }
    
    def test_creare_un_ristorante(self):
        url = reverse('creare-un-ristorante')
        response = self.client.post(url, self.ristorante_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ristorante.objects.count(), 1)
        self.assertEqual(ristorante.objects.get().nome, 'test ristorante 1')

    def tearDown(self):
        ristorante.objects.all().delete()

class aggiornare_un_ristorante_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.ristorante1 = ristorante.objects.create(nome='test ristorante 1', indirizzo='1 via test')

    def test_aggiornare_un_ristorante(self):
        url = reverse('aggiornare-un-ristorante', args=[self.ristorante1.nome])
        aggiornati_dati = {
            'nome': 'aggiornato test ristorante 1',
            'indirizzo': 'aggiornato 1 via test'
        }
        response = self.client.put(url, aggiornati_dati, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ristorante1.refresh_from_db()
        self.assertEqual(self.ristorante1.nome, 'aggiornato test ristorante 1')
        self.assertEqual(self.ristorante1.indirizzo, 'aggiornato 1 via test')

    def tearDown(self):
        ristorante.objects.all().delete()

class eliminare_un_ristorante_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.ristorante1 = ristorante.objects.create(nome='test ristorante 1', indirizzo='1 via test')

    def test_eliminare_un_ristorante(self):
        url = reverse('eliminare-un-ristorante', args=[self.ristorante1.nome])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ristorante.objects.filter(nome=self.ristorante1.nome).exists())

    def tearDown(self):
        ristorante.objects.all().delete()

class ristoranti_tutti_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.ristorante1 = ristorante.objects.create(nome='test ristorante 1', indirizzo='1 via testing')
        self.ristorante2 = ristorante.objects.create(nome='test ristorante 2', indirizzo='2 via testing')

    def test_ristoranti_tutti(self):
        url = reverse('list-ristoranti')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def tearDown(self):
        ristorante.objects.all().delete()

class ristoranti_per_ricetta_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.nome_di_ricetta = 'test ricetta 1'
        ristorante1 = ristorante.objects.create(nome='test ristorante 1', indirizzo='1 via testing')
        ristorante2 = ristorante.objects.create(nome='test ristorante 2', indirizzo='2 via testing')
        ingrediente1 = ingrediente.objects.create(nome='test ingrediente 1')
        ingrediente2 = ingrediente.objects.create(nome='test ingrediente 2')
        ricetta1 = ricetta.objects.create(nome= self.nome_di_ricetta)
        ricetta1.ristorante.add(ristorante1)
        ricetta1.ingrediente.add(ingrediente1)
        ricetta1.ingrediente.add(ingrediente2)

    def test_ristoranti_per_ricetta(self):
        url = reverse('ristoranti-per-ricetta', args=[self.nome_di_ricetta])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)  # Both restaurants should be associated with the recipe

    def tearDown(self):
        ristorante.objects.all().delete()
        ricetta.objects.all().delete()
        ingrediente.objects.all().delete()



################## Ricetta APIs Testing ##################

class creare_un_ricetta_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.ristorante1 = ristorante.objects.create(nome='test ristorante 1', indirizzo='1 via testing')
        self.ristorante2 = ristorante.objects.create(nome='test ristorante 2', indirizzo='2 via testing')
        self.ingrediente1 = ingrediente.objects.create(nome='test ingrediente 1')
        self.ingrediente2 = ingrediente.objects.create(nome='test ingrediente 2')
        self.ricetta_payload = {
            'nome': 'test ricetta 1',
            'ristorante': [self.ristorante1.nome, self.ristorante2.nome],
            'ingrediente': [self.ingrediente1.nome, self.ingrediente2.nome]
        }
    
    def test_creare_un_ricetta(self):
        url = reverse('creare-una-ricetta')
        response = self.client.post(url, self.ricetta_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ricetta.objects.count(), 1)
        self.assertEqual(ricetta.objects.get().nome, 'test ricetta 1')
        self.assertEqual(list(ricetta.objects.get().ristorante.values_list('id', flat=True)), [self.ristorante1.id, self.ristorante2.id])
        self.assertEqual(list(ricetta.objects.get().ingrediente.values_list('id', flat=True)), [self.ingrediente1.id, self.ingrediente2.id])

    def tearDown(self):
        ristorante.objects.all().delete()
        ricetta.objects.all().delete()
        ingrediente.objects.all().delete()

class aggiornare_una_ricetta_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.ristorante1 = ristorante.objects.create(nome='test ristorante 1', indirizzo='1 via testing')
        self.ristorante2 = ristorante.objects.create(nome='test ristorante 2', indirizzo='2 via testing')
        self.ingrediente1 = ingrediente.objects.create(nome='test ingrediente 1')
        self.ingrediente2 = ingrediente.objects.create(nome='test ingrediente 2')
        self.ricetta1 = ricetta.objects.create(nome='test ricetta 1')
        self.ricetta1.ristorante.add(self.ristorante1)
        self.ricetta1.ingrediente.add(self.ingrediente1)

    def test_aggiornare_una_ricetta(self):
        url = reverse('aggiornare-una-ricetta', args=[self.ricetta1.nome])
        aggiornati_dati = {
            'nome': 'aggiornata test ricetta 1',
            'ristorante': [self.ristorante2.nome],
            'ingrediente': [self.ingrediente2.nome]
        }
        response = self.client.put(url, aggiornati_dati, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ricetta1.refresh_from_db()
        self.assertEqual(self.ricetta1.nome, 'aggiornata test ricetta 1')
        self.assertEqual(list(self.ricetta1.ristorante.values_list('id', flat=True)), [self.ristorante2.id])
        self.assertEqual(list(self.ricetta1.ingrediente.values_list('id', flat=True)), [self.ingrediente2.id])

    def tearDown(self):
        ristorante.objects.all().delete()
        ricetta.objects.all().delete()
        ingrediente.objects.all().delete()

class eliminare_una_ricetta_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        ristorante1 = ristorante.objects.create(nome='test ristorante 1', indirizzo='1 via testing')
        ingrediente1 = ingrediente.objects.create(nome='test ingrediente 1')
        self.ricetta1 = ricetta.objects.create(nome='test ricetta 1')
        self.ricetta1.ristorante.add(ristorante1)
        self.ricetta1.ingrediente.add(ingrediente1)

    def test_eliminare_una_ricetta(self):
        url = reverse('eliminare-una-ricetta', args=[self.ricetta1.nome])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ricetta.objects.filter(nome=self.ricetta1.nome).exists())

    def tearDown(self):
        ristorante.objects.all().delete()
        ricetta.objects.all().delete()
        ingrediente.objects.all().delete()

class ricette_tutte_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        ristorante1 = ristorante.objects.create(nome='test ristorante 1', indirizzo='1 via testing')
        ristorante2 = ristorante.objects.create(nome='test ristorante 2', indirizzo='2 via testing')
        ingrediente1 = ingrediente.objects.create(nome='test ingrediente 1')
        ingrediente2 = ingrediente.objects.create(nome='test ingrediente 2')
        ricetta1 = ricetta.objects.create(nome='test ricetta 1')
        ricetta1.ristorante.add(ristorante1)
        ricetta1.ingrediente.add(ingrediente1)
        ricetta2 = ricetta.objects.create(nome='test ricetta 2')
        ricetta2.ristorante.add(ristorante2)
        ricetta2.ingrediente.add(ingrediente2)

    def test_ricette_tutte(self):
        url = reverse('list-ricette')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def tearDown(self):
        ristorante.objects.all().delete()
        ricetta.objects.all().delete()
        ingrediente.objects.all().delete()

class ricette_per_ristorante_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.nome_di_ristorante = 'test ristorante 1'
        ristorante1 = ristorante.objects.create(nome=self.nome_di_ristorante, indirizzo='1 via testing')
        ristorante2 = ristorante.objects.create(nome='test ristorante 2', indirizzo='2 via testing')
        ingrediente1 = ingrediente.objects.create(nome='test ingrediente 1')
        ingrediente2 = ingrediente.objects.create(nome='test ingrediente 2')
        ricetta1 = ricetta.objects.create(nome='test ricetta 1')
        ricetta1.ristorante.add(ristorante1)
        ricetta1.ingrediente.add(ingrediente1)
        ricetta2 = ricetta.objects.create(nome='test ricetta 2')
        ricetta2.ristorante.add(ristorante2)
        ricetta2.ingrediente.add(ingrediente2)

    def test_ricette_per_ristorante(self):
        url = reverse('ricette-per-ristorante', args=[self.nome_di_ristorante])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def tearDown(self):
        ristorante.objects.all().delete()
        ricetta.objects.all().delete()
        ingrediente.objects.all().delete()

class ricette_per_indgrediente_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.nome_di_ingrediente = 'test ingrediente 1'
        ristorante1 = ristorante.objects.create(nome='test ristorante 1', indirizzo='1 via testing')
        ristorante2 = ristorante.objects.create(nome='test ristorante 2', indirizzo='2 via testing')
        ingrediente1 = ingrediente.objects.create(nome=self.nome_di_ingrediente)
        ingrediente2 = ingrediente.objects.create(nome='test ingrediente 2')
        ricetta1 = ricetta.objects.create(nome='test ricetta 1')
        ricetta1.ristorante.add(ristorante1)
        ricetta1.ingrediente.add(ingrediente1)
        ricetta2 = ricetta.objects.create(nome='test ricetta 2')
        ricetta2.ristorante.add(ristorante2)
        ricetta2.ingrediente.add(ingrediente2)

    def test_ricette_per_indgrediente(self):
        url = reverse('ricette-per-ingrediente', args=[self.nome_di_ingrediente])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def tearDown(self):
        ristorante.objects.all().delete()
        ricetta.objects.all().delete()
        ingrediente.objects.all().delete()




################## Ingrediente APIs Testing ##################

class creare_un_ingrediente_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.ingrediente_payload = {
            'nome': 'test ingrediente 1'
        }
    
    def test_creare_un_ingrediente(self):
        url = reverse('creare-un-ingrediente')
        response = self.client.post(url, self.ingrediente_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ingrediente.objects.count(), 1)
        self.assertEqual(ingrediente.objects.get().nome, 'test ingrediente 1')

    def tearDown(self):
        ingrediente.objects.all().delete()

class aggiornare_un_ingrediente_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.ingrediente1 = ingrediente.objects.create(nome='test ingrediente 1')

    def test_aggiornare_un_ingrediente(self):
        url = reverse('aggiornare-un-ingrediente', args=[self.ingrediente1.nome])
        aggiornati_dati = {
            'nome': 'aggiornato test ingrediente 1',
        }
        response = self.client.put(url, aggiornati_dati, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ingrediente1.refresh_from_db()
        self.assertEqual(self.ingrediente1.nome, 'aggiornato test ingrediente 1')

    def tearDown(self):
        ingrediente.objects.all().delete()

class eliminare_un_ingrediente_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.ingrediente1 = ingrediente.objects.create(nome='test ingrediente 1')

    def test_eliminare_un_ristorante(self):
        url = reverse('eliminare-un-ingrediente', args=[self.ingrediente1.nome])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ingrediente.objects.filter(nome=self.ingrediente1.nome).exists())

    def tearDown(self):
        ingrediente.objects.all().delete()

class ingredienti_tutti_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.ingrediente1 = ingrediente.objects.create(nome='test ingrediente 1')
        self.ingrediente2 = ingrediente.objects.create(nome='test ingrediente 2')

    def test_ristoranti_tutti(self):
        url = reverse('list-ingredienti')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def tearDown(self):
        ristorante.objects.all().delete()

class ingredienti_per_ricetta_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.nome_di_ricetta = 'test ricetta 1'
        ristorante1 = ristorante.objects.create(nome='test ristorante 1', indirizzo='1 via testing')
        ingrediente1 = ingrediente.objects.create(nome='test ingrediente 1')
        ingrediente2 = ingrediente.objects.create(nome='test ingrediente 2')
        ricetta1 = ricetta.objects.create(nome= self.nome_di_ricetta)
        ricetta1.ristorante.add(ristorante1)
        ricetta1.ingrediente.add(ingrediente1)

    def test_ingredienti_per_ricetta(self):
        url = reverse('ingredienti-per-ricetta', args=[self.nome_di_ricetta])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def tearDown(self):
        ristorante.objects.all().delete()
        ricetta.objects.all().delete()
        ingrediente.objects.all().delete()

class ingredienti_per_ristorante_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.nome_di_ristorante = 'test ristorante 1'
        ristorante1 = ristorante.objects.create(nome= self.nome_di_ristorante , indirizzo='1 via testing')
        ingrediente1 = ingrediente.objects.create(nome='test ingrediente 1')
        ingrediente2 = ingrediente.objects.create(nome='test ingrediente 2')
        ricetta1 = ricetta.objects.create(nome= 'test ricetta 1')
        ricetta1.ristorante.add(ristorante1)
        ricetta1.ingrediente.add(ingrediente1)

    def test_ingredienti_per_ristorante(self):
        url = reverse('ingredienti-per-ristorante', args=[self.nome_di_ristorante])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def tearDown(self):
        ristorante.objects.all().delete()
        ricetta.objects.all().delete()
        ingrediente.objects.all().delete()