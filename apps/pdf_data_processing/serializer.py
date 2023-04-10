from rest_framework import serializers

from . import services


class TaxFilingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    identificador = serializers.CharField()
    tax_filing = serializers.CharField()
    wages = serializers.IntegerField()
    total_deductions = serializers.IntegerField()

    
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return services.TaxFilingDataClass(**data)
