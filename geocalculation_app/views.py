from django.shortcuts import render,redirect
from django.db.models import Avg
from .models import *
from django.http import HttpResponse
from .decrypt_util import decrypt_value
import csv
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
import csv
from io import TextIOWrapper
from django.contrib.auth.hashers import make_password
from .models import User
from django.contrib import messages
import re
import geopandas as gpd
from shapely.geometry import Point
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render  # Make sure to import render
from io import TextIOWrapper
import csv
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from datetime import datetime,timedelta



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect(reverse('admin_dasboard'))
                elif user.is_approved:
                    login(request, user)
                    request.session['user_id'] = user.id
                    return redirect(reverse('geoid_dashboard'))
                else:
                    error = 'Your account is awaiting approval.'
                    return render(request, 'login.html', {'error': error})
            else:
                error = 'Invalid email or password'
                return render(request, 'login.html', {'error': error})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')


def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        request.session['username'] = username
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('admin_dasboard'))
            else:
                return render(request, 'adminlogin.html', {'error': 'Invalid email or password'})
        except User.DoesNotExist:
            return render(request, 'adminlogin.html', {'error': 'Invalid email or password'})
    context = {}
    if 'username' in request.session:
        context['username'] = request.session['username']
    return render(request, 'adminlogin.html', context)


def admin_dasboard(request):
    pendingdata = User.objects.filter(status='PENDING').count()
    allapproved = User.objects.filter(status='APPROVED').count()
    allrejected = User.objects.filter(status='REJECTED').count()
    totaldata = User.objects.values_list('status').count()
    context = {
        'pendingdata':pendingdata,
        'allapproved':allapproved,
        'allrejected':allrejected,
        'totaldata':totaldata,
       
    }
    return render(request,'admindashboard.html',context)




from django.shortcuts import render
from django.http import HttpResponse
from geocalculation_app.models import User  


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        aadhar = request.POST.get("aadhar", "").strip()
        mobileno = request.POST.get("mobileno", "").strip()
        goverment_id_no = request.POST.get("goverment_id_no", "").strip()
        student_id_no = request.POST.get("student_id_no", "").strip()
        print(student_id_no)
        aadhar_card = request.FILES.get("aadhar_card")
        nda_document = request.FILES.get("nda_document")
        govtidcard = request.FILES.get("govtidcard")
        academicidcard = request.FILES.get("academicidcard")
        user_type = request.POST.get("user_type")  
        if User.objects.filter(email=email).exists():
            errors = 'This Email Id Allready Exists Please Use another Email Id'
            return render(request, "signup.html",{'errors':errors})
        if User.objects.filter(aadhar_no=aadhar).exists():
            errorss = 'This Aadhar No Allready Exists'
            return render(request, "signup.html",{'errorss':errorss})
        if User.objects.filter(goverment_idcard_no=goverment_id_no).exists():
            err = 'This Goverment Id Card No  Allready Exists'
            return render(request, "signup.html",{'err':err})
        if student_id_no and User.objects.filter(student_idcard_no=student_id_no).exists():
            erro = 'This Student Id Card No Already Exists'
            return render(request, "signup.html", {'erro': erro})

        try: 
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                aadhar_no=aadhar,
                aadharcard_upload=aadhar_card,
                nda_upload=nda_document,
                mobile_no = mobileno,
                govt_idcard=govtidcard,
                institute_idcard=academicidcard,
                goverment_idcard_no = goverment_id_no,
                student_idcard_no = student_id_no,
                is_approved=False

            )

            # Set user type based on selection
            if user_type == "govt":
                user.user_types ="GOVT USER"
                user.govt_user = True
            elif user_type == "private":
                user.user_types ="PRIVATE USER"
                user.private_user = True
            elif user_type == "academic":
                user.user_types ="ACADEMIC USER"
                user.academic_user = True
            user.save()

            return redirect(reverse('login_view'))
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)

    return render(request, "signup.html")


def approve_users(request):
    option = request.GET.get('option', None)
    if option == 'APPROVED':
        users = User.objects.filter(status='APPROVED')
    elif option == 'REJECTED':
        users = User.objects.filter(status='REJECTED')
    elif option == 'PENDING':
        users = User.objects.filter(status='PENDING')
    else: 
        users = User.objects.all()
    return render(request, 'approve_users.html', {'users': users})


def edituser(request,id):
    if request.method == 'POST':
        status = request.POST.get('status')
        try:
            user = User.objects.get(id=id)
            user.status = status
            if status == 'APPROVED':
                user.save()
                user.is_approved = True
                print(user.is_approved)
            else:
                user.is_approved = False
            user.save()
            return redirect('approve_users') 
        except User.DoesNotExist:
            return HttpResponse("User not found", status=404)

    alldata = User.objects.filter(id=id)
    return render(request,'edituser.html',{'alldata':alldata})



def update_user_status(request, id):
    if request.method == 'POST':
        status = request.POST.get('status')
        print(status)
        try:
            user = User.objects.get(id=id)
            print('HELLO',user)
            user.status = status
            if status == 'APPROVED':
                user.save()
                user.is_approved = True
                print(user.is_approved)
            else:
                user.is_approved = False
            user.save()
            return redirect('edituser', id=id)  # Redirect to the same page or another page
        except User.DoesNotExist:
            return HttpResponse("User not found", status=404)
    else:
        return HttpResponse("Invalid request method", status=400)

def logout_view(request):
    logout(request)
    return redirect('login_view')


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(reverse('password_reset_confirm', args=[uid, token]))

            # Send reset link via email
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_url}',
                'your-email@example.com',
                [email],
                fail_silently=False,
            )

            return HttpResponse("A password reset link has been sent to your email.")
        except User.DoesNotExist:
            return HttpResponse("Email not found.")

    return render(request, 'password_reset_request.html')



def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password == confirm_password:
                user.password = make_password(new_password)
                user.save()
                return HttpResponse("Password has been reset successfully.")
            else:
                return HttpResponse("Passwords do not match.")

        return render(request, 'password_reset_confirm.html', {'valid_link': True})
    else:
        return HttpResponse("The reset link is invalid or has expired.")

# import csv
# from io import TextIOWrapper
############################################################################################  Average ######################################################################################
# def home(request):
#     if request.method == 'POST':
#         lat_data = request.POST.get('lat')
#         lon_data = request.POST.get('lon')
#         if lat_data and lon_data:
#             lat_data = float(lat_data)
#             lon_data = float(lon_data)
#             try:
#                 exact_point = GridPoint.objects.get(latitude=lat_data, longitude=lon_data)
#                 return render(request, 'index.html', {'exact_point': exact_point})
#             except GridPoint.DoesNotExist:
#                 nearest_points = GridPoint.objects.filter(latitude__gte=lat_data-0.08333, 
#                                                            latitude__lte=lat_data+0.08333, 
#                                                            longitude__gte=lon_data-0.08333, 
#                                                            longitude__lte=lon_data+0.08333)
#                 if nearest_points.exists():
#                     average_value = round(nearest_points.aggregate(Avg('value'))['value__avg'], 3)
#                     return render(request, 'index.html', {'average_value': average_value})
#                 else:
#                     return render(request, 'index.html', {'error_message': 'No points found near the provided latitude and longitude.'})
#         elif 'csv_file' in request.FILES:
#             csv_file = request.FILES['csv_file']
#             csv_data = TextIOWrapper(csv_file, encoding=request.encoding)
#             reader = csv.DictReader(csv_data)
#             latitudes = []
#             longitudes = []
#             for row in reader:
#                 latitudes.append(float(row['lat']))
#                 longitudes.append(float(row['lon']))
#             # Process latitude and longitude values as needed
#             lat_avg = sum(latitudes) / len(latitudes)
#             lon_avg = sum(longitudes) / len(longitudes)
#             exact_point = GridPoint.objects.get(latitude=lat_avg, longitude=lon_avg)
#             return render(request, 'index.html', {'exact_point': exact_point})
#         else:
#             return render(request, 'index.html', {'error_message': 'Please provide latitude and longitude or upload a CSV file.'})
#     return render(request, 'index.html')

