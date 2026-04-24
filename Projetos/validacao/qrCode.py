import qrcode

url = input("Digite a URL para gerar o QR Code: ").strip()
file_path = "C:/Users/Usuario/Desktop/qrcode.png"

qrcoder = qrcode.QRCode()
qrcoder.add_data(url)

img = qrcoder.make_image(fill_color="black", back_color="white")
img.save(file_path)

print(f"QR Code gerado e salvo em: {file_path}")
