from rest_framework import serializers
from .models import ristorante, ricetta, ingrediente

class ristoranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ristorante
        fields = '__all__'

class ricettaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ricetta
        fields = '__all__'

class ingredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ingrediente
        fields = '__all__'