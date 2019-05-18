from django.db import models

# Create your models here.

class Product(models.Model):
	"""docstring for ClassName"""
	name = models.CharField(max_length=100)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	qty = models.IntegerField()
	desc = models.TextField()
	photo = models.FileField() 
	class Meta:
		db_table="product"

#def save(self, *args, **kwargs):
    #self.price = round(self.price,2)
    #super(Product, self).save(*args, **kwargs)
		