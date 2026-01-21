from django.db import models

# Create your models here.
#{ example venture object
#   "id": "v-001",
#   "name": "PortFlow",
#   "pod": "Infrastructure Intelligence",
#   "stage": "Pilot",
#   "founder": "Dr. Samir Hassan",
#   "metrics": {
#     "burn_rate_monthly": 45000,
#     "runway_months": 14,
#     "pilot_customers": 3,
#     "nps_score": 72
#   },
#   "status": "on_track",
#   "last_update": "2025-01-18"
# }
class Venture(models.Model):
    name = models.CharField(max_length=100)
    pod = models.CharField(max_length=100)
    stage = models.CharField(max_length=50)
    founder = models.CharField(max_length=100)
    # should be a JSON field and contain burn_rate_monthly, runway_months, pilot_customers, nps_score
    metrics = models.JSONField(default=dict)
    status = models.CharField(max_length=50)
    last_update = models.DateField()

    def __str__(self):
        return self.name