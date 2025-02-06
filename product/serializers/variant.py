from rest_framework import serializers
from product.models import ProductVariant, Attribute, AttributeValue


class AttributeValueSerializer(serializers.ModelSerializer):
    """Serializer for Attribute Values"""

    class Meta:
        model = AttributeValue
        fields = ['id', 'attribute', 'value']


class AttributeSerializer(serializers.ModelSerializer):
    """Serializer for Attributes"""

    values = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = ['id', 'name', 'values']



class ProductVariantSerializer(serializers.ModelSerializer):
    """Serializer for Product Variants"""
    
    attributes = AttributeValueSerializer(many=True, read_only=True)
    attribute_ids = serializers.ListField(write_only=True, child=serializers.IntegerField())

    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'attributes', 'attribute_ids']

    def create(self, validated_data):
        attribute_ids = validated_data.pop('attribute_ids', [])
        variant = ProductVariant.objects.create(**validated_data)
        variant.attributes.set(AttributeValue.objects.filter(id__in=attribute_ids))
        return variant

    def update(self, instance, validated_data):
        attribute_ids = validated_data.pop('attribute_ids', None)
        if attribute_ids is not None:
            instance.attributes.set(AttributeValue.objects.filter(id__in=attribute_ids))
        return super().update(instance, validated_data)