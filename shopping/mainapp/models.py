from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

User = get_user_model()


def  get_product_url(obj, viewname):
    ct_model = obj.__class__.meta.model_name
    return reverse(viewname, kwargs= {'ct_model': ct_model, 'slug':obj.slug})



class LatestProductsManager:

    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get("with_respect_too")
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_models in ct_models:
            model_product = ct_models.model_class()._base_manager.all().order_by("id")[:5]
            products.extend(model_product)
        if with_respect_to:
            ct_models = ContentType.objects.filter(models= with_respect_to)
            if ct_models.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key= lambda x: x.__class__._meta.model_name.startswith(with_respect_to),reverse= True
                    )
        return products


class LatestProducts:

    objects = LatestProductsManager()

class Category(models.Model):

    name = models.CharField(max_length= 255, verbose_name="Имя категории")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name="Категория",on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Изображение")
    description = models.TextField(verbose_name="Описание", null=True)
    price = models.DecimalField(max_digits= 9, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.title


class CartProduct(models.Model):

    user = models.ForeignKey("Customer", verbose_name="Покупатель", on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", verbose_name="Корзина", on_delete=models.CASCADE, related_name="related_products")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    qty = models.PositiveIntegerField(default= 1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая цена")

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.product.title)


class Cart(models.Model):

    owner = models.ForeignKey("Customer", verbose_name="Владелец", on_delete=models.CASCADE)
    product = models.ManyToManyField(CartProduct, blank=True, related_name="related_cart")
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits= 9, decimal_places=2, verbose_name="Общая цена")

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    address = models.CharField(max_length=255, verbose_name="Адрес")

    def __str__(self):
        return "Покупатель : {} {}".format(self.user.first_name, self.user.last_name)


class Charach(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255, verbose_name="Имя товара для характеристики")

    def __str__(self):
        return "Характеристики для товара: {}".format(self.name)


class Sketch(Product):

    oblzh = models.CharField(max_length=255, verbose_name="Переплет")
    tip = models.CharField(max_length=255, verbose_name="Вид")
    list = models.CharField(max_length=255, verbose_name="Кол-во листов")

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Book(Product):

    oblzh = models.CharField(max_length=255, verbose_name="Переплет")
    author = models.CharField(max_length=255, verbose_name="Автор")
    str = models.CharField(max_length=255, verbose_name="Кол-во страниц")
    imj = models.CharField(max_length=255, verbose_name="Наличие картинок")
    zhanr = models.CharField(max_length=255, verbose_name="Жанр книги")


    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Pen(Product):

    clr = models.CharField(max_length=255, verbose_name="Цвет")
    tolsh = models.CharField(max_length=255, verbose_name="Толщина")
    tip = models.CharField(max_length=255, verbose_name="Тип ручки")

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


