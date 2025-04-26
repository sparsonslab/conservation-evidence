from django.contrib import admin

from evidence.models import Evidence

admin.site.site_header = "Conservation Evidence"
admin.site.index_title = "something something"
admin.site.site_url = "/evidence/index.html"


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):

    list_display = ["intervention_title"]

    def get_queryset(self, request):
        return Evidence.objects.all()
