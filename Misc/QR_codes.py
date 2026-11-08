import qrcode

data:str = "XXX"

img = qrcode.make(data)
print(type(img))  # qrcode.image.pil.PilImage
img.save("XXX.png")