import cv2
import numpy as np
import mediapipe as mp
from pixellib.tune_bg import alter_bg

#flask
def Sunglasses_filter():

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    overlay_image = cv2.imread('assets\sunglasses.png')
    cap = cv2.VideoCapture(0)

    while True:
        status, frame = cap.read()
        
        if not status:

            print("Failed to capture image")
            break

        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            roi_gray = gray_img[y:y+h, x:x+w]

            roi_color = frame[y:y+h, x:x+w]

            eyes = eye_cascade.detectMultiScale(roi_gray)
            
            if len(eyes) > 0:
                ex_min, ey_min = eyes[0][:2]
                ex_max, ey_max = eyes[0][:2]
                ew_max, eh_max = eyes[0][2:]

                for (ex, ey, ew, eh) in eyes:
                    ex_min = min(ex_min, ex)
                    ey_min = min(ey_min, ey)
                    ex_max = max(ex_max, ex + ew)
                    ey_max = max(ey_max, ey + eh)
                overlay_width = ex_max - ex_min
                overlay_height = ey_max - ey_min
                resized_overlay = cv2.resize(overlay_image, (overlay_width, overlay_height))

                roi_color[ey_min:ey_min+overlay_height, ex_min:ex_min+overlay_width] = resized_overlay
                
                
                cv2.rectangle(roi_color, (ex_min, ey_min), (ex_max, ey_max), (0, 255, 0), 2)
        cv2.imshow('Face and Eye Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# to be updated use harcascade to edit the frames
def crop_image(img):
    
    crop=img[50:300,200:420]
    return crop

# to be updated use cvzone
def multi_camera(cam):

    url = "rtsp://192.168.68.128:8080/h264_opus.sdp"
    video_capture_main = cv2.VideoCapture(0)
    video_capture_phone = cv2.VideoCapture(url)

    while True:
        ret0, frame0 = video_capture_main.read()
        ret1, frame1 = video_capture_phone.read()
        if ret0 and ret1:
            
            frame1_resized = cv2.resize(frame1, (frame0.shape[1], frame0.shape[0]))
            
            
            combined_frame = np.hstack((frame0, frame1_resized))
            
            cv2.imshow('Combined', combined_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture_main.release()

    video_capture_phone.release()

    cv2.destroyAllWindows()


# use cvzone
def blur_effect():
    cam = cv2.VideoCapture(0)
    cam.set(3,1980)
    cam,set(4,1080)
    blur = alter_bg(model_type='pb')
    blur.load_pascalvoc_model(r'D:\python_mini_projects\TASKS\PYTHON\xception_pascalvoc.pb')
    seq,result = blur.blur_camera(cam,frames_per_second=10,extreme=True,show_frames=True,frame_name='blur_frame',detect='person',output_video_name=r'D:\python_mini_projects\TASKS\PYTHON\video.mp4')
def main():
    blur_effect()
    
if __name__ == "__main__":
    main()
