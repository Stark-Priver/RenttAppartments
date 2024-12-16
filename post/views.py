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
store = firebase.storage()

def HomePost(request, user_uid, username):
    return render(request, 'post.html', {'user_uid':user_uid, 'username':username})


def PostProducts(request, user_uid, username):
    if request.method == 'POST':

         # Authenticate the user
        
            # Assuming the user is authenticated and you have a valid token
        aptName = request.POST.get('aptName')    
        aptPrice = request.POST.get('aptPrice')
        phoneNo = request.POST.get('number')
        region = request.POST.get('region')
        streetName = request.POST.get('streetname')
        description = request.POST.get('description')
        # Get the selected checkboxes
        selected_features = request.POST.getlist('features')
        
        # Flatten the features list
        features = selected_features

        image_urls = []
        for image_file in request.FILES.getlist('images[]'):
            file_path = f"images/{user_uid}/{image_file.name}"
            image_url = upload_image_to_storage(image_file, file_path)
            if image_url:
                image_urls.append(image_url)
                print(f"Array: {image_urls}")
            
            else:
                print(f"Failed to upload image: {image_file.name}")

        while len(features) < 30:
            features.append("")
        # Ensure the array has exactly 9 items by filling with empty strings
        while len(image_urls) < 9:
            image_urls.append("")        

        print(f"Collected image URLs: {image_urls}")
    
        # Save user data and image URLs to Firestore
        try:
            db = firestore.client()
            
            user_ref = db.collection('UserDetails').document(user_uid)
            user_doc = user_ref.get()
            
            # Check if the user document exists
            if user_doc.exists:
                # Retrieve the email field from the user document
                user_data = user_doc.to_dict()
                email = user_data.get('email')
                if email:
                   # Email found, use it as needed
                   print("Email:", email)
                   
                   apt_Id = db.collection('Appartments').document().id
                   user_ref = db.collection('Appartments').document(apt_Id)
                   user_ref.set({
                       'aptName': aptName,
                      'image_urls': image_urls,
                      'houeseFeatures': features,
                      'aptPrice': aptPrice,
                      'phoneNo': phoneNo,
                      'streetName': streetName,
                      'region': region,
                      'description': description,
                      'user_uid': user_uid,
                      'username': username,
                      'apt_Id': apt_Id,
                      'email': email
                    })
                
                   return redirect('homepost', user_uid=user_uid, username=username) 

                else:
                   print("Email not found for user_uid:", user_uid)
                   
            else:
               print("User document not found for user_uid:", user_uid)
        except Exception as e:
            # Handle Firestore update error
            print(f"Firestore error: {e}")
            return  HttpResponse("Failed to post product. Please try again later.", status=500)
        
    else:
        print(f"no post")
        return render(request, 'post.html', {'user_uid': user_uid, 'username': username})
    
   
    
def Dashboard(request, user_uid, username):
    print(f"UID: {user_uid}")
    print(f"NAME: {username}")
    
    # Print user_uid and username
    print(f"User UID: {user_uid}")
    print(f"Username: {username}")
    
    try:
        # Initialize Firestore client
        db = firestore.client()

        # Get all products data
        products_ref = db.collection('Appartments').where('user_uid', '==', user_uid)
        products_data = products_ref.get()

        # Check if products_data is not None
        if products_data:
            # Convert the data to a list of dictionaries
            productsArray = []
            for product in products_data:
                product_data = product.to_dict()
                product_id = product.id
                # Access image_urls as a list
                image_url = product_data.get('image_urls')
                # Take only the first image URL if available
                first_image = image_url[0] if image_url else None
                
                print(f"Index: {image_url}")
                
                product_dict = {
                    'aptName': product_data.get('aptName', ''),
                    'aptPrice': product_data.get('aptPrice', ''),
                    'image_url': first_image,  # Take only the first image URL
                    'houeseFeatures': product_data.get('houeseFeatures', ''),
                    'description': product_data.get('description', ''),
                    'phoneNo': product_data.get('phoneNo', ''),
                    'region': product_data.get('region', ''),
                    'streetName': product_data.get('streetName', ''),
                    'user_uid': product_data.get('user_uid', ''),
                    'username': product_data.get('username', ''),
                    'product_id': product_id
                    # Add other product fields as needed
                }
                productsArray.append(product_dict)

            return render(request, "mypost.html", {'productsArray': productsArray, 'user_uid': user_uid, 'username': username})
        else:
            # Handle case where no products are foundnhgj
            return render(request, "mypost.html", {'productsArray': [], 'user_uid': user_uid, 'username': username})

    except Exception as e:
        # Handle any exceptions that occur during data retrieval
        print(f"Error fetching products: {e}")
        return render(request, "mypost.html", {'productsArray': [], 'user_uid': user_uid, 'username': username})
     

