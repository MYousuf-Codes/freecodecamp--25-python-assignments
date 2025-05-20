import qrcode

data = 'Don\'t be a stranger!'

qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(data)

qr.make(fit=True)
img = qr.make_image(fill_color='blue', back_color='white')

img.save('E:/giaic/assignments_25/QR Code/qrcode1.png')