#########################################################################################################################################################

# def home(request):
#     if request.method == 'POST':
#         lat_data = request.POST.get('lat')
#         lon_data = request.POST.get('lon')
#         if lat_data and lon_data:
#             lat_data = float(lat_data)
#             lon_data = float(lon_data)
#             try:
#                 exact_point = GridPoint.objects.get(latitude=lat_data, longitude=lon_data)
#                 exact_point.value = decrypt_value(exact_point.value)
#                 return render(request, 'index.html', {'exact_point': exact_point})
#             except GridPoint.DoesNotExist:
#                 nearest_points = GridPoint.objects.filter(
#                     latitude__gte=lat_data - 0.08333, 
#                     latitude__lte=lat_data + 0.08333, 
#                     longitude__gte=lon_data - 0.08333, 
#                     longitude__lte=lon_data + 0.08333
#                 )
#                 if nearest_points.exists():
#                     decrypted_values = [
#                         decrypt_value(point.value) for point in nearest_points
#                     ]
#                     average_value = round(sum(decrypted_values) / len(decrypted_values), 3)
#                     return render(request, 'index.html', {'average_value': average_value, 'lat_data': lat_data, 'lon_data': lon_data})
#                 else:
#                     return render(request, 'index.html', {'error_message': 'No points found near the provided latitude and longitude.'})
#         elif 'csv_file' in request.FILES:
#             csv_file = request.FILES['csv_file']
#             csv_data = TextIOWrapper(csv_file, encoding=request.encoding)
#             reader = csv.DictReader(csv_data)
#             points_data = []
#             for row in reader:
#                 if row['lat'].strip() and row['lon'].strip():
#                     lat_data = float(row['lat'].strip())
#                     lon_data = float(row['lon'].strip())
#                     try:
#                         exact_point = GridPoint.objects.get(latitude=lat_data, longitude=lon_data)
#                         exact_point_dict = {
#                             'latitude': exact_point.latitude,
#                             'longitude': exact_point.longitude,
#                             'value': decrypt_value(exact_point.value)
#                         }
#                         points_data.append({'latitude': lat_data, 'longitude': lon_data, 'exact_point': exact_point_dict})
#                     except GridPoint.DoesNotExist:
#                         nearest_points = GridPoint.objects.filter(
#                             latitude__gte=lat_data - 0.08333,
#                             latitude__lte=lat_data + 0.08333,
#                             longitude__gte=lon_data - 0.08333,
#                             longitude__lte=lon_data + 0.08333
#                         )
#                         if nearest_points.exists():
#                             decrypted_values = [
#                                 decrypt_value(point.value) for point in nearest_points
#                             ]
#                             average_value = round(sum(decrypted_values) / len(decrypted_values), 3)
#                             points_data.append({'latitude': lat_data, 'longitude': lon_data, 'average_value': average_value})
#                         else:
#                             points_data.append({'latitude': lat_data, 'longitude': lon_data, 'error_message': 'No points found near the provided latitude and longitude.'})
#                 else:
#                     points_data.append({'latitude': None, 'longitude': None, 'error_message': 'Latitude or longitude is missing or empty in the CSV row.'})
            
#             # Save points_data in session
#             request.session['points_data'] = points_data
#             return render(request, 'index.html', {'points_data': points_data})
#         else:
#             return render(request, 'index.html', {'error_message': 'Please provide latitude and longitude or upload a CSV file.'})
#     return render(request, 'index.html')




# def download_processed_csv(request):
#     if 'points_data' in request.session:
#         points_data = request.session['points_data']
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="processed_data.csv"'
#         writer = csv.writer(response)
#         writer.writerow(['Latitude', 'Longitude', 'Data'])
#         for data in points_data:
#             latitude = data['latitude']
#             longitude = data['longitude']
#             value = data.get('exact_point', {}).get('value') or data.get('average_value') or data.get('error_message')
#             if isinstance(value, str) and not value.startswith('No points found') and not value.startswith('Latitude or longitude'):
#                 try:
#                     value = decrypt_value(value)
#                 except Exception as e:
#                     value = f"Decryption failed: {e}"
            
#             writer.writerow([latitude, longitude, value])
#         return response
#     else:
#         return HttpResponse("No processed data available.", status=404)


##########################################################################################  0.08333 #########################################################################
# from django.shortcuts import render,redirect
# from django.db.models import Avg
# from .models import *
# from django.http import HttpResponse
# from django.urls import reverse
# import csv
# from io import TextIOWrapper

# def home(request):
#     if request.method == 'POST':
#         lat_data = request.POST.get('lat')
#         lon_data = request.POST.get('lon')
#         if lat_data and lon_data:
#             lat_data = float(lat_data)
#             lon_data = float(lon_data)
#             try:
#                 exact_point = GridPoint.objects.get(latitude=lat_data, longitude=lon_data)
#                 return render(request, 'index.html', {'exact_point': exact_point})
#             except GridPoint.DoesNotExist:
#                 nearest_points = GridPoint.objects.filter(latitude__gte=lat_data-0.08333, 
#                                                            latitude__lte=lat_data+0.08333, 
#                                                            longitude__gte=lon_data-0.08333, 
#                                                           longitude__lte=lon_data+0.08333)
#                 if nearest_points.exists():
#                     average_value = round(nearest_points.aggregate(Avg('value'))['value__avg'], 3)
#                     return render(request, 'index.html', {'average_value': average_value,'lat_data':lat_data,'lon_data':lon_data})
                    
