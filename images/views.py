from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Image, VisitorPass
from utilities.ocr import extract_text_from_image, detect_card_type, extract_aadhaar_details, extract_pan_details
from utilities.qr_handler import generate_qr
from django.core.files.base import ContentFile
from datetime import datetime
import pytz

@csrf_exempt
def upload_image(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    try:
        image_data = request.FILES.get('image')
        if not image_data:
            return JsonResponse({'error': 'No image provided'}, status=400)

        # Save image to the database
        img_instance = Image.objects.create(image=image_data)
        image_path = img_instance.image.path
        img_name = image_path.split("\\")[-1]

        # Extract text and card details
        extracted_text = extract_text_from_image(image_path)
        card_type = detect_card_type(extracted_text)

        if card_type == "aadhaar":
            details = extract_aadhaar_details(extracted_text)
        elif card_type == "pan":
            details = extract_pan_details(extracted_text)
        else:
            details = {"error": "Could not determine card type"}

        details['qr_img_name'] = f'qr_{img_name}'

        return JsonResponse({
            'message': 'Image uploaded successfully',
            'id': img_instance.id,
            'card_type': card_type,
            'details': details
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def upload_page(request):
    return render(request, 'index.html')

@csrf_exempt
def visiting_pass(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    data = request.POST.dict()
    qr_img_name = data.get('qr_img_name', 'default_qr.png')
    pass_id = data.get('pass_id', 'NA')
    expire_at = data.get('expire_at')

    # Generate QR code
    generate_qr(f"http://127.0.0.1:8000/visiting-pass/{pass_id}/", qr_img_name)

    # Get date and time
    dt = datetime.now(pytz.timezone("Asia/Kolkata"))
    date = dt.strftime("%d/%m/%Y")
    time = dt.strftime("%H:%M")

    context = {
        'visitor_name': data.get('Name', 'NA'),
        'date_of_birth': data.get('DOB', 'NA'),
        'gender': data.get('Gender', 'NA'),
        'phone_number': data.get('phone', 'NA'),
        'email': data.get('Email', 'NA'),
        'purpose': 'Project Meeting',
        'date': date,
        'time': time,
        'duration': data.get('Duration', 'NA'),
        'qr_img_name': qr_img_name,
        'pass_id': pass_id,
        'expire_at': expire_at
    }

    # Save VisitorPass to database
    if expire_at:
        context['expire_at'] = pytz.timezone('Asia/Kolkata').localize(datetime.strptime(expire_at, '%Y-%m-%dT%H:%M'))
    
    VisitorPass.objects.create(
        visitor_name=context['visitor_name'],
        date_of_birth=context['date_of_birth'],
        gender=context['gender'],
        phone_number=context['phone_number'],
        email=context['email'],
        purpose=context['purpose'],
        date=context['date'],
        time=context['time'],
        duration=context['duration'],
        qr_img_name=context['qr_img_name'],
        pass_id=context['pass_id'],
        expire_at=context.get('expire_at')
    )

    return render(request, 'visiting_pass.html', context)

def get_visiting_pass(request, pass_id):
    try:
        visitor_pass = VisitorPass.objects.get(pass_id=pass_id)
    except VisitorPass.DoesNotExist:
        return HttpResponse(f'<h1>No pass exists for pass id {pass_id}.</h1>')
    
    context = {
        'visitor_name': visitor_pass.visitor_name,
        'date_of_birth': visitor_pass.date_of_birth,
        'gender': visitor_pass.gender,
        'phone_number': visitor_pass.phone_number,
        'email': visitor_pass.email,
        'purpose': visitor_pass.purpose,
        'date': visitor_pass.date,
        'time': visitor_pass.time,
        'duration': visitor_pass.duration,
        'qr_img_name': visitor_pass.qr_img_name,
        'pass_id': visitor_pass.pass_id,
        'expire_at': visitor_pass.expire_at.strftime('%d/%m/%Y, %H:%M')
    }

    if visitor_pass.expire_at < datetime.now(pytz.timezone('Asia/Kolkata')):
        return HttpResponse(f'<h1 style="color: red;">Pass with pass id {pass_id} expired at {context["expire_at"]}.</h1>')
    
    return render(request, 'visiting_pass.html', context)
