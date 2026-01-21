import factory
from .models import Venture
from faker import Faker

fake = Faker()

class VentureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Venture

    name = factory.LazyAttribute(lambda x: fake.company())
    pod = factory.LazyAttribute(lambda x: fake.bs())
    stage = factory.LazyAttribute(lambda x: fake.random_element(elements=('Ideation', 'Pilot', 'Growth', 'Scale')))
    founder = factory.LazyAttribute(lambda x: fake.name())
    metrics = factory.LazyAttribute(lambda x: {
        'burn_rate_monthly': fake.random_int(min=10000, max=100000),
        'runway_months': fake.random_int(min=1, max=24),
        'pilot_customers': fake.random_int(min=0, max=10),
        'nps_score': fake.random_int(min=0, max=100)
    })
    status = factory.LazyAttribute(lambda x: fake.random_element(elements=('on_track', 'at_risk', 'off_track')))
    last_update = factory.LazyAttribute(lambda x: fake.date_this_year())