#                 else:
#                     return render(request, 'index.html', {'error_message': 'No points found near the provided latitude and longitude.'})
#         elif 'csv_file' in request.FILES:
#             csv_file = request.FILES['csv_file']
#             csv_data = TextIOWrapper(csv_file, encoding=request.encoding)
#             reader = csv.DictReader(csv_data)
#             points_data = []
#             for row in reader:
#                 if row['lat'].strip() and row['lon'].strip():  
#                     lat_data = float(row['lat'].strip())
#                     lon_data = float(row['lon'].strip())
#                     try:
#                         exact_point = GridPoint.objects.get(latitude=lat_data, longitude=lon_data)
#                         exact_point_dict = {
#                             'latitude': exact_point.latitude,
#                             'longitude': exact_point.longitude,
#                             'value': exact_point.value  # Assuming 'value' is an attribute of GridPoint
#                         }
#                         points_data.append({'latitude': lat_data, 'longitude': lon_data, 'exact_point': exact_point_dict})
#                     except GridPoint.DoesNotExist:
#                         nearest_points = GridPoint.objects.filter(latitude__gte=lat_data-0.08333, 
#                                                                 latitude__lte=lat_data+0.08333, 
#                                                                 longitude__gte=lon_data-0.08333, 
#                                                                 longitude__lte=lon_data+0.08333)
#                         if nearest_points.exists():
#                             average_value = round(nearest_points.aggregate(Avg('value'))['value__avg'], 3)
#                             points_data.append({'latitude': lat_data, 'longitude': lon_data, 'average_value': average_value})
#                         else:
#                             points_data.append({'latitude': lat_data, 'longitude': lon_data, 'error_message': 'No points found near the provided latitude and longitude.'})
#                 else:
#                     points_data.append({'latitude': None, 'longitude': None, 'error_message': 'Latitude or longitude is missing or empty in the CSV row.'})
            
#             # Save points_data in session
#             request.session['points_data'] = points_data
#             return render(request, 'index.html', {'points_data': points_data})
#         else:
#             return render(request, 'index.html', {'error_message': 'Please provide latitude and longitude or upload a CSV file.'})
#     return render(request, 'index.html')

##########################################################################################  0.08333 #########################################################################





# def home(request):
#     if request.method == 'POST':
#         lat_data = request.POST.get('lat')
#         lon_data = request.POST.get('lon')
#         latmin = request.POST.get('latmin')
#         latmax = request.POST.get('latmax')
#         lonmin = request.POST.get('lonmin')
#         lonmax = request.POST.get('lonmax')

#         if lat_data and lon_data:
#             lat_data = float(lat_data)
#             lon_data = float(lon_data)
#             try:
#                 # Find the exact point
#                 exact_point = GridPoint.objects.get(latitude=lat_data, longitude=lon_data)
#                 return render(request, 'index.html', {'exact_point': exact_point})
#             except GridPoint.DoesNotExist:
#                # Bilinear interpolation calculation
#                 p1 = GridPoint.objects.filter(latitude__lte=lat_data, longitude__lte=lon_data).order_by('-latitude', '-longitude').first()
                
#                 p2 = GridPoint.objects.filter(latitude__lte=lat_data, longitude__gte=lon_data).order_by('-latitude', 'longitude').first()
               
#                 p3 = GridPoint.objects.filter(latitude__gte=lat_data, longitude__lte=lon_data).order_by('latitude', '-longitude').first()
               
#                 p4 = GridPoint.objects.filter(latitude__gte=lat_data, longitude__gte=lon_data).order_by('latitude', 'longitude').first()
          

#                 if p1 and p2 and p3 and p4:
                    
#                     # Extract the coordinates and values, ensuring all are cast to float
#                     x1, y1, f11 = float(p1.latitude), float(p1.longitude), float(p1.value)
#                     x2, y1, f21 = float(p2.latitude), float(p2.longitude), float(p2.value)
#                     x1, y2, f12 = float(p3.latitude), float(p3.longitude), float(p3.value)
#                     x2, y2, f22 = float(p4.latitude), float(p4.longitude), float(p4.value)
#                     print(x1, y1, f11)
#                     print(x2, y1, f21)
#                     print(x1, y2, f12)
#                     print(x2, y2, f22)
#                     # Check if (x2 - x1) or (y2 - y1) equals 0, which would cause division by zero
#                     if (x2 - x1) == 0 or (y2 - y1) == 0:
#                         return render(request, 'index.html', {
#                             'error_message': 'The surrounding points are too close or identical. Bilinear interpolation is not possible.'
#                         })

#                     # Bilinear interpolation formula
#                     interpolated_value = (
#                         (x2 - lat_data) * (y2 - lon_data) * f11 +
#                         (lat_data - x1) * (y2 - lon_data) * f21 +
#                         (x2 - lat_data) * (lon_data - y1) * f12 +
#                         (lat_data - x1) * (lon_data - y1) * f22
#                     ) / ((x2 - x1) * (y2 - y1))

#                     interpolated_value = round(interpolated_value, 3)

#                     return render(request, 'index.html', {
#                         'interpolated_value': interpolated_value,
#                         'lat_data': lat_data,
#                         'lon_data': lon_data
#                     })
#                 else:
#                     return render(request, 'index.html', {
#                         'error_message': 'Not enough points found for bilinear interpolation.'
#                     })


        
#         elif latmin and latmax and lonmin and lonmax:
#             latmin = float(latmin)
#             latmax = float(latmax)
#             lonmin = float(lonmin)
#             lonmax = float(lonmax)
#             row_step = 0.08333333
#             col_step = 0.08333333

#             points_in_range = GridPoint.objects.filter(
#                 latitude__gte=latmin,
#                 latitude__lte=latmax,
#                 longitude__gte=lonmin,
#                 longitude__lte=lonmax
#             ).order_by('latitude', 'longitude')

#             if points_in_range.exists():
#                 # Prepare the data
#                 output = []
#                 output.append(f"{latmin:.6f}   {latmax:.6f}   {lonmin:.6f}   {lonmax:.6f}   {row_step:.8f}   {col_step:.8f}")

#                 # Create a 2D grid list
#                 latitudes = sorted(set(p.latitude for p in points_in_range))
#                 longitudes = sorted(set(p.longitude for p in points_in_range))
#                 grid = [[None] * len(longitudes) for _ in range(len(latitudes))]

#                 for point in points_in_range:
#                     lat_idx = latitudes.index(float(point.latitude))
#                     lon_idx = longitudes.index(float(point.longitude))
#                     grid[lat_idx][lon_idx] = f"{float(point.value):.3f}"

#                 # Append the grid data
#                 for row in grid:
#                     output.append("   ".join(val if val is not None else "NaN" for val in row))

#                 # Create the HTTP response with .gri data
#                 response = HttpResponse("\n".join(output), content_type='text/plain')
#                 response['Content-Disposition'] = 'attachment; filename="grid_data.gri"'
#                 return response

#             else:
#                 return render(request, 'index.html', {'error_message': 'No points found within the specified range.'})
        
#         elif 'csv_file' in request.FILES:
#             csv_file = request.FILES['csv_file']
#             csv_data = TextIOWrapper(csv_file, encoding=request.encoding)
#             reader = csv.DictReader(csv_data)
#             points_data = []
#             for row in reader:
#                 if row['lat'].strip() and row['lon'].strip():  
#                     lat_data = float(row['lat'].strip())
#                     lon_data = float(row['lon'].strip())
#                     try:
#                         exact_point = GridPoint.objects.get(latitude=lat_data, longitude=lon_data)
#                         exact_point_dict = {
#                             'latitude': exact_point.latitude,
#                             'longitude': exact_point.longitude,
#                             'value': exact_point.value  # Assuming 'value' is an attribute of GridPoint
#                         }
#                         points_data.append({'latitude': lat_data, 'longitude': lon_data, 'exact_point': exact_point_dict})
#                     except GridPoint.DoesNotExist:
#                         nearest_points = GridPoint.objects.filter(
#                             latitude__gte=lat_data-0.04166, 
#                             latitude__lte=lat_data+0.04166, 
#                             longitude__gte=lon_data-0.04166, 
#                             longitude__lte=lon_data+0.04166
#                         )
#                         if nearest_points.exists():
#                             average_value = round(nearest_points.aggregate(Avg('value'))['value__avg'], 3)
#                             points_data.append({'latitude': lat_data, 'longitude': lon_data, 'average_value': average_value})
#                         else:
#                             points_data.append({'latitude': lat_data, 'longitude': lon_data, 'error_message': 'No points found near the provided latitude and longitude.'})
#                 else:
#                     points_data.append({'latitude': None, 'longitude': None, 'error_message': 'Latitude or longitude is missing or empty in the CSV row.'})
            
