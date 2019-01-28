from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import (
    Product, Group, Operator
)

class ProductResource(resources.ModelResource):
    group = resources.Field(
        attribute='group', column_name='group',
        widget=ForeignKeyWidget(Group, 'slug')
    )
    operator = resources.Field(
        attribute='operator', column_name='operator',
        widget=ForeignKeyWidget(Operator, 'slug')
    )
    
    class Meta:
        model = Product
        fields = [
            'code', 'subtype', 'product_name',
            'group', 'operator',
            'nominal', 'price', 'commision'
        ]
        export_order = [
            'code', 'subtype', 'product_name',
            'group', 'operator',
            'nominal', 'price', 'commision'
        ]
        import_id_fields = ['code']
        skip_unchanged = True
        report_skipped = False

# subtype = models.CharField(max_length=1, choices=SUBTYPE_LIST, default=INSTAN)
# code = models.CharField(max_length=20, unique=True)
# product_name = models.CharField(max_length=200)
# group = models.ForeignKey(Group, on_delete=models.CASCADE)
# operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
# price = models.DecimalField(max_digits=12, decimal_places=2)
# commision = models.DecimalField(max_digits=12, decimal_places=2, default=0)
# nominal = models.PositiveIntegerField(default=0)
# extend_server = models.OneToOneField(ExtraServer, on_delete=models.CASCADE, blank=True, null=True)
# is_active = models.BooleanField(default=False)