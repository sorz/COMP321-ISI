from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from .models import Category
from store.utils import make_page


class IndexView(TemplateView):
    template_name = 'category/index.html'

    def render_to_response(self, context, **response_kwargs):
        # Set current_app so that url() on template can render correctly.
        # https://docs.djangoproject.com/en/1.7/topics/http/urls/#topics-http-reversing-url-namespaces
        response_kwargs['current_app'] = self.request.resolver_match.namespace

        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Category.objects.all()
        context['categories'] = categories
        return context


class DetailView(TemplateView):
    template_name = 'category/detail.html'
    order_fields = ('price', '-price', 'average_rating', '-average_rating')

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['current_app'] = self.request.resolver_match.namespace
        return super().render_to_response(context, **response_kwargs)

    def get_queryset(self, category):
        return category.product_set.exclude(status='F')  # exclude off-shelf

    def get_context_data(self, category_id, **kwargs):
        context = super().get_context_data(**kwargs)

        category = get_object_or_404(Category, pk=category_id)
        name_filter = self.request.GET.get('filter', '')
        sort = self.request.GET.get('sort')

        products = self.get_queryset(category)
        if name_filter:
            products = products.filter(name__contains=name_filter)
        if sort in self.order_fields:
            products = products.order_by(sort)
        else:
            sort = ''

        context['category'] = category
        context['filter'] = name_filter
        context['sort'] = sort

        products = make_page(products, self.request.GET.get('page'))
        context['products'] = products

        return context
