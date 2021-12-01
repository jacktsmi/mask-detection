import cv2

cam = cv2.VideoCapture(0)
print(cam.isOpened())

while True:
    ret, img = cam.read()
    if ret:
        # cv2.imshow("Put your face here", img)
        img = cv2.flip(img,1)
        ell_img = cv2.ellipse(img, (320, 240), (200, 150), 90, 0, 360, (255, 0, 0), 3)
        cv2.putText(ell_img, "Put your face here", org=(170, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255), thickness=2)
        cv2.putText(ell_img, "Make sure your forehead is visible", org=(50, 470), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255), thickness=2)
        cv2.imshow(" ", ell_img)
        key = cv2.waitKey(1) & 0XFF
        if key == 'q':
            break

