from django.db import models
from django.utils.text import slugify

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    cost_price = models.FloatField()
    selling_price = models.IntegerField()
    stocks = models.IntegerField()
    totalcp = models.FloatField()
    totalsp = models.IntegerField()
    assumed_profit = models.FloatField()
    left_amount = models.FloatField()
    exipry_date = models.DateField()
    added_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=300)
    
    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()

    # for sitemaps
    def get_absolute_url(self):
        return '/details/%s' %self.slug
    
class Cart(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    amount = models.IntegerField()

    def __str__(self):
        return self.product.name

class Transaction(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=None, null=True, blank=True)
    cart_id = models.IntegerField(default=None, null=True, blank=True)
    selling_price = models.IntegerField()
    profit_or_loss = models.FloatField()
    sold_on = models.DateField(auto_now_add=True)
    remark = models.CharField(max_length=10)
    total_amount = models.IntegerField()

    def __str__(self):
        return self.product.name