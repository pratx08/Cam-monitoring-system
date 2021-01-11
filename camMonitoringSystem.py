import cv2
import winsound

# Initiate camera
cam = cv2.VideoCapture(0)

# Run till cam is open
while cam.isOpened():
    # Capture frames
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()

    # Comapre the 2 frames
    diff = cv2.absdiff(frame1, frame2)

    # Convert to grayscale for precision
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)

    # Remove blurs
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Increse contrast
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Detect contours - Boundary of changes
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours
    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    # Draw rectangular contours for major changes only
    for i in contours:
        # Ignore small changes
        if cv2.contourArea(i) < 15000:
            continue

        # Get (x, y), width and height of contour
        x, y, w, h = cv2.boundingRect(i)

        # Draw the rectangle
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Play alert sound
        winsound.MessageBeep(winsound.MB_OK)

    # Press 'q' to quit
    if cv2.waitKey(10) == ord('q'):
        break

    # Display Cam
    cv2.imshow("Window", frame1)
