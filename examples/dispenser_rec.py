import face_recognition
import cv2
import numpy as np
import os

# Get a reference to webcam #0 (the default one)
def recognize():
    video_capture = cv2.VideoCapture(-1, cv2.CAP_V4L2)

    # Create arrays of known face encodings and their names
    known_face_encodings = []
    known_face_names = []

    path = './faces/'
    faces = os.listdir(path)

    for i in faces:
        load_img = face_recognition.load_image_file(i)
        img_encoding = face_recognition.face_encodings(load_img)[0]
        known_face_encodings.append(img_encoding)
        known_face_names.append(i[:-4])

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    cnt = 0

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame
            
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            name = "Unknown"
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    print(name)

                # face_names.append(name)

        process_this_frame = not process_this_frame
        
        if name == 'Unknown':
            print("Please ensure that you are in the sight of the camera and you have sent your medication to us.")
            cnt += 1

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        if cv2.waitKey(800) or cnt == 10:
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    
    return name!='Unknown', name

ret, name = recognize()