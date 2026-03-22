import re

def clean_text(text):
    text = re.sub(r'(?<=\w)\s(?=\w)', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def extract_structured(full_text):

    text = clean_text(full_text)

    data = {
        "shipment_id": None,
        "shipper": None,
        "consignee": None,
        "pickup_datetime": None,
        "delivery_datetime": None,
        "equipment_type": None,
        "mode": None,
        "rate": None,
        "currency": None,
        "weight": None,
        "carrier_name": None
    }

    patterns = {
        "shipment_id": r'Load\s*ID[:\s]*([A-Z0-9]+)',
        "pickup_datetime": r'(Ship|Pickup)\s*Date[:\s]*([0-9\-:\s]+)',
        "delivery_datetime": r'Delivery\s*Date[:\s]*([0-9\-:\s]+)',
        "shipper": r'Shipper[:\s]*(.*?)(?=Consignee|$)',
        "consignee": r'Consignee[:\s]*(.*?)(?=3rd Party|$)',
        "weight": r'Weight[:\s]*(.*)'
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            if key == "pickup_datetime":
                data[key] = match.group(2).strip()
            else:
                data[key] = match.group(1).strip()

    return data