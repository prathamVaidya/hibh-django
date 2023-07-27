from rest_framework import serializers
from .models import Tracker, Alert

class TrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracker
        fields =  '__all__'
        extra_kwargs = {
                            'email_token': {'write_only': True}
                        }


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields =  '__all__'