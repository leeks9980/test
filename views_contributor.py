from django.shortcuts import render,HttpResponse,redirect
#from .models import Post
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import os
import shutil
# Create your views here.
nextId = 3
event_infoms = [
    {'id':1,'tittle':'행사1','event_time':'행사 시간1','Event_Description':'행사 설명1','event_poster':'img_0.jpg'},
    {'id':2,'tittle':'행사2','event_time':'행사 시간2','Event_Description':'행사 설명2','event_poster':'img_1.jpg'},
]
event_location = [
    {'id':1,'latitude':35.81348433055707,'longitude':127.08855272941277},
    {'id':2,'latitude':35.813167497283146,'longitude':127.09042234488336}
]
#초기 설정화면 함수 
def HTMLtemplate(articletag ,id = None):
    global event_infoms
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li><a href="/update/{id}">행사 정보 수정</a></li>
            <li>
                <form action = "/delete/" method = "POST">
                    <input type ="hidden" name ="id" value = {id}>
                    <input type ="submit" value = "삭제">
                </form>
            </li>
        '''
    new_event = ''
    if id == None:
        new_event = '''
        <li><a href = "/create">행사 추가</a></li>
        '''
    ol = ''
    for event_info in event_infoms:
        ol += f'<li><a href="/read/{event_info["id"]}">{event_info["tittle"]}</a></li>'
    return f'''
    <html>
    <body>
        <h1><a href = "/">전주대 행사 알림<a/></h1>
        <ol>
            {ol}
        </ol>
        {articletag}
        <ul>
            {new_event}
            {contextUI}
        </ul>
    </body>
    </head>
    ''' 
#초기 화면
def index(request):
    article = ''
    return HttpResponse(HTMLtemplate(article))
#매인 화면 만들기
def read(request,id):
    global event_location
    global event_infoms
    article = ''
    for event_info in event_infoms:
        if event_info['id'] == int(id):
            for location in event_location:
                if location['id'] == int(id):
                    article = f''''
                    <h2>{event_info["tittle"]}</h2>
                    <img src="/static/image/{event_info["event_poster"]}" width ="330" height = "330" alt="event_poster"><br>
                    행사 위치<br>
                    {View_map_location_selection()}<br>
                    {event_info["event_time"]}<br>
                    {event_info["Event_Description"]}        
                    '''%(
                        location['latitude'],location['longitude'],
                        location['latitude'],location['longitude'],
                        )
    return HttpResponse(HTMLtemplate(article, id))

#행사 추가
image_lable = 0
@csrf_exempt
def create(request):
    global nextId
    global image_lable
    global event_location
    if request.method == 'GET':
        article = f'''
        <form action = "/create/" method="post" enctype="multipart/form-data">
                <p><input type ="text" name = "tittle" placeholder="행사 제목"></p>
                <p>행사 위치 지정</p>
                <p>{Choosing_map_location('Add')}</p>
                <p><textarea name ="event_time" placeholder="행사 시간"></textarea></p>
                <p><textarea name ="Event_Description" placeholder="행사 설명"></textarea></p>
                <p><input type = "file" name ="image"  accept= image/* placeholder="행사 포스터"></p>
                <p><input type = 'submit'></p>
        </form>
        
        '''
        return HttpResponse(HTMLtemplate(article))
    elif  request.method == 'POST':
        #사직 정적 파일 모여 있는곳 으로 이동 및 사진 이름 변경 
        a = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(f"image_{image_lable}.jpg", a)
        shutil.move(f"C:/python_workspace/{filename}","C:\python_workspace\static\image")
        image_lable += 1
        #행사 위치 좌표 위치 리스트에 넣기
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        new_event_location ={
            'id':nextId,
            'latitude':latitude,
            'longitude':longitude
        }

        #행사 정보 리스트에 정보 추가
        event_location.append(new_event_location)
        tittle = request.POST['tittle']
        event_time= request.POST['event_time']
        Event_Description= request.POST['Event_Description']
        event_poster = filename
        newTopic = {
            'id':nextId,
            "tittle":tittle,
            "event_time":event_time,
            "Event_Description":Event_Description,
            "event_poster":event_poster,
        }
        event_infoms.append(newTopic)
        url = '/read/' + str(nextId)
        nextId += 1
        return redirect(url)
        
#행사 삭제 
@csrf_exempt
def delete(request):
    global event_infoms
    if request.method == 'POST':
        id = request.POST['id']
        new_topics = []
        for event_info in event_infoms:
            if event_info['id'] != int(id):
                new_topics.append(event_info)
        event_infoms = new_topics
        return redirect('/')

#행사 수정 
@csrf_exempt
def update(request,id):
    global event_infoms
    global event_location
    if request.method == 'GET':
        for event_info in event_infoms:
            if event_info['id'] == int(id):
                selectedTopics = {
                    "tittle":event_info['tittle'],
                    "event_time":event_info["event_time"],
                    "Event_Description":event_info["Event_Description"],
                    "event_poster":event_info["event_poster"]
                }
        for i in event_location:
            if i['id'] == int(id):
                new = {
                    'latitude_event_location':i['latitude'],
                    'longitude_event_location':i['longitude']
                }
        
        article = f'''
        <form action = "/update/{id}/" method="post" enctype="multipart/form-data">
                <p><input type ="text" name = "tittle" placeholder="tittle" value ={selectedTopics["tittle"]} "></p>
                <p>행사 위치 지정</p>
                <p>{Choosing_map_location('change')}</p>
                <input type = "text" name ="latitude" placeholder="위도를 입력 하세요" value ={new['latitude_event_location']}>
                <input type = "text" name ="longitude" placeholder="경도를 입력 하세요" value ={new['longitude_event_location']}>
                <p><textarea name ="event_time" placeholder="body">{selectedTopics["event_time"]}</textarea></p>
                <p><textarea name ="Event_Description" placeholder="body">{selectedTopics["Event_Description"]}</textarea></p>
                <p><input type = "file" name ="image" accept= image/* placeholder="행사 포스터"></p>
                <p><input type = 'submit'></p>
        </form>
        '''
        print(123)
        return HttpResponse(HTMLtemplate(article,id))
    elif  request.method == 'POST':
        print(789)
        global image_lable
        try:
            if request.FILES['image'].find('.') >= 0:
                print(9485612)
                a = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(f"image_{image_lable}.jpg", a)
                shutil.move(f"C:/python_workspace/{filename}","C:\python_workspace\static\image")
                image_lable += 1
        except Exception as e:
            print(845)
            for event_info in event_infoms:
                if event_info['id'] == int(id):
                    filename = event_info["event_poster"] 

        #행사 위치 좌표 정보 수정
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        for event_location_adjustment in event_location:
            if event_location_adjustment['id'] == int(id):
                event_location_adjustment['latitude'] = latitude
                event_location_adjustment['longitude'] = longitude 
                    
        #행사 정보 리스트 정보 수정 
        tittle = request.POST['tittle']                                       
        event_time = request.POST['event_time']
        Event_Description = request.POST['Event_Description']
        for event_info in event_infoms:
            if event_info['id'] == int(id):
                event_info['tittle'] = tittle
                event_info['event_time'] = event_time
                event_info['Event_Description'] = Event_Description
                event_info['event_poster'] = filename  
        return redirect(f"/read/{id}/")

#행사 위치 선정 
def Choosing_map_location(select):
    if select == 'change':
        return '''
        <meta charset="utf-8">        
        <div id="map" style="width:50%;height:350px;"></div>
        <div id="clickLatlng"></div>
        <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey=35c83c5172b5dd93b957565cff713e0a"></script>
        <script>
        var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
            mapOption = { 
                center: new kakao.maps.LatLng(35.81378967028329,127.09001917846082), // 지도의 중심좌표
                level: 3 // 지도의 확대 레벨
            };
        var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다
        // 지도를 클릭한 위치에 표출할 마커입니다
        var marker = new kakao.maps.Marker({ 
            // 지도 중심좌표에 마커를 생성합니다 
            position: map.getCenter() 
        }); 
        // 지도에 마커를 표시합니다
        marker.setMap(map);
        // 지도에 클릭 이벤트를 등록합니다
        // 지도를 클릭하면 마지막 파라미터로 넘어온 함수를 호출합니다
        kakao.maps.event.addListener(map, 'click', function(mouseEvent) {       
            // 클릭한 위도, 경도 정보를 가져옵니다 
            var latlng = mouseEvent.latLng; 
            // 마커 위치를 클릭한 위치로 옮깁니다
            marker.setPosition(latlng);
            var message = '클릭한 위치의 위도는 ' + latlng.getLat() + ' 이고, ';
            message += '경도는 ' + latlng.getLng() + ' 입니다';
            var resultDiv = document.getElementById('clickLatlng'); 
            resultDiv.innerHTML = message;
        });
        </script>
        '''
    if select == 'Add':
        return'''
        <meta charset="utf-8">        
        <div id="map" style="width:50%;height:350px;"></div>
        <div id="clickLatlng"></div>
        <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey=35c83c5172b5dd93b957565cff713e0a"></script>
        <script>
        var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
            mapOption = { 
                center: new kakao.maps.LatLng(35.81378967028329,127.09001917846082), // 지도의 중심좌표
                level: 3 // 지도의 확대 레벨
            };
        var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다
        // 지도를 클릭한 위치에 표출할 마커입니다
        var marker = new kakao.maps.Marker({ 
            // 지도 중심좌표에 마커를 생성합니다 
            position: map.getCenter() 
        }); 
        // 지도에 마커를 표시합니다
        marker.setMap(map);
        // 지도에 클릭 이벤트를 등록합니다
        // 지도를 클릭하면 마지막 파라미터로 넘어온 함수를 호출합니다
        kakao.maps.event.addListener(map, 'click', function(mouseEvent) {       
            // 클릭한 위도, 경도 정보를 가져옵니다 
            var latlng = mouseEvent.latLng; 
            // 마커 위치를 클릭한 위치로 옮깁니다
            marker.setPosition(latlng);
            var message = '클릭한 위치의 위도는 ' + latlng.getLat() + ' 이고, ';
            message += '경도는 ' + latlng.getLng() + ' 입니다';
            var resultDiv = document.getElementById('clickLatlng'); 
            resultDiv.innerHTML = message;
        });
        </script>
        <input type = "text" name ="latitude" placeholder="위도를 입력 하세요">
        <input type = "text" name ="longitude" placeholder="경도를 입력 하세요">
        '''

#행사 위치 보기
def View_map_location_selection():
    return '''
    <div id='map' style='width:500px;height:500px;display:inline-block;'></div>
    <script type='text/javascript' src='//dapi.kakao.com/v2/maps/sdk.js?appkey=35c83c5172b5dd93b957565cff713e0a'></script>
    <script>
    var container = document.getElementById('map');
    var options = {
        center: new kakao.maps.LatLng(%s, %s),
        level: 3
    };
    var map = new kakao.maps.Map(container, options);
    var markerPosition  = new kakao.maps.LatLng(%s,%s);
    var marker = new kakao.maps.Marker({position: markerPosition});
    marker.setMap(map);
    // 마커에 커서가 오버됐을 때 마커 위에 표시할 인포윈도우를 생성합니다
    // 인포윈도우를 생성합니다
    var infowindow = new kakao.maps.InfoWindow({
        content : iwContent
    });
    </script>
    '''

#student
def student_HTMLtemplate(articletag ,id = None):
    global event_infoms
    ol = ''
    for event_info in event_infoms:
        ol += f'<li><a href="/read_sutdent/{event_info["id"]}">{event_info["tittle"]}</a></li>'
    return f'''
    <html>
    <body>
        <h1><a href = "/student/">전주대 행사 알림<a/></h1>
        <ol>
            {ol}
        </ol>
        {articletag}
    </body>
    </head>
    '''
def student_see(request):
    article = ''
    return HttpResponse(student_HTMLtemplate(article))
TestImage = ['img_0.jpg','img_1.jpg']
def read_sutdent(request,id):
    global event_location
    global event_infoms
    article = ''
    for event_info in event_infoms:
        if event_info['id'] == int(id):
            for location in event_location:
                if location['id'] == int(id):
                    article = f'''
                    <h2>{event_info["tittle"]}</h2>
                    <img src="/static/image/{event_info["event_poster"]}" width ="330" height = "330" alt="image"><br>
                    행사 위치<br>
                    {View_map_location_selection()}<br>
                    행사 시간<br>
                    {event_info["event_time"]}<br>
                    행사 설명<br>
                    {event_info["Event_Description"]}        
                    '''%(
                        location['latitude'],location['longitude'],
                        location['latitude'],location['longitude'],
                        )
    return HttpResponse(student_HTMLtemplate(article, id))