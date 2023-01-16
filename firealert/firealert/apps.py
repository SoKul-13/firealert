from django.apps import AppConfig
from logging import log
from .models import IrwinData
from .models import ZipData
from datetime import datetime
import csv 
import math
import urllib.request, json
from django.db.models import ValueRange
from decimal import Decimal
from queue import PriorityQueue


class FirealertConfig(AppConfig):
    name = 'firealert'

class FireLocator:   
    def __init__(self):
        pass

    #Read fires and return count
    def findFire(self,longitude, lattitude):
        fire = IrwinData.objects.filter(longitude = longitude, lattitude=lattitude)
        if(len(fire) == 0):
            return 0
        else:
            for f in fire:
                print(f.incidentname)

        return len(fire)

    def findFires(self,longitude, lattitude, zipcode):
        #Get longitude/lattitude for zip
        if(len(zipcode) >0):
            print(' user sent zip code' + zipcode)
            ldata = ZipData.objects.filter(zip=zipcode)
            longitude = ldata[0].longitude
            lattitude = ldata[0].lattitude
            print(longitude,lattitude )

        #Get fires for the zip 
        radius = Decimal(0.20)
        loStart = Decimal(longitude) - radius
        loEnd = Decimal(longitude) + radius
        liStart = Decimal(lattitude) - radius
        liEnd = Decimal(lattitude) + radius

        print(loStart,loEnd)
        fires = IrwinData.objects.filter(
            longitude__range= [loStart,loEnd],
            lattitude__range= [liStart,liEnd]
        )
        results =[]
        if(len(fires) == 0):
            print(" No fires found .......................")
        else:
            weatherData = WeatherReloader()
            windspeed =  weatherData.reloadFromWeatherService(longitude,lattitude)[0]         
            winddegree = weatherData.reloadFromWeatherService(longitude,lattitude)[1]
            print("Got wind data")
            print(windspeed)
    
            print("fires found at this location --------------------------------")
            closestFireTime = 60.0
            count=0
            for f in fires:
                count +=1
                print(f.incidentname,f.city,f.state)
                print("Calculating Time for Fire...")
                deltaLongitude = longitude - f.longitude
                deltaLattitude = lattitude - f.lattitude
                #deltaLongitude = 38.7109-38.792458
                #deltaLattitude = (-123.10414)-(-122.780053)
                radian = math.atan2(deltaLongitude,deltaLattitude)
                angle = radian*(180/math.pi)
                print(angle)
                finalspeed = angle
                anglemeasure = abs(angle - 225)
                anglemeasure = abs(angle - winddegree)
                windspeed = (windspeed*0.000621371)*3600
                windspeed = 6

                if anglemeasure <= 90:
                    finalspeed = windspeed/1.5
                else: 
                    finalspeed = windspeed/1
                
                distance = math.sqrt((pow(deltaLongitude,2) + pow(deltaLattitude,2)))
                distance = distance*69
                print("printing distance")
                print(distance)


                time = distance/finalspeed

                print("You have "+ str(time) +" hours to escape")
                closestFireTime = min(time,closestFireTime)
                print("You have "+ str(closestFireTime) +" hours to escape closest fire")
                

            print("processed all fires, returning information of closest fire")            
            results.append(count)
            results.append(closestFireTime)

        return results
    #end 

    #dd
    def calculateTime(self, longitude, lattitude, userlongitude, userlattitude, windspeed, winddirection):
        
        deltaLongitude = userlongitude-longitude
        deltaLattitude = userlattitude-lattitude
        radian = math.atan2(deltaLongitude,deltaLattitude)
        angle = radian*(180/math.pi)
        print(angle)
        finalspeed = angle
        anglemeasure = abs(angle - winddirection)
        windspeed = (windspeed*0.000621371)*3600

        if anglemeasure <= double(90):
            finalspeed = windspeed/2

        else:
            finalspeed = windspeed/1
        
        distance = (deltaLongitude**2 + deltaLattitude**2)**(1/2)
        distance = distance*69

        time = distance/finalspeed

        print("You have "+ str(time) +" hours to escape")
        return time

class FileReloader:   
   
    def __init__(self):
        pass

    #Read from JSON and update database
    def reloadFromService(self):
        count =0
        urlName="https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Active_Fires/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
        with urllib.request.urlopen(urlName) as url:
            data = json.loads(url.read().decode())
            features = data['features']
            print(" features length =" + str(len(features)))
            for feature in features:
                irId = feature['properties']['IrwinID']  
                
                rowreturn = IrwinData.objects.filter(irwinid = irId)                
                #check in database if exists                 
                if ( len(rowreturn) == 0 ):                        
                    #Add new row
                    row = IrwinData(longitude = feature['geometry']['coordinates'][0], 
                        lattitude = feature['geometry']['coordinates'][1],
                        incidentname = feature['properties']['IncidentName'], 
                        city = feature['properties']['POOCity'], 
                        county = feature['properties']['POOCounty'], 
                        state = feature['properties']['POOState'].split('-')[1], 
                        irwinid = irId)
                    print('Saving Data for ', irId)
                    mdate = datetime.fromtimestamp(feature['properties']['ModifiedOnDateTime_dt']/1000) 
                    cdate = datetime.fromtimestamp(feature['properties']['CreatedOnDateTime_dt']/1000)
                    row.cdate = cdate
                    row.mdate = mdate
                    row.save()
                    count += 1

        return count
            
    #Reload the file
    def reloadCsvFile(self):
        fileName = "C:\\FireData\\Current_Wildfire_Points.csv"
        count =0
        with open(fileName, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for line in reader:
                print(line['POOState'], line['IrwinID'])
                row = IrwinData(longitude = line['ï»¿X'], lattitude = line['Y'],
                incidentname = line['IncidentName'], city = line['POOCity'], county = line['POOCounty'],
                state = line['POOState'].split('-')[1], irwinid = line['IrwinID'])
                mdate = datetime.strptime(line['ModifiedOnDateTime_dt'].rstrip(), '%Y/%m/%d %H:%M:%S') 
                cdate = datetime.strptime(line['CreatedOnDateTime_dt'].rstrip(), '%Y/%m/%d %H:%M:%S')
                row.cdate = cdate
                row.mdate = mdate
                row.save()
                count += 1                
        return count

    def reloadZipData(self):
        fileName = "C:\\FireData\\us-zip-code-latitude-and-longitude.csv"
        count =0
        with open(fileName, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')            
            for line in reader:
                row = ZipData(longitude = line['Longitude'], lattitude = line['Latitude'],
                city = line['City'], zip = line['Zip'],
                state = line['State'])
                row.save()
                count += 1                
        return count
class WeatherReloader:
    def __init__(self):
        pass

    #Read from JSON
    def reloadFromWeatherService(self, longitude, lattitude):  
        speed =0.0
        degree = 0.0      
        urlName="https://api.openweathermap.org/data/2.5/weather?lat="+ str(lattitude) + "&lon=" + str(longitude) + "&appid=c09c3bd35c005e9e5ccad59f08d3e54b"
        print(' url='+ urlName)
        with urllib.request.urlopen(urlName) as url:
            data = json.loads(url.read().decode())
            print(data)
            wind = data['wind']
            speed = wind['speed']
            degree = wind['deg']
            print(speed)
            print(degree)
        
        return (speed,degree)