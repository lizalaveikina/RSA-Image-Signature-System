"""
verify.py

This script verifies the digital signature of a PNG image stored in its metadata.
The signature was created using the RSA algorithm (4096 bits) and the SHA-256 hash function.

Requirements:
- public_key.pem — RSA public key
- signed_image.png — image with the embedded signature in metadata

Output:
- Message indicating whether the signature is valid or invalid
"""

import base64
import io
from PIL import Image
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def load_signature_from_image(image_path: str) -> tuple[str, Image.Image]:
    """
    Extracts the signature from the metadata of a PNG image
    """
    image = Image.open(image_path)
    signature_b64 = image.text.get("Signature")
    return signature_b64, image


def load_public_key(key_path: str):
    """
    Loads the public key from a PEM file
    """
    with open(key_path, "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())


def get_visual_image_bytes(image: Image.Image) -> bytes:
    """
    Obtains the byte representation of the visual image without metadata
    """
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def verify_signature(image_bytes: bytes, signature: bytes, public_key) -> bool:
    """
    Verifies the digital signature for the given image
    """
    digest = hashes.Hash(hashes.SHA256())
    digest.update(image_bytes)
    hash_value = digest.finalize()

    try:
        public_key.verify(
            signature,
            hash_value,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False


def main():
    """
    Main function of the script
    """
    signed_image_path = "signed_image.png"
    public_key_path = "public_key.pem"

    signature_b64, image = load_signature_from_image(signed_image_path)

    if not signature_b64:
        print("Signature not found in metadata")
        return

    signature = base64.b64decode(signature_b64)
    image_bytes = get_visual_image_bytes(image)
    public_key = load_public_key(public_key_path)

    if verify_signature(image_bytes, signature, public_key):
        print("Signature is valid. The image is authentic and has not been modified")
    else:
        print("Signature is invalid or the image has been modified")


if __name__ == "__main__":
    main()