import qrcode

data:str = "https://github.com/Eggeling-Lab-Microscope-Software/blob-B-gone"

img = qrcode.make(data)
print(type(img))  # qrcode.image.pil.PilImage
img.save("current_QR.png")