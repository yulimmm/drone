import cv2

img = cv2.imread('car.jpg')

# Create our body classifier
car_classifier = cv2.CascadeClassifier('car.xml')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Pass frame to our car classifier
cars = car_classifier.detectMultiScale(gray, 1.4, 2)

# Extract bounding boxes for any bodies identified
for (x, y, w, h) in cars:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
    print("down w:" + str(w) + "    h:" + str(h) + "\n")
    print("down x:" + str(x) + "    y:" + str(y) + "\n")

cv2.imshow('image detect',img)
cv2.waitKey()
cv2.destroyAllWindows()
