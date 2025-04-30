"""
sign.py

This script performs a digital signature of a PNG image
using the RSA algorithm (4096 bits) and the SHA-256 hash function.
The signature is embedded in the image's metadata.

Requirements:
- private_key.pem — RSA private key
- original_image.png — image to be signed

Output:
- signed_image.png — image with the embedded signature in metadata
"""

import base64
import io
from PIL import Image, PngImagePlugin
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def load_image_as_bytes(image_path: str) -> bytes:
    """
    Loads the image and returns its byte representation (excluding metadata)
    """
    image = Image.open(image_path)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue(), image


def load_private_key(key_path: str):
    """
    Loads the private key from a PEM file
    """
    with open(key_path, "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )


def create_signature(data: bytes, private_key) -> str:
    """
    Creates a digital signature for the given data
    """
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    hash_value = digest.finalize()

    signature = private_key.sign(
        hash_value,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode()


def embed_signature_in_image(image: Image.Image, signature_b64: str, output_path: str):
    """
    Embeds the signature into the metadata of the PNG image and saves it
    """
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Signature", signature_b64)
    image.save(output_path, "PNG", pnginfo=meta)


def main():
    """
    Main function of the script
    """
    image_path = "original_image.png"
    private_key_path = "private_key.pem"
    output_image_path = "signed_image.png"

    image_bytes, image = load_image_as_bytes(image_path)
    private_key = load_private_key(private_key_path)
    signature_b64 = create_signature(image_bytes, private_key)
    embed_signature_in_image(image, signature_b64, output_image_path)

    print("The image has been signed and saved as `signed_image.png`")


if __name__ == "__main__":
    main()