import django_tables2 as tables
from django.utils.html import format_html

class ItemTable(tables.Table):
    name = tables.Column(verbose_name="Name")
    description = tables.Column(verbose_name="Description")
    type = tables.Column(verbose_name="Type")
    item_date = tables.Column(verbose_name="Date")
    current_location = tables.Column(verbose_name="Current Location")

    class Meta:
        attrs = {"class": "table table-striped table-bordered"}  # Add Bootstrap classes