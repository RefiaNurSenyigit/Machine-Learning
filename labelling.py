import os
import cv2 as cv
import numpy as np

IMAGE_PATH = "C:\\Users\\ref_deneme\\Desktop\\Elmosis\\goruntuIsleme\\dataset\\train"
THRESH_PATH = "C:\\Users\\ref_deneme\\Desktop\\Elmosis\\goruntuIsleme\\dataset\\label2\\"

def save_pic(img, name, thresh_value, counter):
    raw, png = name.split(".")
    cv.imwrite(f"{THRESH_PATH}{raw}_{thresh_value}.png", img)
    print(f"\"{raw}_{thresh_value}.png\" kaydedildi.")
    cv.imshow('kaydedilen', img)
    cv.waitKey(500)  # 0.5 saniye göster
    cv.destroyWindow('kaydedilen')
    return counter + 1

i = 0


for file in os.listdir(IMAGE_PATH):
    indv_path = os.path.join(IMAGE_PATH, file)
    img = cv.imread(indv_path)

    if img is None:
        print(f"{file} okunamadı, atlanıyor...")
        continue

    print(f"İşlenen dosya: {file}")
    cv.imshow('orijinal', img)

    # Başlangıç threshold değeri
    value = 128  
    inv = False  # "i" tuşuna basınca invert edecek

    while True:
        flag = cv.THRESH_BINARY_INV if inv else cv.THRESH_BINARY
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # threshold için griye çevir
        _, thresh = cv.threshold(gray, value, 255, flag)

        cv.imshow('threshold', thresh)
        print(f"[T:{value}] ↑/↓ değer değiştir, I invert, Q kaydet, C iptal")

        key = cv.waitKey(0) & 0xFF

        if key == ord('q'):  # Kaydet
            i = save_pic(thresh, file, value, i)
            cv.destroyWindow('threshold')
            cv.destroyWindow('orijinal')
            break
        elif key == ord('c'):  # İptal
            cv.destroyWindow('threshold')
            cv.destroyWindow('orijinal')
            print("Resim kaydedilmedi.")
            break
        elif key == ord('i'):  # İnvert değiştir
            inv = not inv
            cv.destroyWindow('threshold')
            continue
        elif key == ord('.'):  # . tuşu
            value = min(255, value + 3)
            cv.destroyWindow('threshold')
            print(value)
        elif key == ord(' '):  # boşluk tuşu
            value = max(0, value - 3)
            cv.destroyWindow('threshold')
            print(value)
        elif key == ord('m'):
            kernel = np.ones((3,3), np.uint8)
            thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel )
            thresh = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel)
            cv.imshow('m', thresh)
            key2 = cv.waitKey(0) & 0xFF
            if key2 == ord("q"):
                i = save_pic(thresh, file, value,i)
                cv.destroyWindow('threshold')
                cv.destroyWindow('orijinal')
                cv.destroyWindow('m')
                break

cv.destroyAllWindows()
print(f"Toplam {i} resim işlendi.")

