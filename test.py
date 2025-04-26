import face_recognition
import cv2
import sys

# مسیر تصویر را وارد کنید
image_path = "path_to_your_image.jpg"  # مسیر به تصویر خود را وارد کنید

# بارگذاری تصویر
image = face_recognition.load_image_file(image_path)

# شناسایی چهره‌ها
face_locations = face_recognition.face_locations(image)

# نمایش تعداد چهره‌ها شناسایی شده
print(f"Found {len(face_locations)} face(s) in this photograph.")

# بارگذاری تصویر با استفاده از OpenCV برای نمایش آن
image_cv = cv2.imread(image_path)

# رسم مستطیل دور چهره‌ها
for face_location in face_locations:
    top, right, bottom, left = face_location
    cv2.rectangle(image_cv, (left, top), (right, bottom), (0, 255, 0), 2)

# نمایش تصویر با چهره‌ها
cv2.imshow("Faces found", image_cv)
cv2.waitKey(0)
cv2.destroyAllWindows()
