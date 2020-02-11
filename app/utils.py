import cv2

def get_frame(src=0):
    cap = cv2.VideoCapture(0)
    
    while True:
        ret,frame = cap.read()
        
        if not ret:
            cap = cv2.VideoCapture(src)

        (flag,encodedImage) = cv2.imencode(".jpg",frame)

        if not flag:
            continue

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                    bytearray(encodedImage) + b'\r\n')


