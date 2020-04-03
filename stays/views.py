from django.views.generic import ListView, DetailView
from django.http import Http404

from .models import Stay


class StayListView(ListView):
    """Product List View"""
    queryset = Stay.objects.all()
    template_name = 'stays/list.html'

    def get_context_data(self, *args, **kwargs):
        """Method for getting context data"""
        context = super(StayListView, self)\
            .get_context_data(*args, **kwargs)
        # cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        # context['cart'] = cart_obj
        return context


class StayDetailView(DetailView):
    """Stay Detil View"""
    template_name = 'stays/detail.html'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        instance = Stay.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance
