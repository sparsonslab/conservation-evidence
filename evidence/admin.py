from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib import messages
from django.db.models import CharField

from evidence.models import Evidence

admin.site.site_header = "Conservation Evidence"
admin.site.index_title = "something something"
admin.site.site_url = "/evidence/index.html"


class EffectivenessFilter(SimpleListFilter):
    
    title = "effectiveness"
    parameter_name = "effect"
    
    def lookups(self, request, model_admin):
        return [(i, f"{i}+") for i in range(1, 5)]
    
    def queryset(self, request, queryset):
        print(self.value())
        if self.value() is None:
            return queryset
        return queryset.filter(effectiveness_score__gte=self.value())


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):

    # Show all columns.
    list_display = [field.name for field in Evidence._meta.fields if field.name != 'id']

    # Can search all char fields.
    search_fields = [field.name for field in Evidence._meta.fields if isinstance(field, CharField)]

    # Filter for effectiveness score.
    list_filter = [EffectivenessFilter]

    # Action to show average effectiveness by species group.
    actions = ["effectiveness_by_species"]

    def get_queryset(self, request):
        return Evidence.objects.all()

    @admin.action(description="Effectiveness by species group")
    def effectiveness_by_species(self, request, queryset):
        # For each species group, get the number of entries and
        # total effectiveness score.
        scores = {}
        for obj in queryset:
            group = obj.species_group
            if group not in scores:
                scores[group] = [0, 0]
            score = obj.effectiveness_score
            scores[group][0] += 1
            scores[group][1] += score

        # Simple message to show.
        message = "Mean effectiveness: "
        for group, (n, total) in scores.items():
            message += f"{group} = {total / n: .2f}, "
        messages.add_message(request, messages.INFO, message)
