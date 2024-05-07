from django.shortcuts import render
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from rest_framework import permissions, viewsets
from .serializers import VendorSerializer, POSerializer, HPSerializer, VendorPerformanceSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .functionality import check_po_status, update_quality_rating, update_fulfillment_rate, average_response_time
from datetime import datetime

@csrf_exempt
def vendor_list(request):
    if request.method == "GET":
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = VendorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def vendor_detail(request, vendor_id):
    try:
        vendor = Vendor.objects.get(vendor_code=vendor_id)
    except Vendors.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = VendorSerializer(vendor, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        vendor.delete()
        return HttpResponse(status=204)


@csrf_exempt
def vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(vendor_code=vendor_id)
    except Vendors.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = VendorPerformanceSerializer(vendor)
        return JsonResponse(serializer.data)



@csrf_exempt
def po_list(request):
    if request.method == "GET":
        po = PurchaseOrder.objects.all()
        serializer = POSerializer(po, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = POSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def po_detail(request, po_id):
    try:
        po = PurchaseOrder.objects.get(po_number=po_id)
    except PurchaseOrder.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = POSerializer(po)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        if data.acknowledgement_date != po.acknowledgement_date:
            average_response_time(vendor_code)
        if data.status != po.status:
            update_fulfillment_rate(vendor_code)
        if data.status != po.status and data.status == "COMPLETED":     # If status changes to Completed check and update the vendors on_time_delivery_rate
            check_po_status(vendor_code)
            update_quality_rating(vendor_code)
        serializer = POSerializer(po, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        po.delete()
        return HttpResponse(status=204)


def add_acknowledgement(request, po_id):
    po = PurchaseOrder.objects.get(po_number=po_id)
    po.acknowledgement_date = datetime.now()
    po.save()
    average_response_time(po.vendor.vendor_code)
    serializer = POSerializer(po)
    return JsonResponse(serializer.data)