from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, QueryDict
from django.contrib import messages
from firebase_admin import credentials, auth
import firebase_admin
from firebase_admin import firestore
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyBR_JvPP2Fn731M7sV80a7KtWFTotrhm8g",
  "authDomain": "rentappartment-8c422.firebaseapp.com",
  "databaseURL": "https://rentappartment-8c422-default-rtdb.firebaseio.com",
  "projectId": "rentappartment-8c422",
  "storageBucket": "rentappartment-8c422.appspot.com",
  "messagingSenderId": "18500195576",
  "appId": "1:18500195576:web:136e5c01fd510b8246d70d",
  "measurementId": "G-HD380NWNZ7"
}


firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth1 = firebase.auth()

def Home(request):
    try:
        # Initialize Firestore client
        db = firestore.client()

        # Get all products data
        app_ref = db.collection('Appartments')
        app_data = app_ref.get()

        # Check if products_data is not None
        if app_data:
            # Convert the data to a list of dictionaries
            appatArray = []
            for appat in app_data:
                product_data = appat.to_dict()
                apt_Id = appat.id
                # Access image_urls as a list
                image_urls = product_data.get('image_urls', [])
                # Take only the first image URL if available
                # Access image_urls as a list
                #image_url = product_data.get('image_urls')
                image_url = image_urls[0] if image_urls else None
    
                
                appat_dict = {
                    'aptName': product_data.get('aptName', ''),
                    'aptPrice': product_data.get('aptPrice', ''),
                    'image_url': image_url,  # Take only the first image URL
                    'description': product_data.get('description', ''),
                    'phoneNo': product_data.get('phoneNo', ''),
                    'region': product_data.get('region', ''),
                    'streetName': product_data.get('streetName', ''),
                    'user_uid': product_data.get('user_uid', ''),
                    'username': product_data.get('username', ''),
                    'email': product_data.get('email', ''),
                    'apt_Id': apt_Id
                    # Add other product fields as needed
                }
                appatArray.append(appat_dict)

                print(f"ProdArray: {appatArray}")

            return render(request, "startuppage.html", {'appatArray': appatArray})
        else:
            # Handle case where no products are found
            return render(request, "startuppage.html", {'appatArray': []})

    except Exception as e:
        # Handle any exceptions that occur during data retrieval
        print(f"Error fetching products Benezeth: {e}")
        return render(request, "startuppage.html", {'appatArray': []})
    

def Test(request):
    return render(request, 'temp.html')    


def MainpageSignedIn(request, user_uid, username):

    try:
        # Initialize Firestore client
        db = firestore.client()

        # Get all products data
        app_ref = db.collection('Appartments')
        app_data = app_ref.get()

        # Check if products_data is not None
        if app_data:
            # Convert the data to a list of dictionaries
            appatArray = []
            for appat in app_data:
                product_data = appat.to_dict()
                apt_Id = appat.id
                # Access image_urls as a list
                image_urls = product_data.get('image_urls', [])
                # Take only the first image URL if available
                # Access image_urls as a list
                #image_url = product_data.get('image_urls')
                image_url = image_urls[0] if image_urls else None
    
                
                appat_dict = {
                    'aptName': product_data.get('aptName', ''),
                    'aptPrice': product_data.get('aptPrice', ''),
                    'image_url': image_url,  # Take only the first image URL
                    'description': product_data.get('description', ''),
                    'phoneNo': product_data.get('phoneNo', ''),
                    'region': product_data.get('region', ''),
                    'streetName': product_data.get('streetName', ''),
                    'user_uid': product_data.get('user_uid', ''),
                    'username': product_data.get('username', ''),
                    'email': product_data.get('email', ''),
                    'apt_Id': apt_Id
                    # Add other product fields as needed
                }
                appatArray.append(appat_dict)

                print(f"ProdArray: {appatArray}")

            return render(request, "homesignedin.html", {'user_uid': user_uid, 'username': username, 'appatArray': appatArray})
        else:
            # Handle case where no products are found
            return render(request, "homesignedin.html", {'user_uid': user_uid, 'username': username, 'appatArray': []})

    except Exception as e:
        # Handle any exceptions that occur during data retrieval
        print(f"Error fetching products Benezeth: {e}")
        return render(request, "homesignedin.html", {'user_uid': user_uid, 'username': username, 'appatArray': []})

def listPropety(request):
    return render(request, 'list_property.html')

def GoToLogIn(request):
    return render(request, 'login.html')

def GoToRegister(request):
    return render(request, 'register.html')


