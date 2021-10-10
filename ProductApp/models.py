from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
from django.utils.safestring import mark_safe


class Category(MPTTModel):
    status = (
        ('Available', 'Available'),
        ('Not available', 'Not available'),
    )

    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    title = models.CharField(max_length=100)
    image = models.ImageField(blank=True, upload_to='category/')
    status = models.CharField(max_length=20, choices=status)
    slug = models.SlugField(null=True, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.image.url))
    image_tag.short_description = 'Image'


class Product(models.Model):
    status = (
        ('Available', 'Available'),
        ('Not available', 'Not available'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    image = models.ImageField(blank=True, upload_to='product/')
    new_price = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    old_price = models.DecimalField(decimal_places=2, max_digits=15)
    quantity = models.IntegerField(default=0)
    min_quantity = models.IntegerField(default=3)
    descriptions = models.TextField()
    status = models.CharField(max_length=20, choices=status)
    slug = models.SlugField(null=True, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.image.url))
    image_tag.short_description = 'Image'

    def imageurl(self):
        if self.image:
            return self.image.url
        else:
            return ''

    # def get_absolute_url(self):
    #     return reverse("product_element", kwargs={"slug": self.slug})


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(blank=True, upload_to='product/')

    def __str(self):
        return self.title
