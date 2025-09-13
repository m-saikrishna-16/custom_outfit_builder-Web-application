from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout  
from fashion import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .tokens import generate_token  
import os
from django.shortcuts import render
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash") 
# Home View
def index(request):
    return render(request, "index.html")

# Signup View
def signup(request):
    if request.method == "POST":
        Username = request.POST['username']
        name = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Username & Email Checks
        if User.objects.filter(username=Username).exists():
            messages.error(request, "Username already exists. Please try another one.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('signup')

        if len(Username) > 10:
            messages.error(request, "Username must be under 10 characters.")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # Create User (Set is_active=False for email verification)
        myuser = User.objects.create_user(username=Username, email=email, password=pass1)
        myuser.first_name = name
        myuser.last_name = lname
        myuser.is_active = False  # User will be inactive until email is verified
        myuser.save()

        messages.success(request, "Your account has been created! Please verify your email to activate your account.")

        # Welcome Email
        subject = "Welcome to Design Django Login"
        message = f"Hello {myuser.first_name}!!\n\n" \
                  f"Welcome to Design!!\nThank you for visiting our website.\n" \
                  f"We have also sent you a confirmation email. Please confirm your email address to activate your account.\n\n" \
                  f"Thank You"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm Your Email - Design Django Login"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(email_subject, message2, from_email, [myuser.email])
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, "signup.html")

# Signin View
def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user = authenticate(username=username, password=pass1)

        if user is not None:
            if user.is_active:
                login(request, user)
                fname = user.first_name
                messages.success(request, "Successfully signed in!")
                return redirect('index')
            else:
                messages.error(request, "Your account is not activated. Please check your email for activation link.")
                return redirect('signin')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('signin')

    return render(request, "signin.html")

# Signout View
def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('index')

# Email Activation View
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your account has been activated!")
        return redirect('index')
    else:
        return render(request, 'activation_invalid.html')

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# Store chat messages in a global list (for simplicity)
session_messages = []

def chatbot(request):
     return render(request, "chat.html", {"messages": session_messages})

from django.contrib.auth.decorators import login_required

from .models import SavedDesign

@login_required
def my_designs(request):
    designs = SavedDesign.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_designs.html', {'designs': designs})


@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        user_input = data.get("message")

        if user_input:
            session_messages.append({"role": "user", "content": user_input})
            try:
                response = model.generate_content(user_input)
                ai_reply = response.text
            except Exception as e:
                ai_reply = f"Error: {e}"

            session_messages.append({"role": "assistant", "content": ai_reply})
            return JsonResponse({"reply": ai_reply})
    return JsonResponse({"reply": "Invalid request"}, status=400)





def products(request):
    return render(request, 'products.html')

from django.contrib.auth.decorators import login_required

@login_required
def cart_view(request):
    return render(request, 'cart.html', {'username': request.user.username})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
import os
@login_required
def outfit_builder(request):
    return render(request, "outfit_builder.html")

def get_outfit_image(request):
    category = request.GET.get("category", "").lower()
    color = request.GET.get("color", "").lower()
    sleeve = request.GET.get("sleeve", "").lower()

    filename = f"{category}_{color}_{sleeve}.png"
    image_path = os.path.join("static/preset_outfits", filename)

    if os.path.exists(image_path):
        return JsonResponse({"image_url": f"/static/preset_outfits/{filename}"})
    else:
        return JsonResponse({"error": "Image not found"}, status=404)


from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def save_custom_image(image, filename='custom_image.jpg', model_instance=None, field_name=None):
    
    # Convert RGBA to RGB to avoid JPEG saving error
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Save image to in-memory buffer as JPEG
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    buffer.seek(0)  # Reset buffer cursor to start

    image_file = ContentFile(buffer.read(), name=filename)

    # Save to model field if provided
    if model_instance and field_name:
        getattr(model_instance, field_name).save(filename, image_file, save=True)
        return None  # Image saved to model, no need to return file

    return image_file

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import SavedDesign
from django.contrib.auth.decorators import login_required

@csrf_exempt  # Needed if calling this via JavaScript
@login_required
def save_design(request):
    if request.method == 'POST':
        try:
            print("Request received to save design")

            data = json.loads(request.body)
            image_data = data.get('image_data')

            if image_data:
                print("Image data received")
                print("User:", request.user.username)

                design = SavedDesign(user=request.user, design_image=image_data)
                design.save()

                print("Design saved successfully")

                return JsonResponse({'success': True})
            else:
                print("No image data provided")
                return JsonResponse({'success': False, 'error': 'No image data provided'})

        except Exception as e:
            print("Error while saving:", e)
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        print("Invalid request method")
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    


# Create Gemini model instance
 # You can also try "gemini-pro"

def recommender(request):
    recommendation = None

    if request.method == 'POST':
        gender = request.POST.get("gender")
        occasion = request.POST.get("occasion")
        weather = request.POST.get("weather")
        style = request.POST.get("style")
        color = request.POST.get("color")

        prompt = (
            f"You are a professional fashion stylist. Suggest three different stylish outfit options "
            f"for a {gender} attending a {occasion} in {weather} weather. "
            f"The preferred style is {style}, and the user prefers {color} colors. "
            f"\n\n"
            f"Format the response as follows:\n"
            f"*Option 1:*\n"
            f"• Item 1\n\n"
            f"• Item 2\n\n"
            f"...\n\n"
            f"*Option 2:*\n"
            f"• Item 1\n\n"
            f"...\n\n"
            f"*Option 3:*\n"
            f"...\n\n"
            f"Make sure there's a line gap between each bullet point. Keep it realistic, fashionable, and easy to read."
        )

        try:
            response = model.generate_content(prompt)
            recommendation = response.text
        except Exception as e:
            recommendation = f"⚠ Error: {str(e)}"

    return render(request, 'recommender.html', {'recommendation': recommendation})

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem

@csrf_exempt
def place_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cart_items = data.get("cart", [])
            name = data.get("name", "Anonymous")

            # Calculate total price
            total_price = sum(item.get('price', 0) * item.get('quantity', 1) for item in cart_items)

            # Save Order
            order = Order.objects.create(name=name, total=total_price)

            # Save OrderItems
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_id=item.get('id', 0),  # 0 or None for custom designs
                    title=item.get('title', 'Custom Design'),
                    price=item.get('price', 0),
                    quantity=item.get('quantity', 1),
                    image=item.get('image', '')
                )

            return JsonResponse({"message": "Order placed successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)

def order_success(request):
    return render(request, 'order_success.html')

from django.http import JsonResponse
from .models import Product

def get_products(request):
    products = Product.objects.all()
    data = [product.to_dict() for product in products]
    return JsonResponse(data, safe=False)
