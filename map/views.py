from django.shortcuts import render
import folium
import geocoder
import random
from .forms import DropdownForm

# Create your views here.



currentMapPoints = []

numMarkersPlaced = 0


def index(request):
    form = DropdownForm()
    return render(request, 'newGame.html',{'form': form})

def newGame(request):
    #create new game.
    #get type of game from form.

    selected_option = None

    if(request.method == 'POST'):
        form = DropdownForm(request.POST)
        if form.is_valid():
            selected_option = form.cleaned_data['dropdown']
            if selected_option == 'option1':
                print("Selected small map.")
                context = getNewMap(selected_option)
            elif selected_option == 'option2':
                #index(request)
                context = getNewMap(selected_option)
            elif selected_option == 'option3':
                context = getNewMap(selected_option)

            else:
                print("Error")
            return render(request, 'index.html', context)

    else:
        form = DropdownForm()
        return render(request, 'newGame.html',{'form': form})


    


def getNewMap(option):

    selected_option = option

    mapSizeValue = 0.1
    mapSizeZoom = 12

    

    if(selected_option == "option1"):
        mapSizeValue = 0.01
        mapSizeZoom = 15
    if(selected_option == "option2"):
        mapSizeValue = 0.025
        mapSizeZoom = 14
    if(selected_option == "option3"):
        mapSizeValue = 0.1
        mapSizeZoom = 12


    #create map object

    global numMarkersPlaced
    numMarkersPlaced = 0
    currentMapPoints.clear()

    g = geocoder.ip('me')
    g_lat = g.lat
    g_long = g.lng

    new_map = folium.Map(location=[g_lat,g_long], zoom_start=mapSizeZoom)

    for i in range(5):
        random_lat = random.uniform(g_lat - mapSizeValue , g_lat + mapSizeValue)
        random_long = random.uniform(g_long - mapSizeValue, g_long + mapSizeValue)
        folium.Marker(location=[random_lat,random_long], popup="Location " + str(i+1)).add_to(new_map)

        currentMapPoints.append(random_lat)
        currentMapPoints.append(random_long)


    custom_icon = folium.Icon(color='green', icon='star')
    folium.Marker(location=[g_lat,g_long],popup="Your Location",icon=custom_icon).add_to(new_map)

    pageTitle = "Home Page"
        
    new_map = new_map._repr_html_()
    context = {
        'new_map':new_map,
        'lat_long':g.latlng,
        'page_title':pageTitle,
        'make_guess':"Make First Guess"
    }
    return context


def addMarker(request):
    #add marker for guess

    global numMarkersPlaced

    finishedGuessing = False

    totalScore = 0

    g = geocoder.ip('me')
    g_lat = g.lat
    g_long = g.lng

    currentMap = folium.Map(location=[g_lat,g_long], zoom_start=13)

    


    print(currentMapPoints)

    

    if(numMarkersPlaced <= 4):
        
        

        #######
        ##
        #for testing
        ##
        #######
        #random_lat = random.uniform(g_lat - 0.01 , g_lat + 0.01)
        #random_long = random.uniform(g_long - 0.01, g_long + 0.01)

        currentMapPoints.append(g_lat)
        currentMapPoints.append(g_long)
        
        
        
        numPoints = 0
        numPoints = len(currentMapPoints)/2
        numPoints = int(numPoints)
        print(numPoints)

        for i in range(numPoints):
            if(i<5):
                folium.Marker(location=[currentMapPoints[2*i],currentMapPoints[2*i+1]], popup="Location " + str(i+1)).add_to(currentMap)
            else:
                custom_icon = folium.Icon(color='red',icon="circle")
                folium.Marker(location=[currentMapPoints[2*i],currentMapPoints[2*i+1]], icon=custom_icon,popup="Guess " + str(i-4)).add_to(currentMap)



        numMarkersPlaced = numMarkersPlaced +1

        totalScore = GetScore(numMarkersPlaced)

        if(numMarkersPlaced == 4):
            make_guess = "Make Final Guess"
        
        if(numMarkersPlaced == 5):
            print("Finished guessing.")

            finishedGuessing = True

            

            totalScore = GetScore(numMarkersPlaced)

        

        
    make_guess = "Make Guess " + str(numMarkersPlaced+1)

    roundNumber = numMarkersPlaced
    pageTitle = "Playing Game Round " + str(roundNumber)


    currentMap = currentMap._repr_html_()
    context = {
        'new_map':currentMap,
        'lat_long':g.latlng,
        'total_score':totalScore,
        'page_title':pageTitle,
        'make_guess':make_guess
    }

    if(finishedGuessing):
        return render(request, 'finishedGame.html',context)
    else:
        return render(request, 'index.html',context)

def GetScore(numMarkers):
    totalScore = 0

    for i in range(numMarkers):
        roundScore = abs((currentMapPoints[2*i+10] - currentMapPoints[2*i]) * 10000) + abs((currentMapPoints[2*i+11] - currentMapPoints[2*i+1]) * 10000)

        roundScore = 5000 - roundScore
        print(roundScore)
        totalScore += roundScore

    return int(totalScore)