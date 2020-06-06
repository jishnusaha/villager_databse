from rest_framework import serializers
from .models import Villager


class VillagerSerializer(serializers.ModelSerializer):
    absolute_url = serializers.CharField(source='get_absolute_url')
    father_name = serializers.CharField(source='father')
    mother_name = serializers.CharField(source='mother')
    bari_name = serializers.CharField(source='bari')
    father_absolute_url = serializers.SerializerMethodField('get_father_absolute_url')
    mother_absolute_url = serializers.SerializerMethodField('get_mother_absolute_url')
    # new_field = serializers.CharField(source='father.get_absolute_url')
    # mother_absolute_url = serializers.CharField(source='get_father_absolute_url')
    class Meta:
        fields = ['name', 'absolute_url', 'father_absolute_url', 'father_name', 'mother_absolute_url', 'mother_name',
                  'bari_name', 'occupation', 'lives_in_village']
        model = Villager

    def get_father_absolute_url(self, object):

        villager = Villager.objects.get(pk=object.id)

        if villager.father:
            return villager.father.get_absolute_url()
        else:
            return None

    def get_mother_absolute_url(self, object):
        villager = Villager.objects.get(pk=object.id)

        if villager.mother:
            return villager.mother.get_absolute_url()
        else:
            return None




