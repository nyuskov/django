from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView

from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


class CartAddView(LoginRequiredMixin, View):
    def post(self, request, product_id, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(
                product=product,
                quantity=cd["quantity"],
                override_quantity=cd["override"],
            )
        return redirect("cart:cart_detail")


class CartRemoveView(LoginRequiredMixin, View):
    def post(self, request, product_id, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect("cart:cart_detail")


class CartDetailView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = "cart/detail.html"
    context_object_name = "cart"
