from django.test import TestCase

# Create your tests here.
# import pytesseract
# from PIL import Image
#
# pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract-OCR\tesseract.exe'
# text = pytesseract.image_to_string(Image.open(r'C:\Users\Administrator\Desktop\7.png'))
#
# print(text)

import easyocr

reader = easyocr.Reader(['ch_sim', 'en'])  # need to run only once to load model into memory
result = reader.readtext(r'C:\Users\Administrator\Desktop\bainiao.png',)
print(result)