#             # Save points_data in session
#             request.session['points_data'] = points_data
#             return render(request, 'index.html', {'points_data': points_data})
#         else:
#             return render(request, 'index.html', {'error_message': 'Please provide latitude and longitude or upload a CSV file.'})
    
#     return render(request, 'index.html')

########################################################################################  0.04166 Nearest Point ####################################################################


# def geoid_dashboard(request):
#     if request.method == 'POST':
#         lat_data = request.POST.get('lat')
#         lon_data = request.POST.get('lon')
#         latmin = request.POST.get('latmin')
#         latmax = request.POST.get('latmax')
#         lonmin = request.POST.get('lonmin')
#         lonmax = request.POST.get('lonmax')

#         if lat_data and lon_data:
#             lat_data = float(lat_data)
#             lon_data = float(lon_data)
#             try:
#                 exact_point = GridPoint.objects.get(latitude=lat_data, longitude=lon_data)
#                 return render(request, 'index.html', {'exact_point': exact_point})
#             except GridPoint.DoesNotExist:
#                 nearest_points = GridPoint.objects.filter(
#                     latitude__gte=lat_data-0.04166, 
#                     latitude__lte=lat_data+0.04166, 
#                     longitude__gte=lon_data-0.04166, 
#                     longitude__lte=lon_data+0.04166
#                 )
#                 print(nearest_points)
#                 if nearest_points.exists():
#                     average_value = round(nearest_points.aggregate(Avg('value'))['value__avg'], 3)
#                     print(average_value)
#                     return render(request, 'index.html', {'average_value': average_value,'lat_data':lat_data,'lon_data':lon_data})
#                 else:
#                     return render(request, 'index.html', {'error_message': 'No points found near the provided latitude and longitude.'})
        
#         elif latmin and latmax and lonmin and lonmax:
#             latmin = float(latmin)
#             latmax = float(latmax)
#             lonmin = float(lonmin)
#             lonmax = float(lonmax)
#             row_step = 0.08333333
#             col_step = 0.08333333

#             points_in_range = GridPoint.objects.filter(
#                 latitude__gte=latmin,
#                 latitude__lte=latmax,
#                 longitude__gte=lonmin,
#                 longitude__lte=lonmax
#             ).order_by('latitude', 'longitude')

#             if points_in_range.exists():
#                 # Prepare the data
#                 output = []
#                 output.append(f"{latmin:.6f}   {latmax:.6f}   {lonmin:.6f}   {lonmax:.6f}   {row_step:.8f}   {col_step:.8f}")

#                 # Create a 2D grid list
#                 latitudes = sorted(set(p.latitude for p in points_in_range))
#                 longitudes = sorted(set(p.longitude for p in points_in_range))
#                 grid = [[None] * len(longitudes) for _ in range(len(latitudes))]

#                 for point in points_in_range:
#                     lat_idx = latitudes.index(float(point.latitude))
#                     lon_idx = longitudes.index(float(point.longitude))
#                     grid[lat_idx][lon_idx] = f"{float(point.value):.3f}"

#                 # Append the grid data
#                 for row in grid:
#                     output.append("   ".join(val if val is not None else "NaN" for val in row))

#                 # Create the HTTP response with .gri data
#                 response = HttpResponse("\n".join(output), content_type='text/plain')
#                 response['Content-Disposition'] = 'attachment; filename="grid_data.gri"'
#                 return response

#             else:
#                 return render(request, 'index.html', {'error_message': 'No points found within the specified range.'})
        
#         elif 'csv_file' in request.FILES:
#             csv_file = request.FILES['csv_file']
#             csv_data = TextIOWrapper(csv_file, encoding=request.encoding)
#             reader = csv.DictReader(csv_data)
#             points_data = []
#             for row in reader:
#                 if row['lat'].strip() and row['lon'].strip():  
#                     lat_data = float(row['lat'].strip())
#                     lon_data = float(row['lon'].strip())
#                     try:
#                         exact_point = GridPoint.objects.get(latitude=lat_data, longitude=lon_data)
#                         exact_point_dict = {
#                             'latitude': exact_point.latitude,
#                             'longitude': exact_point.longitude,
#                             'value': exact_point.value  # Assuming 'value' is an attribute of GridPoint
#                         }
#                         points_data.append({'latitude': lat_data, 'longitude': lon_data, 'exact_point': exact_point_dict})
#                     except GridPoint.DoesNotExist:
#                         nearest_points = GridPoint.objects.filter(
#                             latitude__gte=lat_data-0.04166, 
#                             latitude__lte=lat_data+0.04166, 
#                             longitude__gte=lon_data-0.04166, 
#                             longitude__lte=lon_data+0.04166
#                         )
                        
#                         if nearest_points.exists():
#                             average_value = round(nearest_points.aggregate(Avg('value'))['value__avg'], 3)
#                             points_data.append({'latitude': lat_data, 'longitude': lon_data, 'average_value': average_value})
#                         else:
#                             points_data.append({'latitude': lat_data, 'longitude': lon_data, 'error_message': 'No points found near the provided latitude and longitude.'})
#                 else:
#                     points_data.append({'latitude': None, 'longitude': None, 'error_message': 'Latitude or longitude is missing or empty in the CSV row.'})
            
#             # Save points_data in session
#             request.session['points_data'] = points_data
#             return render(request, 'index.html', {'points_data': points_data})
#         else:
#             return render(request, 'index.html', {'error_message': 'Please provide latitude and longitude or upload a CSV file.'})
    
#     return render(request, 'index.html')

########################################################################################  0.04166 Nearest Point ####################################################################

# def bilinear_interpolation(x, y, x1, y1, f11, x2, y2, f22, f12, f21):
#     if (x2 - x1) == 0 or (y2 - y1) == 0:
#         return None

#     return (
#         f11 * (x2 - x) * (y2 - y) +
#         f21 * (x - x1) * (y2 - y) +
#         f12 * (x2 - x) * (y - y1) +
#         f22 * (x - x1) * (y - y1)
#     ) / ((x2 - x1) * (y2 - y1))



# def linear_interpolation(lat_data, lon_data):
#     # Find two nearest longitude points for the same latitude
#     p1 = GridPoint.objects.filter(latitude=lat_data, longitude__lte=lon_data).order_by('-longitude').first()
#     p2 = GridPoint.objects.filter(latitude=lat_data, longitude__gte=lon_data).order_by('longitude').first()

#     if p1 and p2:
#         lon1, f1 = float(p1.longitude), float(p1.value)
#         lon2, f2 = float(p2.longitude), float(p2.value)

