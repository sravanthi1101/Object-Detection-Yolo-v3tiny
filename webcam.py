import cv2
import numpy as np
net=cv2.dnn.readNet('yolov3-tiny.weights','yolov3-tiny.cfg')
classes=[]
with open("coco.txt",'r') as f:
    classes= f.read().split('\n')
 
cap=cv2.VideoCapture(0)
#img= cv2.imread("nuts.jpeg")
 
while True:
    ret, img = cap.read()
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, _= img.shape
    blob=cv2.dnn.blobFromImage(img,1/255, (416,416), (0,0,0), swapRB=True, crop=False)
    net.setInput(blob)
    
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
    print(ln)
    #output_layers_names= net.getUnconnectedOutLayers()
    #print(output_layers_names)
 
    #layerOutputs=net.forward(output_layers_names)
    layerOutputs=net.forward(ln)
 
 
    boxes=[]
    confidences=[]
    class_ids=[]
 
    for output in layerOutputs:
        for detection in output:
            
            scores = detection[5::]
            print(scores)
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
 
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
 
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
 
    
    print(len(boxes))
    indexes= cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)
 
    if len(indexes) > 0:
        print(indexes.flatten())
 
 
    font=cv2.FONT_HERSHEY_PLAIN
    colors=np.random.uniform(0,255,size=(len(boxes),3))
 
    if len(indexes)>0:
        for i in indexes.flatten():
            
            x, y, w, h = boxes[i]
            label=str(classes[class_ids[i]])
            confidence=str(round(confidences[i],2))
            color=colors[i]
            cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
            cv2.putText(img,label+" "+confidence,(x,y+20),font,2,(255,255,255),2)
 
 
    cv2.imshow("Image",cv2.resize(img, (800,600)))
    key= cv2.waitKey(1)
    if key==27:
        break
 
cap.release()
cv2.destroyAllWindows()
 
""" font=cv2.FONT_HERSHEY_PLAIN
colors=np.random.uniform(0,255,size=(len(boxes),3))
 
for i in range(len(boxes)):
    x, y, w, h = boxes[i]
 
    label=str(classes[class_ids[i]])
    confidence=str(round(confidences[i],2))
    color=colors[i]
    cv2.rectangle(img,(x,y),((x+w),(y+h)),color,2)
    cv2.putText(img,label+" "+confidence,(x,y+20),font,2,(0,0,255),2)
     """
 
 
 
 
 
 
""" indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 2, color, 3)
 
    cv2.imshow("Image",cv2.resize(img, (800,600)))
    if cv2.waitKey(27) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
 """
 