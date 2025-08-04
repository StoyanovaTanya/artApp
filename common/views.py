from django.contrib import messages
from django.views.generic import TemplateView
from artwork.models import Artwork



class HomeView(TemplateView):
    template_name = 'common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_artworks'] = Artwork.objects.order_by('-id')[:6]
        return context

def my_view(request):
    messages.success(request, 'Successfully done!')
    messages.error(request, 'Something went wrong.')
