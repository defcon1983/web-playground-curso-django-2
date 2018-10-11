from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import Page
from .forms import PageForm

# existen otras funciones decoradoras como login_required y permission_required

class StaffRequiredMixin(object):
    @method_decorator(staff_member_required) #con esto se ahorra el if comentado
    def dispatch(self, request, *args, **kwargs):
        # if not request.user.is_staff:
            # return redirect( reverse_lazy('admin:login') )

        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs) 

class PageListView(ListView):
	model = Page

class PageDetailView(DetailView):
	model = Page

# Con esto se ahorra el mixin
@method_decorator(staff_member_required, name='dispatch')
class PageCreate(CreateView):
    model = Page
    # fields = ['title', 'content', 'order']
    form_class = PageForm
    success_url = reverse_lazy('pages:pages')

class PageUpdate(StaffRequiredMixin, UpdateView):
    model = Page
    # fields = ['title', 'content', 'order']
    form_class = PageForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
    	return reverse_lazy('pages:update', args=[self.object.id]) + '?ok'

class PageDelete(StaffRequiredMixin, DeleteView):
    model = Page
    success_url = reverse_lazy('pages:pages')
