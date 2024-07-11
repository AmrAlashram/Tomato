from django.http import JsonResponse, HttpResponseNotAllowed
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.parsers import JSONParser
from .serializers import ristoranteSerializer, ricettaSerializer, ingredienteSerializer
from .models import ristorante, ricetta, ingrediente


######################  Ristoranti  ######################

def creare_un_ristorante(request):
    if request.method == 'POST':
        dati = JSONParser().parse(request)
        serializer = ristoranteSerializer(data=dati)
        if serializer.is_valid():
            ristorante = serializer.save()
            return JsonResponse({'success': True, 'nome': ristorante.nome}, status=201)
        return JsonResponse({'success': False, 'errors': serializer.errors}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])

def eliminare_un_ristorante(request, nome_di_ristorante):
    if request.method == 'DELETE':
        try:
            ristorante_object = ristorante.objects.get(nome=nome_di_ristorante)
            ristorante_object.delete()
            return JsonResponse({'message': f'ristorante "{nome_di_ristorante}" deleted successfully'}, status=204)
        except ristorante.DoesNotExist:
            return JsonResponse({'error': f'ristorante "{nome_di_ristorante}" not found'}, status=404)
    else:
        return HttpResponseNotAllowed(['DELETE'])

def aggiornare_un_ristorante(request, nome_di_ristorante):
    if request.method == 'PUT':
        try:
            ristorante_object = ristorante.objects.get(nome=nome_di_ristorante)
        except ristorante.DoesNotExist:
            return JsonResponse({'error': f'ristorante "{nome_di_ristorante}" not found'}, status=404)
        dati = JSONParser().parse(request)
        nome_nuovo = dati.get('nome', '')
        indirizzo_nuovo = dati.get('indirizzo', '')
        if not nome_nuovo:
            return JsonResponse({'error': 'New name is required'}, status=400)
        ristorante_object.nome = nome_nuovo
        ristorante_object.indirizzo = indirizzo_nuovo
        ristorante_object.save()
        return JsonResponse({'message': f'ristorante "{nome_di_ristorante}" updated successfully', 'nome_nuovo': nome_nuovo, 'indirizzo_nuovo': indirizzo_nuovo}, status=200)
    else:
        return HttpResponseNotAllowed(['PUT'])

def ristoranti_tutti(request):
    ristoranti = ristorante.objects.all()
    dati = list(ristoranti.values())
    return JsonResponse(dati, safe=False)

def ristoranti_per_ricetta(request, nome_di_ricetta):
    ristoranti = ristorante.objects.filter(ricetta__nome = nome_di_ricetta)
    dati = list(ristoranti.values())
    return JsonResponse(dati, safe=False)

######################  Ricette  ######################

def creare_una_ricetta(request):
    if request.method == 'POST':
        dati = JSONParser().parse(request)

        # replace names by ids for the related ristoranti and ingredienti in the ricetta payload
        # this is done because they are saved in the database using their ids.
        ingredienti = list(ingrediente.objects.filter(nome__in=dati['ingrediente']).values())
        ingredienti_ids = [ingrediente['id'] for ingrediente in ingredienti]
        ristoranti = list(ristorante.objects.filter(nome__in=dati['ristorante']).values())
        ristoranti_ids = [ristorante['id'] for ristorante in ristoranti]
        dati['ristorante'] = ristoranti_ids
        dati['ingrediente'] = ingredienti_ids

        serializer = ricettaSerializer(data=dati)       
        if serializer.is_valid():
            if dati['ristorante'] and dati['ingrediente']:     
                ricetta = serializer.save()
                return JsonResponse({'success': True, 'id': ricetta.id}, status=201)
        return JsonResponse({'success': False, 'errors': serializer.errors}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])

def eliminare_una_ricetta(request, nome_di_ricetta):
    if request.method == 'DELETE':
        try:
            ricetta_object = ricetta.objects.get(nome=nome_di_ricetta)
            ricetta_object.delete()
            return JsonResponse({'message': f'ricetta "{nome_di_ricetta}" deleted successfully'}, status=204)
        except ricetta.DoesNotExist:
            return JsonResponse({'error': f'ricetta "{nome_di_ricetta}" not found'}, status=404)
    else:
        return HttpResponseNotAllowed(['DELETE'])

