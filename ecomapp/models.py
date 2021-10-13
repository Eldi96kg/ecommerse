from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    full_name = models.CharField(max_length=200, verbose_name='Полное имя')
    address = models.CharField(max_length=200,null=True, blank=True, verbose_name='Адрес')
    joined_on = models.DateTimeField(auto_now_add=True,verbose_name='')

    def __str__(self):
        return self.full_name


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200,verbose_name='Название')
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория' )
    image = models.ImageField(upload_to='products',verbose_name='Картинка')
    marked_price = models.PositiveIntegerField(verbose_name='Рыночная цена')
    selling_price = models.PositiveIntegerField(verbose_name='Цена для вас')
    description = models.TextField(verbose_name='Описание')
    warranty = models.CharField(max_length=300,null=True,blank=True,default='Нет', verbose_name='Гарантия')
    return_policy = models.CharField(max_length=300,null=True,blank=True,default='Нет возврата',verbose_name='Политика возврата')
    view_count = models.PositiveIntegerField(default=0,verbose_name='Просмотрено')

    class Meta:
        ordering=['-id']

    def __str__(self):
        return self.title


class Cart(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True,verbose_name='Клиент')
    total = models.PositiveIntegerField(default=0,verbose_name='Всего к оплате')
    created_at= models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')

    def __str__(self):
        return 'Cart' +str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Карзина')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='Продукт')
    rate = models.PositiveIntegerField(verbose_name='Оценка')
    quantity = models.PositiveIntegerField(verbose_name='Кол-во')
    subtotal = models.PositiveIntegerField(verbose_name='Сумма')

    def __str__(self):
        return 'Cart:' + str(self.cart.id) + "CartProduct:" + str(self.id)


ORDER_STATUS=(
    ('Order Received',"Order Received"),
    ('Order Processing','Order Processing'),
    ('On the way', 'On the way'),
    ('Order Completed', 'Order Completed'),
    ('Order Canceled', 'Order Canceled'),
)


class Order(models.Model):
    cart=models.OneToOneField(Cart,on_delete=models.CASCADE,verbose_name='Корзина')
    ordered_by=models.CharField(max_length=200,verbose_name='Заказчик', )
    shipping_address=models.CharField(max_length=200, verbose_name='Адрес заказчика')
    mobile=models.CharField(max_length=50,verbose_name="Мобильный телефон")
    email = models.EmailField(null=True, blank=True,verbose_name="Email адрес")
    subtotal=models.PositiveIntegerField()
    discount=models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50,choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order:"+str(self.id)
















