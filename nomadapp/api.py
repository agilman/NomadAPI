from nomadapp.models import *
from nomadapp.serializers import *

from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User

from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

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
        print("Hello", userId)
        #TODO: VALIDATION
        user = User.objects.get(pk=userId)

        advName = data["advName"]
        advType = data["advType"]
        advStatus = data["advStatus"]

        #TODO
        #If advStatus = active, need to unset previous active.

        adv = Adventure(name=advName,user=user,advType=advType,advStatus=advStatus)
        adv.save()

        #create directory
        #media_root = settings.USER_MEDIA_ROOT
        #os.mkdir(media_root + "/" + str(userId)+"/"+str(adv.id))
        #os.mkdir(media_root + "/" + str(userId)+"/"+str(adv.id)+"/gear")

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
def maps(request,mapId=None):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        adv = Adventure.objects.get(id=int(data["adv"]))

        map = Map(name=data["name"],adv=adv)
        map.save()

        serialized = MapSerializer(map)

        return JsonResponse(serialized.data,safe=False)
    if request.method == 'DELETE':
        mapToDel = Map.objects.get(id=mapId)

        mapToDel.delete()
        serialized = MapSerializer(mapToDel)

        return JsonResponse(serialized.data,safe=False)

@csrf_exempt
def segments(request,mapId=None):
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
    if request.method=='GET':
        map = Map.objects.get(id=mapId)
        geoJson = makeGeoJsonFromMap(map)
        return JsonResponse(geoJson,safe=False)

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
