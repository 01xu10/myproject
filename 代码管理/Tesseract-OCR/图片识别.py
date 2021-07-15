
from urllib.parse import unquote

# from js2py.host.jsfunctions import encodeURIComponent
#
# a = 'TfMvjsHWGj'
# b = encodeURIComponent(a)
# print(b)

from PIL import Image
import pytesseract
text = pytesseract.image_to_string(Image.open('图片识别样本1.png'), lang='chi_sim')
print(text)