def LogInSubmit(request):
    if request.method == 'POST':
       email = request.POST.get('email')
       password = request.POST.get('password')
       
           #Sign in using firebase authentication
       
               
       user = auth1.sign_in_with_email_and_password(email, password)
       #user_uid = auth1.current_user
       user_uid = user['localId']
       #username = user['username']
       
       # Retrieve the username from Firestore using the UID
       db = firestore.client()
       user_doc = db.collection('UserDetails').document(user_uid).get()
       
       if user_doc.exists:
          username = user_doc.to_dict().get('username')
       else:
          username = "Unknown"  # Default username if not found
            
       
       #print(f"User UID: {user_uid}")
       print(f"User UID: {user_uid}")
       print(f"username: {username}")
         # Redirect the user to the welcome page along with username and user UID
       return redirect('mainpage', user_uid=user_uid, username=username)
     
    else:
        return render(request, 'login.html')
    

    #return render(request, 'homesignedin.html')


def RegisterSubmit(request):
     # Retrieve form data
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        # Check if email already exists
        if is_email_exists(email):
            # Email already exists, handle the error (e.g., show error message to the user)
            return HttpResponse("Email already exists")
    
        # Authenticate user using Firebase
        user = auth.create_user(email=email, password=password) 
        
        # Get the UID of the newly created user
        user_id = user.uid       
        # Save user data to Firestore
        db = firestore.client()
        user_ref = db.collection('UserDetails').document(user_id)
        user_ref.set({
            'username': username,
            'email': email,
            'password': password,
            'user_id':user_id
            # Add additional user data as needed
        })
        
        return redirect('register_submit')
       
    else:
        return render(request, 'register.html') 


def is_email_exists(email):
    # Check if email exists using Firebase Authentication
    try:
        auth.get_user_by_email(email)
        return True  # Email exists
    except firebase_admin.auth.UserNotFoundError:
        return False  # Email doesn't exist
    

def GoToPost(request, user_uid, username):
    return redirect(reverse('homepost', kwargs={'user_uid': user_uid, 'username': username}))

def GoToDetailsAppartment(request, user_uid, username, apt_Id):

    db = firestore.client()

        # Get the product data to find the seller_uid
    appt_ref = db.collection('Appartments').where('apt_Id', '==', apt_Id)
    apt_data = appt_ref.get()

    # Get all Appartments data by user uid
    apt_refUID = db.collection('Appartments').where('user_uid', '==', user_uid)
    apt_dataUID = apt_refUID.get()

    if apt_data:
            for appart in apt_data:
                appt_info = appart.to_dict()
                seller_uid = appt_info.get('user_uid', '')
                break  # Assuming prod_id is unique, so we can exit the loop after finding the product

    appartArray = []
    for apt in apt_data:
            appart_data = apt.to_dict()
            product_id = apt.id
            # Access image_urls as a list and filter out empty strings
            image_urls = appart_data.get('image_urls', [])
            filtered_images = []
        
            for image in image_urls:
               if image == "":
                  break
               filtered_images.append(image)


            # Get house features and stop if empty string is encountered
            house_features = appart_data.get('houeseFeatures', [])
            filtered_features = []
        
            for feature in house_features:
                if feature == "":
                   break
                filtered_features.append(feature)

    print(f"Images {filtered_images}")
                
    apt_dict = {
        'aptName': appart_data.get('aptName', ''),
        'aptPrice': appart_data.get('aptPrice', ''),
        'image_url': filtered_images,  # Take only the first image URL
        'description': appart_data.get('description', ''),
        'houeseFeatures': filtered_features,
        'phoneNo': appart_data.get('phoneNo', ''),
        'region': appart_data.get('region', ''),
        'streetName': appart_data.get('streetName', ''),
        'user_uid': appart_data.get('user_uid', ''),
        'username': appart_data.get('username', ''),
        'email': appart_data.get('email', ''),
        'apt_Id': apt_Id
                    # Add other product fields as needed
                }
    appartArray.append(apt_dict)

    print(f"Features: {filtered_features}")
                
    print(appartArray)

    aptArrayAll = []
    if apt_dataUID:
        
        for apt in apt_dataUID:
            apt_data_data = apt.to_dict()
            apt_ID = apt.id
            # Access image_urls as a list
            image_all = apt_data_data.get('image_urls')
            first_image = image_all[0] if image_all else None
                        
            apt_dictAll = {
                'aptName': apt_data_data.get('aptName', ''),
        'aptPrice': apt_data_data.get('aptPrice', ''),
        'image_url': first_image,  # Take only the first image URL
        'description': apt_data_data.get('description', ''),
        'phoneNo': apt_data_data.get('phoneNo', ''),
        'region': apt_data_data.get('region', ''),
        'streetName': apt_data_data.get('streetName', ''),
        'user_uid': apt_data_data.get('user_uid', ''),
        'username': apt_data_data.get('username', ''),
        'email': apt_data_data.get('email', ''),
        'apt_Id': apt_ID
                    # Add other product fields as needed
                }
                        
            aptArrayAll.append(apt_dictAll) 
            print(f"all: {aptArrayAll}")       

    
    return render(request, 'details.html', {'user_uid': user_uid, 'username': username, 'apt_Id': apt_Id, 'appartArray': appartArray, 'aptArrayAll': aptArrayAll})