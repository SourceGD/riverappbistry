from nacl.encoding import Base64Encoder
from nacl.public import PrivateKey

# Générer une nouvelle clé privée
private_key = PrivateKey.generate()

# Convertir la clé privée en une chaîne de caractères encodée en Base64
private_key_str = private_key.encode(encoder=Base64Encoder).decode("utf-8")

print(private_key_str)