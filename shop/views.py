from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Category, Product


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "shop/product/list.html"
    context_object_name = "products"
    paginate_by = 5

    def get_queryset(self):
        return Product.objects.filter(available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        category_slug = self.kwargs.get("category_slug")
        category = None
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            context["products"] = self.get_queryset().filter(category=category)
        context["category"] = category
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "shop/product/detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = get_object_or_404(
            Product,
            slug=self.kwargs.get("slug"),
            id=self.kwargs.get("id"),
            available=True,
        )
        return context
