"""
Digital signature embedder for PNG images

This script loads a 4096-bit RSA private key and embeds
a SHA-256-based digital signature of a PNG image directly
into its metadata using base64 encoding.
"""

import base64
import hashlib
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def load_private_key(path: str):
    """Load the private RSA key from a PEM file."""
    with open(path, "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )


def calculate_image_hash(image_path: str) -> bytes:
    """Return the SHA-256 hash of the image file."""
    with open(image_path, "rb") as image_file:
        return hashlib.sha256(image_file.read()).digest()


def embed_signature_into_png(image_path: str, signature: bytes, output_path: str):
    """Embed the base64 signature into PNG metadata and save new image."""
    image = Image.open(image_path)
    metadata = PngInfo()
    metadata.add_text("Signature", base64.b64encode(signature).decode())
    image.save(output_path, pnginfo=metadata)


def main():
    """Main signing process."""
    private_key_path = "private_key.pem"
    image_input_path = "original_image.jpg"
    image_output_path = "signed_image.png"

    private_key = load_private_key(private_key_path)
    image_hash = calculate_image_hash(image_input_path)

    signature = private_key.sign(
        image_hash,
        padding.PKCS1v15(),
        hashes.SHA256(),
    )

    embed_signature_into_png(image_input_path, signature, image_output_path)
    print(f"Saved {image_output_path}")


if __name__ == "__main__":
    main()
