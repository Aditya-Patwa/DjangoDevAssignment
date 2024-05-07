from .models import PurchaseOrder, Vendor
import datetime
# Check for PO Metrics

def check_po_status(vendor_code):
    vendor = Vendor.objects.get(vendor_code=vendor_code)
    vendors_po = vendor.purchaseorder_set.all()
    total_po = vendor.purchaseorder_set.count()
    before_deadline = 0
    for po in vendors_po:
        if datetime.datetime.now() - po.delivery_data() >= 0:
            before_deadline += 1
    if total_po > 0:    
        vendor.on_time_delivery_rate = before_deadline/total_po
        vendor.save()


def average_response_time(vendor_code):
    vendor = Vendor.objects.get(vendor_code=vendor_code)
    vendors_po = vendor.purchaseorder_set.all()
    acknowledged_pos = 0
    timedeltas = []
    for po in vendors_po:
        if po.acknowledgement_date is not None:
            acknowledged_pos += 1
            timedelta = po.acknowledgement_date - po.issue_date
            timedeltas.append(timedelta)
    
    total_time = sum(timedeltas, datetime.timedelta(0)) / len(timedeltas)
    vendor.average_response_time = total_time.days + total_time.seconds/(3600*24)
    vendor.save()




def update_quality_rating(vendor_code):
    vendor = Vendor.objects.get(vendor_code=vendor_code)
    completed_po = PurchaseOrder.objects.filter(vendor=vendor, status="COMPLETED")
    total_completed_pos = len(completed_po)
    average_quality = 0
    for po in completed_po:
        average_quality += po.quantity
    vendor.quality_rating_avg = average_quality/total_completed_pos

def update_fulfillment_rate(vendor_code):
    vendor = Vendor.objects.get(vendor_code=vendor_code)
    total_po = vendor.purchaseorder_set.count()
    completed_po = PurchaseOrder.objects.filter(vendor=vendor, status="COMPLETED").count()
    vendor.fulfillment_rate = completed_po/total_po
    vendor.save()