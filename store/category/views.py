from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Category


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

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['current_app'] = self.request.resolver_match.namespace
        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, category_id, **kwargs):
        context = super().get_context_data(**kwargs)

        category = get_object_or_404(Category, pk=category_id)
        products = category.product_set.filter(off_shelf=False)
        context['category'] = category

        name_filter = self.request.GET.get('filter', '')
        if name_filter:
            products = products.filter(name__contains=name_filter)
        context['filter'] = name_filter

        sort = self.request.GET.get('sort')
        if sort in ('price', '-price', 'rating', '-rating'):
            products = products.order_by(sort)
        else:
            sort = ''
        context['sort'] = sort

        # Code of pagination is from
        # https://docs.djangoproject.com/en/1.7/topics/pagination/#using-paginator-in-a-view

        paginator = Paginator(products, 3)  # 3 products per page for testing

        page = self.request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            products = paginator.page(paginator.num_pages)
        context['products'] = products

        return context
