from django.db import models
from django.db.models import Model, CharField, IntegerField

evidence_types = [
    (1, "Experimental"),
    (2, "Observational"),
    (3, "Review")
]


class Evidence(Model):

    intervention_title = CharField(max_length=1000)

    species_group = CharField(max_length=100)

    year = IntegerField()

    location = CharField(max_length=100)

    effectiveness_score = IntegerField()

    evidence_type = IntegerField(choices=evidence_types, default=1)

    brief_outcome = CharField(max_length=1000)

