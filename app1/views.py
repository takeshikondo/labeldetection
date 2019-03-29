from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .forms import PhotoForm, ImageForm
from .models import Photo
import requests
import base64
import json
 
def upload(request):
    ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
    api_key = 'your_api_key'
    
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('app1:upload')
    else:
        form =PhotoForm()
        objects = Photo.objects.all()
        last = objects.last()
    
    #image_files = []     
    #image_requests = []
    
    #image_files.append(last.image.url[1:])
    
    #for file in image_files:
    #    with open(file, 'rb') as f:
    #        content = base64.b64encode(f.read()).decode('UTF-8')
    #        image_requests.append({
    #                'image': {'content': content},
    #                'features': [{
    #                   'type': 'LABEL_DETECTION',
    #                   'maxResults': 5
    #                }]
    #        })
    
    if len(objects) > 0:
        with open(last.image.url[1:], 'rb') as f:
            content = base64.b64encode(f.read()).decode('UTF-8')
            image_requests = {
                    'image': {'content': content},
                    'features': [{
                            'type': 'LABEL_DETECTION',
                            'maxResults': 3
                            }]
                    }
                
        response = requests.post(ENDPOINT_URL,
                                 data=json.dumps({"requests": image_requests}),
                                 params={'key': api_key},
                                 headers={'Content-Type': 'application/json'})
        
        description1 = response.json()['responses'][0]['labelAnnotations'][0]['description']
        score1 = response.json()['responses'][0]['labelAnnotations'][0]['score']
        description2 = response.json()['responses'][0]['labelAnnotations'][1]['description']
        score2 = response.json()['responses'][0]['labelAnnotations'][1]['score']
        description3 = response.json()['responses'][0]['labelAnnotations'][2]['description']
        score3 = response.json()['responses'][0]['labelAnnotations'][2]['score']
        
    else:
        description1 = ''
        score1 = 0
        description2 = ''
        score2 = 0
        description3 = ''
        score3 = 0
                    
    d = {
        'form': form,
        'objects': objects,
        'last': last,
        'description1': description1,
        'score1': '{:.3f}'.format(score1),
        'description2': description2,
        'score2': '{:.3f}'.format(score2),
        'description3': description3,
        'score3': '{:.3f}'.format(score3),
    }
        
    return render(request, 'app1/upload.html', d)

def upload2(request):
    from PIL import Image
    from io import BytesIO
    
    ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
    api_key = 'your_api_key'
    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']
            #image = form.cleaned_data['image']
            
            img = Image.open(image)
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
                        
            content = base64.b64encode(buffered.getvalue()).decode('UTF-8')
            image_requests = {
                    'image': {'content': content},
                    'features': [{
                            'type': 'LABEL_DETECTION',
                            'maxResults': 3
                            }]
                    }
                    
            response = requests.post(ENDPOINT_URL,
                                 data=json.dumps({"requests": image_requests}),
                                 params={'key': api_key},
                                 headers={'Content-Type': 'application/json'})
            
            description1 = response.json()['responses'][0]['labelAnnotations'][0]['description']
            score1 = response.json()['responses'][0]['labelAnnotations'][0]['score']
            description2 = response.json()['responses'][0]['labelAnnotations'][1]['description']
            score2 = response.json()['responses'][0]['labelAnnotations'][1]['score']
            description3 = response.json()['responses'][0]['labelAnnotations'][2]['description']
            score3 = response.json()['responses'][0]['labelAnnotations'][2]['score']
            
            d = {
                'description1': description1,
                'score1': '{:.3f}'.format(score1),
                'description2': description2,
                'score2': '{:.3f}'.format(score2),
                'description3': description3,
                'score3': '{:.3f}'.format(score3),
            }
                        
            return render(request, 'app1/label.html', d)
        
    else:
        form = ImageForm()   
                
    d = {
        'form': form,
    }
        
    return render(request, 'app1/upload2.html', d)
    

def download(request):
    return render(request, 'app1/download.html')
