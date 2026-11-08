import qrcode

data: str = "This is a test string for generating a QR code."

img = qrcode.make(data)
print(type(img))  # qrcode.image.pil.PilImage

# enforce tight image border
border_size: int = 2
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=border_size,
)

qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

# save the image
img.save("test.png".replace(" ", "_"))
