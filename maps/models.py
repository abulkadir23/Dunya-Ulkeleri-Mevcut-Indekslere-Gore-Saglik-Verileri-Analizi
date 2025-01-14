from django.db import models

class CountryData(models.Model):
    country = models.CharField(max_length=255)
    life_expectancy = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    happiness_level = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cost_of_living = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    purchasing_power = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    obesity_level = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    annual_work_hours = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        db_table = 'son_veriler2'
        managed = False

    def __str__(self):
        return self.country 