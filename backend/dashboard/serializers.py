from rest_framework import serializers
from .models import Venture


class VentureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venture
        fields = "__all__"


class VentureMetricsSerializer(serializers.Serializer):
    total_ventures = serializers.IntegerField()
    active_ventures = serializers.IntegerField()
    total_burn_rate = serializers.IntegerField()
    avg_runway = serializers.IntegerField()
