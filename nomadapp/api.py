from nomadapp.models import *
from nomadapp.serializers import *
from nomadapp.forms import *

from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User

from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

from PIL import Image
from PIL.ExifTags import TAGS

import os

from datetime import datetime

@csrf_exempt
def user(request,userName=None):
    if request.method == 'GET':
        try:
          user = User.objects.get(username=userName)
          serialized = UserSerializer(user).data
        except User.DoesNotExist:
            serialized = []

        return JsonResponse(serialized, safe=False)

    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['allow'] = ','.join(['get','options'])
        return response

@csrf_exempt
def me(request,userId):
    if request.method == 'GET':
        adventures = Adventure.objects.filter(user=userId)
        advSerializer = AdventureSerializer(adventures,many=True)

        total = {"adventures":advSerializer.data,"bio":"#",'profilePhotos':[]}
        return JsonResponse(total, safe=False)

    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['allow'] = ','.join(['get','options'])
        return response

@csrf_exempt
def adventures(request,advId=None):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        userId = int(data["user"])
        #TODO: VALIDATION
        user = User.objects.get(pk=userId)

        advName = data["advName"]
        advType = data["advType"]
        advStatus = data["advStatus"]

        adv = Adventure(name=advName,user=user,advType=advType,advStatus=advStatus)
        adv.save()

        #create directory
        target = os.path.join(settings.USER_MEDIA_ROOT,str(userId),str(adv.id))
        os.mkdir(target)

        serialized = AdventureSerializer(adv)
        return JsonResponse(serialized.data,safe=False)

    if request.method == 'DELETE':
        advToDel = Adventure.objects.get(id=advId)

        advToDel.delete()
        serialized = AdventureSerializer(advToDel)

        return JsonResponse(serialized.data,safe=False)

    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['allow'] = ','.join(['post','delete','options'])
        return response


@csrf_exempt
def advMaps(request,advId=None):
    if request.method == 'GET':
        maps = Map.objects.filter(adv=advId)
        serialized = MapSerializer(maps,many=True)

        return JsonResponse(serialized.data,safe=False)

@csrf_exempt
def advMaps2(request, advId=None):
    if request.method == 'GET':
        maps = Map.objects.filter(adv=advId)
        results = []
        for map in maps:
            res = {'id':map.id,
                   'name':map.name,
                   'geojson': makeGeoJsonFromMap(map)}
            results.append(res)

        return JsonResponse(results,safe=False)

@csrf_exempt
def maps(request,mapId=None):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        adv = Adventure.objects.get(id=int(data["adv"]))

        map = Map(name=data["name"],adv=adv)
        map.save()

        result = { 'id': map.id,
                'name': map.name,
                'geojson': makeGeoJsonFromMap(map)
        }

        #create a directory for user media
        target = os.path.join(settings.USER_MEDIA_ROOT, str(data["user"]),str(adv.id),str(map.id))
        os.mkdir(target)

        return JsonResponse(result,safe=False)
    if request.method == 'DELETE':
        mapToDel = Map.objects.get(id=mapId)

        mapToDel.delete()
        serialized = MapSerializer(mapToDel)

        return JsonResponse(serialized.data,safe=False)

@csrf_exempt
def segments(request,mapId=None):
    if request.method=='GET':
        """ This was used by API to get segments from 1 map at a time...
            Moved to getting all segments with maps """
        map = Map.objects.get(id=mapId)
        geoJson = makeGeoJsonFromMap(map)
        return JsonResponse(geoJson,safe=False)

    if request.method=='POST':
        data = JSONParser().parse(request)
        #Try validation with serializers...

        if "map" in data.keys() and data["map"] is not None:
            map = Map.objects.get(id=int(data["map"]))
            startTime  = None
            endTime = None
            if "startTime" in data.keys():
                startTime = data["startTime"]
            if "endTime" in data.keys():
                endTime = data["endTime"]

            distance = data["distance"]
            waypoints = data["waypoints"]

            #create segment
            mapSegment = Segment(map=map,
                                        startTime=startTime,
                                        endTime=endTime,
                                        distance = distance
                                        )

            mapSegment.save()
            #create waypoints
            for point in waypoints:
                waypointObj = WayPoint(segment = mapSegment, lat = point[1], lng = point[0])
                waypointObj.save()

            #return custom geoJson
            result = makeGeoJsonFromSegment(mapSegment)

            return JsonResponse(result,safe=False)
        else:
            return JsonResponse({"error":"Bad input"})

