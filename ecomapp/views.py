from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, FormView
from django.contrib.auth import authenticate, login,logout
from rest_framework.response import Response

from .forms import *
from .models import *
from rest_framework.views import APIView

from rest_framework import viewsets, status
from .models import Product
from .serializers import ProductSerializer

class ProductList(APIView):
    serializer_class = ProductSerializer
    # queryset = Product.objects.all()

    def get(self,request, format=None):
        articles = Product.objects.all()
        serializer = ProductSerializer(articles, many=True)
        return Response({"articles": serializer.data})

    def post(self, request):
        """ """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,pk=None):
        """Updating one object"""
        return Response({'method':'put'})

    def patch(self,request, pk=None):
        return Response({"method":'patch'})

    def delete(self, request, pk=None):
        return Response({'method':'delete'})




"""Вывод главной страницы"""
class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myname']='Eldiiar'
        context['product_list'] = Product.objects.all()
        return context

"""Вывод всех продуктов"""
class AllProductsView(TemplateView):
    template_name = 'allproducts.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context


"""Детальный просмотр продукта"""
class ProductDetailView(TemplateView):
    template_name = 'productdetail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug=self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count+=1
        product.save()
        context['product'] = product
        return context


"""Добавить в  карзину"""
class AddToCartView(TemplateView):
    template_name = 'addtocart.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # взять id продукта из request url
        product_id = self.kwargs['pro_id']
        # взять продукт
        product_obj=Product.objects.get(id=product_id)
# проверить имеется ли корзина
        cart_id=self.request.session.get('cart_id',None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
            # продукт имеется в карзинке
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity+=1
                cartproduct.subtotal+=product_obj.selling_price
                cartproduct.save()
                cart_obj.total+=product_obj.selling_price
                cart_obj.save()
                # новый продукт добавлен в карзину
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj,product=product_obj,rate=product_obj.selling_price,
                                                         quantity=1,subtotal=product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.selling_price,
                                                     quantity=1, subtotal=product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
            #проверь есть ли продукт в корзине

            return context


"""Просмотр карзины"""
class MyCartView(TemplateView):
    template_name = 'mycart.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id=self.request.session.get('cart_id',None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart=None

        context['cart']=cart
        return context


"""Изменить карзину"""
class ManageCartView(View):
    def get(self,requests,*args,**kwargs):
        cp_id=self.kwargs['cp_id']
        action = requests.GET.get('action')
        cp_obj=CartProduct.objects.get(id=cp_id)
        cart_obj=cp_obj.cart

        if action == 'inc':
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == 'dcr':
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == 'rmv':
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass

        return redirect("ecomapp:mycart")


"""Заказать товары в карзине"""
class CheckoutView(CreateView):
    template_name = 'checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy("ecomapp:home")

    def dispatch(self, request, *args, **kwargs):
        user=request.user
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super(CheckoutView, self).dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart=cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Заказ получен"
            del self.request.session['cart_id']
        else:
            return redirect('ecomapp:home')
        return super(CheckoutView, self).form_valid(form)


"""Регистрация спользователя"""
class CustomerRegistrationView(CreateView):
    template_name = 'customerregistration.html'
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("ecomapp:home")
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user=User.objects.create_user(username,email,password)
        form.instance.user = user
        login(self.request,user)
        return super().form_valid(form)


"""Выход из системы пользователя"""
class CustomerLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('ecomapp:home')


"""Вход в систему пользователя"""
class CustomerLoginView(FormView):
    template_name = 'customerlogin.html'
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomapp:home")

    def form_valid(self, form):
        uname=form.cleaned_data.get('username')
        pword = form.cleaned_data['password']
        usr = authenticate(username=uname, password =pword)
        if usr is not None and usr.customer:
            login(self.request, usr)
        else:
            return render(self.request, self.template_name,{'form':self.form_class,
                                                            'error':"Введите правильные данные"})

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url= self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'