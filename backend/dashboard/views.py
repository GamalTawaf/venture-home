
import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from .models import Venture
from .factories import VentureFactory
# Create your views here.
def dashboard_view(request):
    return JsonResponse({'message': 'Welcome to the dashboard!'})

@require_GET
def venture_list(request):
    all_ventures = Venture.objects.all()
    return JsonResponse({'ventures': list(all_ventures.values())})

@require_POST
def save_venture(request):
    data = json.loads(request.body)
    venture = Venture.objects.create(
        name=data['name'],
        pod=data['pod'],
        stage=data['stage'],
        founder=data['founder'],
        metrics=data['metrics'],
        status=data['status'],
        last_update=data['last_update']
    )
    return JsonResponse({'id': venture.id, 'message': 'Venture saved successfully!'})


@require_POST
def generate_random_venture(request):
    count = int(request.GET.get('count', 20))
    VentureFactory.create_batch(count)
    return JsonResponse({'message': f'{count} random ventures generated successfully!'})