#         # Ensure longitudes are not identical for linear interpolation
#         if lon2 != lon1:
#             interpolated_value = f1 + (f2 - f1) * (lon_data - lon1) / (lon2 - lon1)
#             interpolated_value = round(interpolated_value, 3)
#             print('interpolated_value',interpolated_value) 
#             return render(None, 'index.html', {
#                 'average_value': interpolated_value,
#                 'lat_data': lat_data,
#                 'lon_data': lon_data
#             })
#         else:
#             return render(None, 'index.html', {
#                 'error_message': 'The surrounding points have identical longitudes. Linear interpolation is not possible.'
#             })

#     else:
#         return render(None, 'index.html', {
#             'error_message': 'Not enough points found for interpolation.'
#         })


# def home(request):
#     if request.method == 'POST':
#         lat_data = request.POST.get('lat')
#         lon_data = request.POST.get('lon')
#         latmin = request.POST.get('latmin')
#         latmax = request.POST.get('latmax')
#         lonmin = request.POST.get('lonmin')
#         lonmax = request.POST.get('lonmax')
#         if lat_data and lon_data:
#             lat_data = float(lat_data)
#             lon_data = float(lon_data)
#             try:
#                 # Find the exact point
#                 exact_point = GridPoint.objects.get(latitude=lat_data, longitude=lon_data)
#                 return render(request, 'index.html', {'exact_point': exact_point})
#             except GridPoint.DoesNotExist:
#                # Bilinear interpolation calculation
#                 p1 = GridPoint.objects.filter(latitude__lte=lat_data, longitude__lte=lon_data).order_by('-latitude', '-longitude').first()
#                 p2 = GridPoint.objects.filter(latitude__lte=lat_data, longitude__gte=lon_data).order_by('-latitude', 'longitude').first()
#                 p3 = GridPoint.objects.filter(latitude__gte=lat_data, longitude__lte=lon_data).order_by('latitude', '-longitude').first()
#                 p4 = GridPoint.objects.filter(latitude__gte=lat_data, longitude__gte=lon_data).order_by('latitude', 'longitude').first()
#                 # Check if bilinear interpolation is possible
#                 if p1 and p2 and p3 and p4:
#                     lat1, lon1, f11 = float(p1.latitude), float(p1.longitude), float(p1.value)
#                     lat2, lon2, f22 = float(p4.latitude), float(p4.longitude), float(p4.value)
#                     f12 = float(p2.value)
#                     f21 = float(p3.value)
#                     # Bilinear interpolation only if the latitudes and longitudes are not too close
#                     if (lat2 - lat1) != 0 and (lon2 - lon1) != 0:
#                         interpolated_value = bilinear_interpolation(lon_data, lat_data, lon1, lat1, f11, lon2, lat2, f22, f12, f21)
#                         interpolated_value = round(interpolated_value, 3)
#                         print(interpolated_value)
#                         return render(request, 'index.html', {
#                             'average_value': interpolated_value,
#                             'lat_data': lat_data,
#                             'lon_data': lon_data
#                         })
#                     else:
#                         # Fallback to linear interpolation
#                         return linear_interpolation(lat_data, lon_data)
#                 else:
#                     # Fallback to linear interpolation if all points for bilinear are not found
#                     return linear_interpolation(lat_data, lon_data)
#         elif latmin and latmax and lonmin and lonmax:
#             latmin = float(latmin)
#             latmax = float(latmax)
#             lonmin = float(lonmin)
#             lonmax = float(lonmax)
#             row_step = 0.08333333
#             col_step = 0.08333333
#             points_in_range = GridPoint.objects.filter(
#                 latitude__gte=latmin,
#                 latitude__lte=latmax,
#                 longitude__gte=lonmin,
#                 longitude__lte=lonmax
#             ).order_by('latitude', 'longitude')
#             if points_in_range.exists():
#                 # Prepare the data
#                 output = []
#                 output.append(f"{latmin:.6f}   {latmax:.6f}   {lonmin:.6f}   {lonmax:.6f}   {row_step:.8f}   {col_step:.8f}")
#                 # Create a 2D grid list
#                 latitudes = sorted(set(p.latitude for p in points_in_range))
#                 longitudes = sorted(set(p.longitude for p in points_in_range))
#                 grid = [[None] * len(longitudes) for _ in range(len(latitudes))]
#                 for point in points_in_range:
#                     lat_idx = latitudes.index(float(point.latitude))
#                     lon_idx = longitudes.index(float(point.longitude))
#                     grid[lat_idx][lon_idx] = f"{float(point.value):.3f}"
#                 # Append the grid data
#                 for row in grid:
#                     output.append("   ".join(val if val is not None else "NaN" for val in row))

#                 # Create the HTTP response with .gri data
#                 response = HttpResponse("\n".join(output), content_type='text/plain')
#                 response['Content-Disposition'] = 'attachment; filename="grid_data.gri"'
#                 return response
#             else:
#                 return render(request, 'index.html', {'error_message': 'No points found within the specified range.'})
#         elif 'csv_file' in request.FILES:
#             csv_file = request.FILES['csv_file']
#             csv_data = TextIOWrapper(csv_file, encoding=request.encoding)
#             reader = csv.DictReader(csv_data)
#             points_data = []
#             for row in reader:
#                 if row['lat'].strip() and row['lon'].strip():  
#                     lat_data = float(row['lat'].strip())
#                     lon_data = float(row['lon'].strip())
#                     try:
#                         exact_point = GridPoint.objects.get(latitude=lat_data, longitude=lon_data)
#                         exact_point_dict = {
#                             'latitude': exact_point.latitude,
#                             'longitude': exact_point.longitude,
#                             'value': exact_point.value
#                         }
#                         points_data.append({'latitude': lat_data, 'longitude': lon_data, 'exact_point': exact_point_dict})
#                     except GridPoint.DoesNotExist:
#                         # Get surrounding points for bilinear interpolation
#                         p1 = GridPoint.objects.filter(latitude__lte=lat_data, longitude__lte=lon_data).order_by('-latitude', '-longitude').first()
#                         p2 = GridPoint.objects.filter(latitude__lte=lat_data, longitude__gte=lon_data).order_by('-latitude', 'longitude').first()
#                         p3 = GridPoint.objects.filter(latitude__gte=lat_data, longitude__lte=lon_data).order_by('latitude', '-longitude').first()
#                         p4 = GridPoint.objects.filter(latitude__gte=lat_data, longitude__gte=lon_data).order_by('latitude', 'longitude').first()

#                         if p1 and p2 and p3 and p4:
#                             lat1, lon1, f11 = float(p1.latitude), float(p1.longitude), float(p1.value)
#                             lat2, lon2, f22 = float(p4.latitude), float(p4.longitude), float(p4.value)
#                             f12 = float(p2.value)
#                             f21 = float(p3.value)

