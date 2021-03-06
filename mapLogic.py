import cv2
from data import edges, points, halls
from dijkestra import Graph
import base64

graph = Graph(edges)
img = cv2.imread('./sm_map.png')
color = (255,0,0)
font = cv2.FONT_HERSHEY_SIMPLEX

# given src: Text & dst: Text we use our dectionary *data.halls* to transfrom those to points
# then we find and draw the shortest path on the map and them encode to base64
def locate(src, dst):
    out = graph.dijkstra(halls[src],halls[dst])
    layer = cv2.resize(img.copy(), (610,315))
    for i in range(0, len(out)-1):
        cv2.line(layer, out[i], out[i+1], (0,0,255), thickness=2, lineType=8, shift=0)
    layer = cv2.resize(layer, (500, 350))
    layer = cv2.rotate(layer, rotateCode=cv2.ROTATE_90_COUNTERCLOCKWISE)
    retval, buffer = cv2.imencode('.jpg', layer)
    jpg_as_text = 'data:image/jpeg;base64,'+base64.b64encode(buffer).decode("utf-8") 
    return jpg_as_text

# given place: Text & dst: Text we use our dectionary *data.halls* to get location of that place
# then we add *you are here* mark on the map and then encode to base46 
def mark(place):
    layer = cv2.resize(img.copy(), (610,315))
    cv2.circle(layer,halls[place], 2, color, thickness=5) 
    cv2.putText(layer,'Here you are!',(halls[place][0]-50, halls[place][1]-10), font, .5,(255,0,0,255),1,cv2.LINE_AA) 
    layer = cv2.resize(layer, (500, 350))
    layer = cv2.rotate(layer, rotateCode=cv2.ROTATE_90_COUNTERCLOCKWISE)
    retval, buffer = cv2.imencode('.jpg', layer)
    jpg_as_text = 'data:image/jpeg;base64,'+base64.b64encode(buffer).decode("utf-8") 
    return jpg_as_text
    