def aggiornare_una_ricetta(request, nome_di_ricetta):
    if request.method == 'PUT':
        try:
            ricetta_object = ricetta.objects.get(nome=nome_di_ricetta)
        except ricetta.DoesNotExist:
            return JsonResponse({'error': f'ricetta "{nome_di_ricetta}" not found'}, status=404)
        dati = JSONParser().parse(request)

        # separate ricetta payload fields to check whether empty or not
        nome_nuovo = dati.get('nome', '')
        ingredienti_nuovi = dati.get('ingrediente', '')
        ristoranti_nuovi = dati.get('ristorante', '')
        if not nome_nuovo or not ingredienti_nuovi or not ristoranti_nuovi:
            return JsonResponse({'error': 'Required fields must not be empty'}, status=400)
        
        # replace names by ids for the related ristoranti and ingredienti in the ricetta payload
        # this is done because they are saved in the database using their ids.
        ingredienti_nuovi = list(ingrediente.objects.filter(nome__in=ingredienti_nuovi).values())
        ingredienti_nuovi_ids = [ingrediente['id'] for ingrediente in ingredienti_nuovi]
        ristoranti_nuovi = list(ristorante.objects.filter(nome__in=ristoranti_nuovi).values())
        ristoranti_nuovi_ids = [ristorante['id'] for ristorante in ristoranti_nuovi]
        if not ingredienti_nuovi_ids or not ristoranti_nuovi_ids:
            return JsonResponse({'error': 'Names of ingredenti and ricette must be correct'}, status=400)

        ricetta_object.nome = nome_nuovo
        ricetta_object.ristorante.set(ristoranti_nuovi_ids)
        ricetta_object.ingrediente.set(ingredienti_nuovi_ids)
        ricetta_object.save()
        return JsonResponse({'message': f'ricetta "{nome_di_ricetta}" updated successfully', 'nome_nuovo': nome_nuovo, 'ristoranti_nuovi': ristoranti_nuovi_ids, 'ingredienti_nuovi': ingredienti_nuovi_ids}, status=200)
    else:
        return HttpResponseNotAllowed(['PUT'])

def ricette_tutte(request):
    ricette = ricetta.objects.all()
    dati = list(ricette.values())
    return JsonResponse(dati, safe=False)

def ricette_per_ristorante(request, nome_di_ristorante):
    ricette = ricetta.objects.filter(ristorante__nome = nome_di_ristorante)
    dati = list(ricette.values())
    return JsonResponse(dati, safe=False)

def ricette_per_ingrediente(request, nome_di_ingrediente):
    ricette = ricetta.objects.filter(ingrediente__nome = nome_di_ingrediente)
    dati = list(ricette.values())
    return JsonResponse(dati, safe=False)


######################  Ingrediente  ######################

def creare_un_ingrediente(request):
    if request.method == 'POST':
        dati = JSONParser().parse(request)
        serializer = ingredienteSerializer(data=dati)
        if serializer.is_valid():
            ingrediente = serializer.save()
            return JsonResponse({'success': True, 'id': ingrediente.id}, status=201)
        return JsonResponse({'success': False, 'errors': serializer.errors}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])

def eliminare_un_ingrediente(request, nome_di_ingrediente):
    if request.method == 'DELETE':
        try:
            ingrediente_object = ingrediente.objects.get(nome=nome_di_ingrediente)
            ingrediente_object.delete()
            return JsonResponse({'message': f'ricetta "{nome_di_ingrediente}" deleted successfully'}, status=204)
        except ricetta.DoesNotExist:
            return JsonResponse({'error': f'ricetta "{nome_di_ingrediente}" not found'}, status=404)
    else:
        return HttpResponseNotAllowed(['DELETE'])

def aggiornare_un_ingrediente(request, nome_di_ingrediente):
    if request.method == 'PUT':
        try:
            ingrediente_object = ingrediente.objects.get(nome=nome_di_ingrediente)
        except ingrediente.DoesNotExist:
            return JsonResponse({'error': f'ingrediente "{nome_di_ingrediente}" not found'}, status=404)
        dati = JSONParser().parse(request)
        nome_nuovo = dati.get('nome', '')
        if not nome_nuovo:
            return JsonResponse({'error': 'New name is required'}, status=400)
        ingrediente_object.nome = nome_nuovo
        ingrediente_object.save()
        return JsonResponse({'message': f'ingrediente "{nome_di_ingrediente}" updated successfully', 'nome_nuovo': nome_nuovo}, status=200)
    else:
        return HttpResponseNotAllowed(['PUT'])

def ingredienti_tutti(request):
    ingredienti = ingrediente.objects.all()
    dati = list(ingredienti.values())
    return JsonResponse(dati, safe=False)

def ingredienti_per_ricetta(request, nome_di_ricetta):
    ingredienti = ingrediente.objects.filter(ricetta__nome = nome_di_ricetta)
    dati = list(ingredienti.values())
    return JsonResponse(dati, safe=False)

def ingredienti_per_ristorante(request, nome_di_ristorante):
    ricette = ricetta.objects.filter(ristorante__nome = nome_di_ristorante)
    ingredienti = ingrediente.objects.filter(ricetta__in = ricette).distinct()
    dati = list(ingredienti.values())
    return JsonResponse(dati, safe=False)



