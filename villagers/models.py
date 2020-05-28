from django.db import models

# Create your models here.
from django.urls import reverse


class Villager(models.Model):

    # personal information
    name = models.CharField(max_length=50, blank=False, null=False)
    sex_option = (
        (None, ''),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    sex = models.CharField(
        max_length=10,
        choices=sex_option,
        blank=False,
        default='',
        help_text='লিঙ্গ',
    )
    bari = models.ForeignKey('Bari', on_delete=models.SET_DEFAULT, default=None)
    # family information
    father = models.ForeignKey('self', on_delete=models.SET_DEFAULT, default=None, blank=True, null=True,
                               related_name='father_name')
    mother = models.ForeignKey('self', on_delete=models.SET_DEFAULT, default=None, blank=True, null=True,
                               related_name="mother_name")
    grand_father = models.ForeignKey('self', on_delete=models.SET_DEFAULT, default=None, blank=True, null=True,
                                     related_name='grand_father_name')
    grand_mother = models.ForeignKey('self', on_delete=models.SET_DEFAULT, default=None, blank=True, null=True,
                                     related_name="grand_mother_name")

    highest_education = models.CharField(max_length=20, blank=True, null=True)
    highest_education_institute = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True, help_text='পেশা')
    marital_status_option = (
        (None, ''),
        ('Married', 'Married'),
        ('Unmarried', 'Unmarried'),
    )
    marital_status = models.CharField(
        max_length=10,
        choices=marital_status_option,
        blank=False,
        default='',
        help_text='বিবাহিত',
    )
    spouse = models.ForeignKey('self', on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)

    lives_in_villager_option = (
        (None, ''),
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    lives_in_village = models.CharField(
        max_length=10,
        choices=lives_in_villager_option,
        blank=False,
        default='',
        help_text='বর্তমানে গ্রামে থাকেন?',
    )
    alive_option = (
        (None, ''),
        ('Alive', 'Alive'),
        ('Dead', 'Dead'),
    )
    alive = models.CharField(
        max_length=10,
        choices=alive_option,
        blank=False,
        default='',
        help_text='জীবিত আছেন?',
    )


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this villager."""
        return reverse('villager-details', args=[str(self.id)])


class Bari(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name