#                             # Bilinear interpolation if possible
#                             if (lat2 - lat1) != 0 and (lon2 - lon1) != 0:
#                                 interpolated_value = bilinear_interpolation(lon_data, lat_data, lon1, lat1, f11, lon2, lat2, f22, f12, f21)
#                                 interpolated_value = round(interpolated_value, 3)
#                                 print('bilinear',interpolated_value)
#                                 points_data.append({'latitude': lat_data, 'longitude': lon_data, 'average_value': interpolated_value})
#                             else:
#                                 # Fall back to linear interpolation
#                                 linear_result = linear_interpolation(lat_data, lon_data)
#                                 print('linear',linear_result)
#                                 points_data.append({'latitude': lat_data, 'longitude': lon_data, 'average_value': linear_result})
#                         else:
#                             # If not enough points for bilinear interpolation, try linear
#                             linear_result = linear_interpolation(lat_data, lon_data)
#                             print('linear_result',linear_result)
#                             points_data.append({'latitude': lat_data, 'longitude': lon_data, 'average_value': linear_result})
#                 else:
#                     points_data.append({'latitude': None, 'longitude': None, 'error_message': 'Latitude or longitude is missing or empty in the CSV row.'})

#             # Save points_data in session
#             request.session['points_data'] = points_data
#             return render(request, 'index.html', {'points_data': points_data})

#         else:
#             return render(request, 'index.html', {'error_message': 'Please provide latitude and longitude or upload a CSV file.'})
#     return render(request, 'index.html')

# def home(request):
#     if request.method == 'POST':
#         lat_data = request.POST.get('lat')
#         lon_data = request.POST.get('lon')
#         latmin = request.POST.get('latmin')
#         latmax = request.POST.get('latmax')
#         lonmin = request.POST.get('lonmin')
#         lonmax = request.POST.get('lonmax')

#         if lat_data and lon_data:
#             lat_data = float(lat_data)
#             lon_data = float(lon_data)
#             try:
#                 exact_point = GridPoint.objects.get(latitude=lat_data, longitude=lon_data)
#                 return render(request, 'index.html', {'exact_point': exact_point})
#             except GridPoint.DoesNotExist:
#                 nearest_points = GridPoint.objects.filter(
#                     latitude__gte=lat_data-0.04166, 
#                     latitude__lte=lat_data+0.04166, 
#                     longitude__gte=lon_data-0.04166, 
#                     longitude__lte=lon_data+0.04166
#                 )
#                 if nearest_points.exists():
#                     average_value = round(nearest_points.aggregate(Avg('value'))['value__avg'], 3)
#                     return render(request, 'index.html', {'average_value': average_value,'lat_data':lat_data,'lon_data':lon_data})
#                 else:
#                     return render(request, 'index.html', {'error_message': 'No points found near the provided latitude and longitude.'})
        
#         elif latmin and latmax and lonmin and lonmax:
#             latmin = float(latmin)
#             latmax = float(latmax)
#             lonmin = float(lonmin)
#             lonmax = float(lonmax)
#             row_step = 0.08333333
#             col_step = 0.08333333

#             points_in_range = GridPoint.objects.filter(
#                 latitude__gte=latmin,
#                 latitude__lte=latmax,
#                 longitude__gte=lonmin,
#                 longitude__lte=lonmax
#             ).order_by('latitude', 'longitude')

#             if points_in_range.exists():
#                 # Prepare the data
#                 output = []
#                 output.append(f"{latmin:.6f}   {latmax:.6f}   {lonmin:.6f}   {lonmax:.6f}   {row_step:.8f}   {col_step:.8f}")

#                 # Create a 2D grid list
#                 latitudes = sorted(set(p.latitude for p in points_in_range))
#                 longitudes = sorted(set(p.longitude for p in points_in_range))
#                 grid = [[None] * len(longitudes) for _ in range(len(latitudes))]

#                 for point in points_in_range:
#                     lat_idx = latitudes.index(float(point.latitude))
#                     lon_idx = longitudes.index(float(point.longitude))
#                     grid[lat_idx][lon_idx] = f"{float(point.value):.3f}"

#                 # Append the grid data
#                 for row in grid:
#                     output.append("   ".join(val if val is not None else "NaN" for val in row))

#                 # Create the HTTP response with .gri data
#                 response = HttpResponse("\n".join(output), content_type='text/plain')
#                 response['Content-Disposition'] = 'attachment; filename="grid_data.gri"'
#                 return response

#             else:
#                 return render(request, 'index.html', {'error_message': 'No points found within the specified range.'})
        
#         elif 'csv_file' in request.FILES:
#             csv_file = request.FILES['csv_file']
#             csv_data = TextIOWrapper(csv_file, encoding=request.encoding)
#             reader = csv.DictReader(csv_data)
#             points_data = []
#             for row in reader:
#                 if row['lat'].strip() and row['lon'].strip():  
#                     lat_data = float(row['lat'].strip())
#                     lon_data = float(row['lon'].strip())
#                     try:
#                         exact_point = GridPoint.objects.get(latitude=lat_data, longitude=lon_data)
#                         exact_point_dict = {
#                             'latitude': exact_point.latitude,
#                             'longitude': exact_point.longitude,
#                             'value': exact_point.value  # Assuming 'value' is an attribute of GridPoint
#                         }
#                         points_data.append({'latitude': lat_data, 'longitude': lon_data, 'exact_point': exact_point_dict})
#                     except GridPoint.DoesNotExist:
#                         nearest_points = GridPoint.objects.filter(
#                             latitude__gte=lat_data-0.04166, 
#                             latitude__lte=lat_data+0.04166, 
#                             longitude__gte=lon_data-0.04166, 
#                             longitude__lte=lon_data+0.04166
#                         )
#                         if nearest_points.exists():
#                             average_value = round(nearest_points.aggregate(Avg('value'))['value__avg'], 3)
#                             points_data.append({'latitude': lat_data, 'longitude': lon_data, 'average_value': average_value})
#                         else:
#                             points_data.append({'latitude': lat_data, 'longitude': lon_data, 'error_message': 'No points found near the provided latitude and longitude.'})
#                 else:
#                     points_data.append({'latitude': None, 'longitude': None, 'error_message': 'Latitude or longitude is missing or empty in the CSV row.'})
            
#             # Save points_data in session
#             request.session['points_data'] = points_data
#             return render(request, 'index.html', {'points_data': points_data})
#         else:
#             return render(request, 'index.html', {'error_message': 'Please provide latitude and longitude or upload a CSV file.'})
    
#     return render(request, 'index.html')

# from django.shortcuts import render
# from django.db.models import Avg
# from .models import GridPoint
# import math



# def home(request):
#     if request.method == 'POST':
#         lat_data = request.POST.get('lat')
#         lon_data = request.POST.get('lon')

#         if lat_data and lon_data:
#             lat_data = float(lat_data)
#             lon_data = float(lon_data)

#             # Find the four surrounding points for bilinear interpolation
#             p1 = GridPoint.objects.filter(latitude__lte=lat_data, longitude__lte=lon_data).order_by('-latitude', '-longitude').first()
#             p2 = GridPoint.objects.filter(latitude__lte=lat_data, longitude__gte=lon_data).order_by('-latitude', 'longitude').first()
#             p3 = GridPoint.objects.filter(latitude__gte=lat_data, longitude__lte=lon_data).order_by('latitude', '-longitude').first()
#             p4 = GridPoint.objects.filter(latitude__gte=lat_data, longitude__gte=lon_data).order_by('latitude', 'longitude').first()

