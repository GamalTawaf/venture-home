from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter
from .models import Venture
from .serializers import VentureSerializer, VentureMetricsSerializer
from .factories import VentureFactory
from integrations.chat import ask_venture_question


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # default
    page_size_query_param = 'page_size'
    max_page_size = 10000  # or whatever upper limit you want
# define filters for Venture model
class VentureFilter(FilterSet):
    pod = CharFilter(field_name="pod", lookup_expr="icontains")
    stage = CharFilter(field_name="stage", lookup_expr="icontains")
    status = CharFilter(field_name="status", lookup_expr="icontains")

    class Meta:
        model = Venture
        fields = ["pod", "stage", "status"]


# define the VentureViewSet which django reset framework handles CRUD operations and custom actions for Venture model
class VentureViewSet(viewsets.ModelViewSet):
    queryset = Venture.objects.all()
    serializer_class = VentureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VentureFilter
    pagination_class = CustomPageNumberPagination
    search_fields = ["name", "pod", "stage", "status"]
    ordering_fields = ["name", "pod", "stage", "status", "last_update"]
    ordering = ["-last_update"]

    @action(detail=False, methods=["get"])
    def metrics(self, request):
        """Get dashboard metrics"""
        ventures = self.get_queryset()
        total_ventures = ventures.count()
        active_ventures = ventures.filter(status__iexact="active").count()

        total_burn_rate = sum(
            venture.metrics.get("burn_rate_monthly", 0)
            for venture in ventures
            if venture.metrics
        )

        runways = [
            venture.metrics.get("runway_months", 0)
            for venture in ventures
            if venture.metrics and venture.metrics.get("runway_months", 0) > 0
        ]
        avg_runway = round(sum(runways) / len(runways)) if runways else 0

        metrics_data = {
            "total_ventures": total_ventures,
            "active_ventures": active_ventures,
            "total_burn_rate": total_burn_rate,
            "avg_runway": avg_runway,
        }

        serializer = VentureMetricsSerializer(metrics_data)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def generate_random(self, request):
        """Generate random ventures for testing"""
        count = request.data.get("count", 20)
        VentureFactory.create_batch(int(count))
        return Response(
            {"message": f"{count} random ventures generated successfully!"},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"])
    def chat(self, request):
        """AI-powered chat about ventures using LangChain and Gemini"""
        question = request.data.get("question", "").strip()

        if not question:
            return Response(
                {"error": "Question is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            ventures = self.get_queryset()
            venture_data = []
            for venture in ventures:
                venture_info = {
                    "id": venture.id,
                    "name": venture.name,
                    "pod": venture.pod,
                    "stage": venture.stage,
                    "founder": venture.founder,
                    "status": venture.status,
                    "last_update": (
                        venture.last_update.isoformat() if venture.last_update else None
                    ),
                    "metrics": venture.metrics or {},
                }
                venture_data.append(venture_info)

            answer = ask_venture_question(question, venture_data)

            return Response(
                {
                    "question": question,
                    "answer": answer,
                    "ventures_analyzed": len(venture_data),
                }
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to process chat request: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
