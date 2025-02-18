import qrcode

data:str = "..."

img = qrcode.make(data)
print(type(img))  # qrcode.image.pil.PilImage
img.save("something.png")