#             # Check if bilinear interpolation is possible
#             if p1 and p2 and p3 and p4:
#                 lat1, lon1, f11 = float(p1.latitude), float(p1.longitude), float(p1.value)
#                 lat2, lon2, f22 = float(p4.latitude), float(p4.longitude), float(p4.value)
#                 f12 = float(p2.value)
#                 f21 = float(p3.value)

#                 # Bilinear interpolation only if the latitudes and longitudes are not too close
#                 if (lat2 - lat1) != 0 and (lon2 - lon1) != 0:
#                     interpolated_value = bilinear_interpolation(lon_data, lat_data, lon1, lat1, f11, lon2, lat2, f22, f12, f21)
#                     interpolated_value = round(interpolated_value, 3)
#                     print(interpolated_value)
#                     return render(request, 'index.html', {
#                         'interpolated_value': interpolated_value,
#                         'lat_data': lat_data,
#                         'lon_data': lon_data
#                     })
#                 else:
#                     # Fallback to linear interpolation
#                     return linear_interpolation(lat_data, lon_data)
#             else:
#                 # Fallback to linear interpolation if all points for bilinear are not found
#                 return linear_interpolation(lat_data, lon_data)

#         else:
#             return render(request, 'index.html', {'error_message': 'Please provide latitude and longitude.'})

#     return render(request, 'index.html')





