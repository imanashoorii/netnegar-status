import traceback

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status, generics
from datetime import datetime, timedelta
from math import ceil
from .models import Incident, ErrorLog
from .serializers import IncidentSerializer, IncidentListSerializer, HealthDetailSerializer, StatusBarSerializer, \
    ChartSerializerData
from .pagination import LargeResultsSetPagination
from netnegar.models import HealthDetail
from .enum import ServiceList, Zones
from .utils import convertIntervalToPersian
from .iranMonthRange import fromDate_toDate


class CreateIncident(generics.CreateAPIView):
    permission_classes = (
        IsAuthenticated,
        IsAdminUser
    )

    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "با موفقیت ساخته شد", "data": serializer.data}, status=status.HTTP_201_CREATED,
                        headers=headers)


class ListIncident(generics.ListAPIView):
    queryset = Incident.objects.filter(deletedAt__exists=False).order_by('-createdAt')
    serializer_class = IncidentListSerializer
    pagination_class = LargeResultsSetPagination


class OngoingIncident(generics.ListAPIView):
    queryset = Incident.objects.filter(deletedAt__exists=False, to_date__gte=datetime.now()).order_by('-createdAt')
    serializer_class = IncidentListSerializer
    pagination_class = LargeResultsSetPagination


class DeleteIncident(generics.DestroyAPIView):
    queryset = Incident.objects.order_by('-createdAt')
    serializer_class = IncidentListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = "id"


class UpdateIncident(generics.UpdateAPIView):
    queryset = Incident.objects.order_by('-createdAt')
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class HealthChart(GenericAPIView):

    def post(self, request):
        serializer = HealthDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            pipeline = [
                {
                    "$match": {}
                },
            ]

            if serializer.validated_data.get("zone") == 0:
                pipeline[0]["$match"]['zone'] = {"$in": [
                    Zones.IRAN_AFRANET,
                    Zones.IRAN_ASIATECH,
                    Zones.IRAN_MOBINNET,
                    Zones.IRAN_ZIRSAKHT,
                    Zones.IRAN_PARSONLINE,
                    Zones.IRAN_SOROUSH_RASANEH
                ]}
            if serializer.validated_data.get("zone") == 1:
                pipeline[0]["$match"]['zone'] = {"$in": [
                    Zones.GERMANY_DIGITAL_OCEAN,
                    Zones.NETHERLANDS_DIGITAL_OCEAN,
                    Zones.USA_DIGITAL_OCEAN,
                ]}

            interval = serializer.validated_data.get("interval")
            service = serializer.validated_data.get("service")
            fromDate, toDate = fromDate_toDate()

            if service == "API":
                pipeline[0]['$match']['monitor'] = {"$in": [ServiceList.MYSQL, ServiceList.MONGODB]}
            if service == "panel":
                pipeline[0]['$match']['monitor'] = service

            if interval == "daily":
                deltaTime = datetime.now() - timedelta(1)
                pipeline[0]["$match"]['time'] = {"$gte": deltaTime.replace(hour=0, minute=0, second=0),
                                                 "$lte": datetime.now()}
                pipeline.append(
                    {
                        "$group": {
                            "_id": "$time",
                            "value": {"$avg": "$value"},
                        }
                    }
                )
                pipeline.append(
                    {
                        "$addFields": {
                            "date": "$_id",
                            "hour": {"$hour": "$_id"},
                            "percentile": {"$ceil": "$value"},
                            "interval": convertIntervalToPersian(interval),
                        }
                    },
                )
                pipeline.append({'$sort': {'date': 1}})
            elif interval == "weekly":
                deltaTime = datetime.now() - timedelta(7)
                pipeline[0]["$match"]['time'] = {"$gte": deltaTime.replace(hour=0, minute=0, second=0),
                                                 "$lte": datetime.now()}
                pipeline.append(
                    {
                        "$group": {
                            "_id": {"$dateToString": {"format": '%Y-%m-%d', "date": '$time'}},
                            "value": {"$avg": "$value"},
                        }
                    }
                )
                pipeline.append(
                    {
                        "$addFields": {
                            "date": "$_id",
                            "percentile": {"$ceil": "$value"},
                            "interval": convertIntervalToPersian(interval),
                        }
                    },
                )
            elif interval == "monthly":
                pipeline[0]["$match"]['time'] = {"$gte": fromDate,
                                                 "$lte": toDate}
                pipeline.append(
                    {
                        "$group": {
                            "_id": {"$dateToString": {"format": '%Y-%m-%d', "date": '$time'}},
                            "value": {"$avg": "$value"},
                        }
                    }
                )
                pipeline.append(
                    {
                        "$addFields": {
                            "date": "$_id",
                            "percentile": {"$ceil": "$value"},
                            "interval": convertIntervalToPersian(interval),
                        }
                    },
                )
            elif interval == "ninety":
                deltaTime = datetime.now() - timedelta(90)
                pipeline[0]["$match"]['time'] = {"$gte": deltaTime.replace(hour=0, minute=0, second=0),
                                                 "$lte": datetime.now()}
                pipeline.append(
                    {
                        "$group": {
                            "_id": {"$dateToString": {"format": '%Y-%m-%d', "date": '$time'}},
                            "value": {"$avg": "$value"},
                        }
                    }
                )
                pipeline.append(
                    {
                        "$addFields": {
                            "date": "$_id",
                            "percentile": {"$ceil": "$value"},
                            "interval": convertIntervalToPersian(interval),
                        }
                    },
                )

            pipeline.append(
                {'$sort': {'date': 1}}
            )

            items = list(HealthDetail.objects.aggregate(*pipeline))
            serializeItems = ChartSerializerData(data=items, many=True)
            if serializeItems.is_valid(raise_exception=True):
                return Response(serializeItems.data, status.HTTP_200_OK)


