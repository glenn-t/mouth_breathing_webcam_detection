import cv2
import time
import os
from datetime import datetime

JPEG_QUALITY = 80
RATIO = 16/9
CAPTURE_RESOLUTION = "360p"
OUTPUT_RESOLUTION_HEIGHT = 360
OUTPUT_RESOLUTION_WIDTH = int(OUTPUT_RESOLUTION_HEIGHT*RATIO)

RESOLUTIONS = {
    (str(x) + "p"): {
        "height": x,
        "width": int(x*RATIO)
    } for x in [360, 720, 1080]
}

RES_HEIGHT = RESOLUTIONS[CAPTURE_RESOLUTION]["height"]
RES_WIDTH = RESOLUTIONS[CAPTURE_RESOLUTION]["width"]



encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]

def capture_photos(interval=1, output_folder="webcam_captures"):
    """
    Captures photos from webcam at specified intervals.
    
    Parameters:
    interval (int): Time interval between captures in seconds (default: 1)
    output_folder (str): Folder to save captured images (default: 'webcam_captures')
    """
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")
       
    try:
        while True:
            # Capture frame
            camera = cv2.VideoCapture(0)
            if  not camera.isOpened():
                print("Camera not available")
            else:
                camera.set(cv2.CAP_PROP_FRAME_WIDTH, RES_WIDTH)
                camera.set(cv2.CAP_PROP_FRAME_HEIGHT, RES_HEIGHT)
                ret, frame = camera.read()
                if frame is not None:

                    # Generate timestamp for filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{output_folder}/webcam_{timestamp}.jpg"
                
                    # Save the image
                    if (RES_WIDTH != OUTPUT_RESOLUTION_WIDTH) and (RES_HEIGHT != OUTPUT_RESOLUTION_HEIGHT):
                        frame = cv2.resize(frame, (OUTPUT_RESOLUTION_WIDTH, OUTPUT_RESOLUTION_HEIGHT))

                    cv2.imwrite(filename, frame, encode_param)

                    print(f"Captured: {filename}")
                
                    # Display the frame
                    # cv2.imshow("Webcam Capture", frame)
                    
                    # # Check for 'q' key press to exit (wait for 'interval' seconds or until key press)
                    # if cv2.waitKey(int(interval * 10000)) & 0xFF == ord('q'):
                    #     print("Capture stopped by user.")
                    #     break
            camera.release()
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("Capture stopped by user (Ctrl+C).")
    
    finally:
        # Release the webcam and close windows
        camera.release()
        cv2.destroyAllWindows()
        print("Webcam released and program terminated.")

if __name__ == "__main__":
    capture_photos()