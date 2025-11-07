from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from coupons.forms import CouponApplyForm
from shop.models import Product
from shop.recommender import Recommender
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


class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = "cart/detail.html"

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        for item in cart:
            item["update_quantity_form"] = CartAddProductForm(
                initial={"quantity": item["quantity"], "override": True}
            )
        coupon_apply_form = CouponApplyForm()

        r = Recommender()
        cart_products = [item["product"] for item in cart]
        if cart_products:
            recommended_products = r.suggest_products_for(
                cart_products, max_results=4
            )
        else:
            recommended_products = []

        return render(
            request,
            self.template_name,
            {
                "cart": cart,
                "coupon_apply_form": coupon_apply_form,
                "recommended_products": recommended_products,
            },
        )
