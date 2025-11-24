from rest_framework import serializers
from posicoes.models import BJJPos


class BJJPosSerializer(serializers.ModelSerializer):
    class Meta:
        model = BJJPos
        fields = "__all__"
