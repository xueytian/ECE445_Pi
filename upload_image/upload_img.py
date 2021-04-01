#




import requests, json
import pyimgur

CLIENT_ID = '0c214ab9446e86e'
PATH = 'bird1.jpg'

im = pyimgur.Imgur(CLIENT_ID)
uploaded_image = im.upload_image(PATH, title="pic")

print(uploaded_image.title)
print(uploaded_image.link)
print(uploaded_image.size)
print(uploaded_image.type)

print('uploaded link:', uploaded_image.link)