def makeGeoJsonFromMap(map):
    features = []
    for segment in map.segments.all():

        coordinates = []
        for coord in segment.coordinates.all():
            coordinates.append([float(coord.lat),float(coord.lng)])

        geometry = {"type":"LineString","coordinates":coordinates}

        segmentDict = {"type":"Feature",
                       "geometry":geometry,
                       "properties": {"segmentId":segment.id,
                                      "distance":segment.distance,
                                      "startTime":segment.startTime,
                                      "endTime":segment.endTime}
                       }
        features.append(segmentDict)

    mapDict = {"type":"FeatureCollection", "features":features}
    return mapDict

def makeGeoJsonFromSegment(segment):
    coordinates = []
    for coord in segment.coordinates.all():
        coordinates.append([float(coord.lat),float(coord.lng)])

    geometry = {"type":"LineString","coordinates":coordinates}

    feature = {"type":"Feature",
               "geometry":geometry,
               "properties":{"segmentId":segment.id,
                             "distance":segment.distance,
                             "startTime":segment.startTime,
                             "endTime":segment.endTime}
              }
    return feature


@csrf_exempt
def photoUpload(request):
    if request.method == "POST":
        form = photoUploadForm(request.POST,request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            userId = form['userId'].value()
            advId = form['advId'].value()
            mapId = form['mapId'].value()
            photoRecord = handle_uploaded_photo(userId,advId,mapId,f)
            print("photoRecord:", photoRecord)
            serialized = PhotoSerializer(photoRecord)


            return JsonResponse(serialized.data,safe=False)
        else:
            return JsonResponse({"msg":"FAIL"},safe=False)

@csrf_exempt
def photos(request,mapId=None):
    if request.method=='GET':
        results = Photo.objects.filter(map=mapId)
        serialized = PhotoSerializer(results,many=True)
        return JsonResponse(serialized.data,safe=False)

## Helper functions...
## These image convertion routines should be called from a queue
##  and executed seperately from the webserver
def convertImage(filePath,targetName,newName):
    target = os.path.join(filePath,targetName)
    im = Image.open(target)

    im.save(os.path.join(filePath,newName), "JPEG", quality=85, optimize=True, progressive=True)

def rotateImage(imgPath):
    print(imgPath)
    im = Image.open(imgPath)

    srev = imgPath[::-1]
    ext = imgPath[len(srev)-srev.index("."):]

    if ext=="jpg" or ext=="jpeg":
        toRotate = True
        exifdict = im._getexif()
        if exifdict:
            for k in exifdict.keys():
                if k in TAGS.keys():
                    if TAGS[k]=="Orientation":
                        orientation = exifdict[k]
                        if orientation == 3:
                            im = im.rotate(180, expand=True)
                        elif orientation == 6:
                            im = im.rotate(270, expand=True)
                        elif orientation == 8:
                            im = im.rotate(90, expand=True)
                        else:
                            toRotate = False

        if toRotate:
            im.save(imgPath)

def handle_uploaded_photo(userId,advId,mapId,f):
    #save file
    fileName = f.name
    filePath = os.path.join(settings.USER_MEDIA_ROOT,str(userId),str(advId),str(mapId))
    target = os.path.join(filePath , fileName)

    with open(target, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    #create a db record
    myMap = Map.objects.get(id=int(mapId))
    now = datetime.now()
    dbPicture = Photo(map=myMap, caption=None ,uploadTime=now)
    dbPicture.save()

    #convert image to jpg, and save named after photo id
    newName= str(dbPicture.id)+".jpg"
    convertImage(filePath,fileName,newName)

    #rotate image if needed.
    rotateImage(os.path.join(filePath,newName))

    #delete initial download
    os.remove(os.path.join(filePath,fileName))

    return dbPicture