def Edit(request, user_uid, username, apt_Id):

    print(f"ID: {apt_Id}")
    print(f"UserNameEDit: {username}")
    print(f"UserUID: {user_uid}")
    
    try:
        # Initialize Firestore client
        db = firestore.client()

        # Get product by ID
        products_ref = db.collection('Appartments').where('apt_Id', '==', apt_Id)
        products_data = products_ref.get()

        # Check if products_data is not None
        if products_data:
            # Convert the data to a list of dictionaries
            productsArray = []
            for product in products_data:
                product_data = product.to_dict()
                product_id = product.id
                # Access image_urls as a list
                image_url = product_data.get('image_urls')
                
                # Take only the first image URL if available
                
                product_dict = {
                   'aptName': product_data.get('aptName', ''),
                    'aptPrice': product_data.get('aptPrice', ''),
                    'image_url': image_url,  # Take only the first image URL
                    'houeseFeatures': product_data.get('houeseFeatures', ''),
                    'description': product_data.get('description', ''),
                    'phoneNo': product_data.get('phoneNo', ''),
                    'region': product_data.get('region', ''),
                    'streetName': product_data.get('streetName', ''),
                    'user_uid': product_data.get('user_uid', ''),
                    'username': product_data.get('username', ''),
                    'product_id': product_id
                    # Add other product fields as needed
                }
                productsArray.append(product_dict)

            return render(request, "edit.html", {'productsArray': productsArray, 'user_uid': user_uid, 'username': username})
        else:
            # Handle case where no products are foundnhgj
            return render(request, "edit.html", {'productsArray': [], 'user_uid': user_uid, 'username': username})


    except Exception as e:
        # Handle any exceptions that occur during data retrieval
        print(f"Error fetching products: {e}")
        return render(request, "edit.html", {'productsArray': [], 'user_uid': user_uid, 'username': username})
    

    #return render(request, 'edit.html', {'user_uid': user_uid, 'username': username, 'prod_id': prod_id})
   
   
def ProductUpdated(request, user_uid, username, apt_Id):
    if request.method == 'POST':
        apptName = request.POST.get('aptName')    
        aptPrice = request.POST.get('aptPrice')
        phoneNo = request.POST.get('number')
        region = request.POST.get('region')
        streetName = request.POST.get('streetname')
        description = request.POST.get('description')
        
        selected_features = request.POST.getlist('features')
        
        # Flatten the features list
        features = selected_features
        
        getImage = []  # Initialize getImage as an empty list or None

       
        # Save user data and image URL to Firestore
        try:
            db = firestore.client()

            # Get product by ID
            products_ref = db.collection('Appartments').where('apt_Id', '==', apt_Id)
            products_data = products_ref.get()
            user_ref = db.collection('UserDetails').document(user_uid)
            user_doc = user_ref.get()

            # Check if the user document exists
            if user_doc.exists:
                user_data = user_doc.to_dict()
                email = user_data.get('email')

                if email:
                    print("Email:", email)

                    # Check for image file in request
                    image_file = request.FILES.get('images')

                    if image_file is None:
                        # No image file uploaded, use existing images from Firestore
                        if products_data:
                            for product in products_data:
                                product_data = product.to_dict()
                                getImage = product_data.get('image_urls', [])  # Use an empty list if no images

                            print(f"getImage: {getImage}")
                        else:
                            print("No product data found, using default image list.")
                    else:
                        # Image file uploaded, save the new image
                        file_path = f"images/{user_uid}/{image_file.name}"
                        image_url = upload_image_to_storage(image_file, file_path)
                        getImage.append(image_url)  # Append the new image URL to getImage

                    # Update Firestore with new data
                    user_ref = db.collection('Appartments').document(apt_Id)
                    user_ref.set({
                        'aptName': apptName,
                        'image_urls': getImage,
                        'houeseFeatures': features,
                        'aptPrice': aptPrice,
                        'phoneNo': phoneNo,
                        'streetName': streetName,
                        'region': region,
                        'description': description,
                        'user_uid': user_uid,
                        'username': username,
                        'apt_Id': apt_Id,
                        'email': email
                    })

                    return HttpResponse("Product posted successfully!")

                else:
                    print("Email not found for user_uid:", user_uid)
                    return HttpResponse("User email not found.", status=400)

        except Exception as e:
            print(f"Firestore error: {e}")
            return HttpResponse("Failed to post product. Please try again later.", status=500)

    else:
        print("No POST request received")
        return render(request, 'edit.html', {'user_uid': user_uid, 'username': username})


def Delete(request, user_uid, username, apt_Id):

    return render(request, 'delete.html', {'user_uid': user_uid, 'username': username, 'apt_Id': apt_Id})
    

def DeletionProduct(request, user_uid, username, apt_Id): 

    try:
        db = firestore.client()

        # Get product by ID
        product_ref = db.collection('Appartments').document(apt_Id)
        product_doc = product_ref.get()

        # Check if the product exists
        if product_doc.exists:
            # Delete the product
            product_ref.delete()
            messages.success(request, 'Product deleted successfully.')
        else:
            messages.error(request, 'Product does not exist.')

    except ValueError as e:     
        # Handle any exceptions
        print(f"Error deleting product: {e}")
        messages.error(request, 'Failed to delete product.')

    # Redirect back to the dashboard
    return redirect('mydashboard', user_uid=user_uid, username=username)  


def CancellDeletion(request, user_uid, username):
    return redirect('mydashboard', user_uid=user_uid, username=username) 


def upload_image_to_storage(image_file, file_path):
    try:
        # Upload the image file to Firebase Storage
        image_data = image_file.read()
        store.child(file_path).put(image_data)
        
        # Get the download URL of the uploaded image
        image_url = store.child(file_path).get_url(None)
        print(f"Successfully uploaded image: {file_path}")
        return image_url
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None
    