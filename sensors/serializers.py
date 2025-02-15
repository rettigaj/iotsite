#from django.utils.dateparse import parse_datetime
from rest_framework import serializers
from sensors.models import *


class SensorDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = SensorData
        fields = ['id', 'timestamp', 'relay_id', 'sensor_id',
                  'sensor_type', 'units', 'data', 'longitude', 'latitude',
                  'altitude', 'speed', 'climb']


class LoRaGatewaySerializer(serializers.ModelSerializer):

    class Meta:
        model = LoRaGateway
        fields = ['gtw_id', 'gtw_trusted', 'timestamp', 'time', 'channel',
                  'rssi', 'snr', 'rf_chain', 'latitude', 'longitude']


class LoRaGatewayMetadataSerializer(serializers.ModelSerializer):

    gateways = LoRaGatewaySerializer(many=True)

    class Meta:
        model = LoRaGatewayMetadata
        fields = ['time', 'frequency', 'modulation', 'data_rate', 'coding_rate', 'gateways']


class LoRaGatewayPayloadFieldsSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoRaGatewayPayloadFields
        fields = ['b', 'sm1', 'sm2', 'sm3', 'sm4', 't1', 't2']


class LoRaGatewayDataSerializer(serializers.ModelSerializer):

    payload_fields = LoRaGatewayPayloadFieldsSerializer(required=True)
    metadata = LoRaGatewayMetadataSerializer(required=True)

    class Meta:
        model = LoRaGatewayData
        fields = ['app_id', 'dev_id', 'hardware_serial', 'port', 'counter',
                  'payload_raw', 'payload_fields', 'metadata', 'downlink_url']

    def create(self, validated_data):
        payload_data = validated_data.pop('payload_fields')
        metadata_data = validated_data.pop('metadata')
        gateways_data = metadata_data.pop('gateways')

        instance = LoRaGatewayData.objects.create(**validated_data)
        LoRaGatewayPayloadFields.objects.create(gateway_data=instance, **payload_data)
        meta_instance = LoRaGatewayMetadata.objects.create(gateway_data=instance, **metadata_data)

        for gateway_data in gateways_data:
            LoRaGateway.objects.create(metadata=meta_instance, **gateway_data)

        return instance


class SensorIDListingField(serializers.StringRelatedField):
    def to_internal_value(self, value):
        sensor_id = FeatherSensorID.objects.create(sensor_id=value)
        return sensor_id

    def to_representation(self, value):
        return value.sensor_id


class SensorTemperatureListingField(serializers.StringRelatedField):
    def to_internal_value(self, value):
        temperature = FeatherSensorTemperature.objects.create(temperature=value)
        return temperature

    def to_representation(self, value):
        return value.temperature


class FeatherDataSerializer(serializers.ModelSerializer):

    SensorID = SensorIDListingField(many=True, required=False)
    Temperature = SensorTemperatureListingField(many=True, required=False)

    class Meta:
        model = FeatherData
        fields = ['TimeStamp', 'TimeFormat', 'Date', 'SensorID', 'Temperature',
                  'TempFormat', 'DeviceID', 'Location', 'Latitude', 'Longitude']


class FeatherMetadataV2Serializer(serializers.ModelSerializer):

    class Meta:
        model = FeatherMetadataV2
        fields = ['location', 'latitude', 'longitude', 'time']


class FeatherSensorDataV2Serializer(serializers.ModelSerializer):

    class Meta:
        model = FeatherSensorDataV2
        fields = ['sensor_id', 'sensor_type', 'sensor_data', 'sensor_units']


class FeatherDataV2Serializer(serializers.ModelSerializer):

    metadata = FeatherMetadataV2Serializer(required=True)
    data = FeatherSensorDataV2Serializer(many=True, required=False)

    class Meta:
        model = FeatherDataV2
        fields = ['dev_id', 'metadata', 'data']

    def create(self, validated_data):
        metadata_data = validated_data.pop('metadata')
        sensors_data = validated_data.pop('data')

        instance = FeatherDataV2.objects.create(**validated_data)
        FeatherMetadataV2.objects.create(feather_data=instance, **metadata_data)

        for sensor_data in sensors_data:
            FeatherSensorDataV2.objects.create(feather_data=instance, **sensor_data)

        return instance
