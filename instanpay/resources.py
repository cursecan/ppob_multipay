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


class GroupResource(resources.ModelResource):
    class Meta:
        model = Group
        field = [
            'slug', 'group_name'
        ]
        export_order = [
            'slug', 'group_name'
        ]
        import_id_fields = ['slug']
        skip_unchanged = True
        report_skipped = False


class OperatorResource(resources.ModelResource):
    group = resources.Field(
        attribute='group', column_name='group',
        widget=ForeignKeyWidget(Group, 'slug')
    )

    class Meta:
        model = Operator
        fields = [
            'slug', 'operator_name',
            'grup'
        ]
        export_order = [
            'slug', 'operator_name',
            'grup'
        ]
        import_id_fields = ['slug']
        skip_unchanged = True
        report_skipped = False