def download_points(request):
    points_data = request.GET.get('points_data')
    if points_data:
        response = HttpResponse(points_data, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="points_data.txt"'
        return response
    else:
        return HttpResponse("No data available for download.")


def download_processed_csv(request):
    if 'points_data' in request.session:
        points_data = request.session['points_data']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="processed_data.csv"'
        writer = csv.writer(response)
        writer.writerow(['Latitude', 'Longitude', 'E Hight' ,'N Value', 'Orthometric Hight', 'Error Message'])
        for data in points_data:
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            e_hight= data.get('e_hight')
            n_value = data.get('n_value')  
            adjusted_value = data.get('adjusted_value') 
            error_message = data.get('error_message')  
            writer.writerow([
                latitude,
                longitude,
                e_hight,
                n_value if n_value is not None else '',
                adjusted_value if adjusted_value is not None else '',
                error_message if error_message else ''
            ])
        
        return response
    return HttpResponse("No processed data available.", status=404)
    


    # longitude__lte=lon_data+0.04166
@login_required(login_url='/')
def geoid_dashboard(request):
    return render(request,'index.html')


@login_required(login_url='/')
def geoid_valuefind(request):
    date = datetime.now()
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    username = user.username
    usertype = user.user_types
    option = request.GET.get('option', 'single')
    if request.method == 'POST':
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            csv_data = TextIOWrapper(csv_file, encoding=request.encoding)
            reader = csv.DictReader(csv_data)
            points_data = []
            point_count = 0
            request.session['points_data'] = points_data  

            for row in reader:
                if row['lat'].strip() and row['lon'].strip():
                    try:
                        lat_data = float(row['lat'].strip())
                        lon_data = float(row['lon'].strip())
                        h_data = float(row['Ellipsoidal_Height'].strip()) if 'Ellipsoidal_Height' in row and row['Ellipsoidal_Height'].strip() else None  # Check if 'h_height' key exists
                    except ValueError:
                        points_data.append({
                            'latitude': row.get('lat'),
                            'longitude': row.get('lon'),
                            'H_HIGHT': row.get('Ellipsoidal_Height'),
                            'error_message': 'Latitude or longitude is not a valid number.'
                        })
                        continue

                    shapefile_path = 'C:\inetpub\wwwroot\geocalculation\India_Shapefile\Territorial Boundaries.shp'  
                    shp_data = gpd.read_file(shapefile_path)
                    user_point = Point(lon_data, lat_data)
                    matched_shape = shp_data[shp_data.geometry.apply(lambda geom: geom.contains(user_point))]

                    if not matched_shape.empty:
                        state_name = matched_shape.iloc[0]['STATE']
                        try:
                            exact_point = GridPoint.objects.get(latitude=lat_data, longitude=lon_data, state=state_name)
                            exact_point_value = float(exact_point.value)

                            point_entry = {
                                'latitude': lat_data,
                                'longitude': lon_data,
                                'n_value': exact_point_value,
                                'e_hight': h_data
                            }
                            if h_data is not None:
                                point_entry['adjusted_value'] = h_data - exact_point_value

                            points_data.append(point_entry)
                            point_count += 1
                        except GridPoint.DoesNotExist:
                            nearest_points = GridPoint.objects.filter(
                                state=state_name,
                                latitude__gte=lat_data - 1/24, 
                                latitude__lte=lat_data + 1/24, 
                                longitude__gte=lon_data - 1/24, 
                                longitude__lte=lon_data + 1/24
                            ).values()

                            if nearest_points.exists():
                                average_value = float(round(nearest_points.aggregate(Avg('value'))['value__avg'], 3))

                                point_entry = {
                                    'latitude': lat_data,
                                    'longitude': lon_data,
                                    'n_value': average_value,
                                    'e_hight': h_data
                                }

                                # Add adjusted value only if h_data is provided
                                if h_data is not None:
                                    point_entry['adjusted_value'] = h_data - average_value

                                points_data.append(point_entry)
                                point_count += 1 
                            else:
                                points_data.append({
                                    'latitude': lat_data,
                                    'longitude': lon_data,
                                    'error_message': 'No Undulation value (N-value) found near the provided latitude and longitude.'
                                })
                    else:
                        points_data.append({
                            'latitude': lat_data,
                            'longitude': lon_data,
                            'error_message': 'Coordinate entered lies outside the territorial boundary of India'
                        })

                else:
                    points_data.append({
                        'latitude': None,
                        'longitude': None,
                        'error_message': 'Latitude or longitude is missing or empty in the CSV row.'
                    })
            databackup.objects.create(
                username=username,
                user_type=usertype,
                pointdownload=str(point_count),  # Save the count as a string
                updatetime=date
            )        

            return render(request, 'shownvalue.html', {'points_data': points_data, 'option': option})

        # Handling direct POST request for lat/lon input
        lat_data = request.POST.get('lat')
        lon_data = request.POST.get('lon')
        Ellipsoidal_Height = request.POST.get('Ellipsoidal_Height')

        if lat_data and lon_data:
            try:
                lat_data = float(lat_data)
                lon_data = float(lon_data)
                Ellipsoidal_Height = float(Ellipsoidal_Height) if Ellipsoidal_Height else None
            except ValueError:
                return render(request, 'index.html', {'error': 'Latitude or longitude must be a number.', 'option': option})

            shapefile_path = 'C:\inetpub\wwwroot\geocalculation\India_Shapefile\Territorial Boundaries.shp'
            shp_data = gpd.read_file(shapefile_path)
            user_point = Point(lon_data, lat_data)
            matched_shape = shp_data[shp_data.geometry.apply(lambda geom: geom.contains(user_point))]
            print(matched_shape)
            if not matched_shape.empty:
                state_name = matched_shape.iloc[0]['STATE']
                try:
                    grid_point = GridPoint.objects.get(state=state_name, latitude=lat_data, longitude=lon_data)
                    points_data = []
                    point_count = 0
                    request.session['points_data'] = points_data
                    grid_point_value = float(grid_point.value)

                    point_entry = {
                        'latitude': grid_point.latitude,
                        'longitude': grid_point.longitude,
                        'n_value': grid_point_value,
                        'e_hight': Ellipsoidal_Height
                        
                    }
                    
                    # Add adjusted value only if h_height is provided
                    if Ellipsoidal_Height is not None:
                        point_entry['adjusted_value'] = Ellipsoidal_Height - grid_point_value

                    points_data.append(point_entry)
                    point_count += 1
                    databackup.objects.create(
                        username=username,
                        user_type=usertype,
                        pointdownload=str(point_count),  # Save the count as a string
                        updatetime=date
                    )  
                    return render(request, 'shownvalue.html', {'points_data': points_data, 'option': option})

                except GridPoint.DoesNotExist:
                    nearest_points = GridPoint.objects.filter(
                        state=state_name,
                        latitude__gte=lat_data - 1/24, 
                        latitude__lte=lat_data + 1/24, 
                        longitude__gte=lon_data - 1/24, 
                        longitude__lte=lon_data + 1/24
                    ).values()
                    print(nearest_points)
                    points_data = []
                    point_count = 0
                    request.session['points_data'] = points_data
                    if nearest_points.exists():
                        average_value = float(round(nearest_points.aggregate(Avg('value'))['value__avg'], 3))

                        point_entry = {
                            'latitude': lat_data,
                            'longitude': lon_data,
                            'n_value': average_value,
                            'e_hight': Ellipsoidal_Height
                        }
                        if Ellipsoidal_Height is not None:
                            point_entry['adjusted_value'] = Ellipsoidal_Height - average_value

                        points_data.append(point_entry)
                        point_count += 1
                    else:
                        points_data.append({
                            'latitude': lat_data,
                            'longitude': lon_data,
                            'error_message': 'No Undulation value (N-value) found near the provided latitude and longitude.'
                        })
                    databackup.objects.create(
                        username=username,
                        user_type=usertype,
                        pointdownload=str(point_count),  # Save the count as a string
                        updatetime=date
                    )      

                    return render(request, 'shownvalue.html', {'points_data': points_data, 'option': option})
                
            else:
                return render(request, 'shownvalue.html', {'error_message': 'Coordinate entered lies outside the territorial boundary of India', 'option': option})
         
    return render(request, 'shownvalue.html', {'option': option})












# from django.shortcuts import render
# from django.db.models import Avg
# from django.utils.encoding import TextIOWrapper
# from osgeo import ogr  # GDAL for shapefile handling
# from .models import GridPoint
# from shapely.geometry import Point  # Shapely for point creation
# import csv

# def geoid_dashboard(request):
#     shapefile_path = 'D:\\python_project\\PYTHON_project\\geocalculation\\India_Shapefile\\Territorial Boundaries.shp'  
#     shapefile = ogr.Open(shapefile_path)
#     layer = shapefile.GetLayer()  # Access layer data
    
#     def get_state_from_shapefile(lon, lat):
#         point = ogr.Geometry(ogr.wkbPoint)
#         point.AddPoint(lon, lat)
        
#         for feature in layer:
#             if feature.GetGeometryRef().Contains(point):
#                 return feature.GetField("STATE")  # Adjust "STATE" to the correct field name
#         return None
    
#     if request.method == 'POST':
#         points_data = []
#         request.session['points_data'] = points_data
        
#         if 'csv_file' in request.FILES:
#             csv_file = request.FILES['csv_file']
#             csv_data = TextIOWrapper(csv_file, encoding=request.encoding)
#             reader = csv.DictReader(csv_data)
            
#             for row in reader:
#                 lat_str = row['lat'].strip()
#                 lon_str = row['lon'].strip()
                
#                 if lat_str and lon_str:
#                     lat_data = float(lat_str)
#                     lon_data = float(lon_str)
#                     state_name = get_state_from_shapefile(lon_data, lat_data)
                    
#                     if state_name:
#                         try:
#                             exact_point = GridPoint.objects.get(latitude=lat_data, longitude=lon_data, state=state_name)
#                             points_data.append({
#                                 'latitude': lat_data,
#                                 'longitude': lon_data,
#                                 'exact_point': {
#                                     'latitude': exact_point.latitude,
#                                     'longitude': exact_point.longitude,
#                                     'value': exact_point.value
#                                 }
#                             })
#                         except GridPoint.DoesNotExist:
#                             nearest_points = GridPoint.objects.filter(
#                                 state=state_name,
#                                 latitude__gte=lat_data - 0.04166,
#                                 latitude__lte=lat_data + 0.04166,
#                                 longitude__gte=lon_data - 0.04166,
#                                 longitude__lte=lon_data + 0.04166
#                             ).values()
                            
#                             if nearest_points.exists():
#                                 average_value = round(nearest_points.aggregate(Avg('value'))['value__avg'], 3)
#                                 points_data.append({
#                                     'latitude': lat_data,
#                                     'longitude': lon_data,
#                                     'average_value': average_value
#                                 })
#                             else:
#                                 points_data.append({
#                                     'latitude': lat_data,
#                                     'longitude': lon_data,
#                                     'error_message': 'No points found near the provided latitude and longitude.'
#                                 })
#                     else:
#                         points_data.append({
#                             'latitude': lat_data,
#                             'longitude': lon_data,
#                             'error_message': 'No matching state found for the provided latitude and longitude.'
#                         })
#                 else:
#                     points_data.append({
#                         'latitude': None,
#                         'longitude': None,
#                         'error_message': 'Latitude or longitude is missing or empty in the CSV row.'
#                     })

#             return render(request, 'index.html', {'points_data': points_data})

#         # Single point handling for latitude and longitude provided in POST data
#         lat_data = request.POST.get('lat')
#         lon_data = request.POST.get('lon')
        
#         if lat_data and lon_data:
#             lat_data = float(lat_data)
#             lon_data = float(lon_data)
#             state_name = get_state_from_shapefile(lon_data, lat_data)
            
#             if state_name:
#                 try:
#                     grid_point = GridPoint.objects.get(state=state_name, latitude=lat_data, longitude=lon_data)
#                     return render(request, 'index.html', {'exact_point': grid_point})
#                 except GridPoint.DoesNotExist:
#                     nearest_points = GridPoint.objects.filter(
#                         state=state_name,
#                         latitude__gte=lat_data - 0.04166,
#                         latitude__lte=lat_data + 0.04166,
#                         longitude__gte=lon_data - 0.04166,
#                         longitude__lte=lon_data + 0.04166
#                     ).values()
                    
#                     if nearest_points.exists():
#                         average_value = round(nearest_points.aggregate(Avg('value'))['value__avg'], 3)
#                         points_data.append({
#                             'latitude': lat_data,
#                             'longitude': lon_data,
#                             'average_value': average_value
#                         })
#                     else:
#                         points_data.append({
#                             'latitude': lat_data,
#                             'longitude': lon_data,
#                             'error_message': 'No points found near the provided latitude and longitude.'
#                         })
                    
#                     return render(request, 'index.html', {'points_data': points_data})
#             else:
#                 return render(request, 'index.html', {'error_message': 'No matching state found for the provided latitude and longitude.'})

#     return render(request, 'index.html')
