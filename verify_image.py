"""
Digital signature verifier for PNG images

This script verifies the RSA signature embedded in a PNG image's metadata
against the original image file. It ensures that the image has not been altered
and was signed using the corresponding private key.
"""

import base64
import hashlib
import sys
from PIL import Image
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def load_public_key(path: str):
    """Load the RSA public key from a PEM file."""
    with open(path, "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())


def get_signature_from_png(image_path: str) -> str:
    """Extract the base64-encoded signature from PNG metadata."""
    image = Image.open(image_path)
    return image.text.get("Signature")


def calculate_image_hash(image_path: str) -> bytes:
    """Return the SHA-256 hash of the original image file."""
    with open(image_path, "rb") as image_file:
        return hashlib.sha256(image_file.read()).digest()


def verify_signature(public_key, signature: bytes, image_hash: bytes) -> bool:
    """Verify the digital signature using the public RSA key."""
    try:
        public_key.verify(
            signature,
            image_hash,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False


def main():
    """Main verification process."""
    public_key_path = "public_key.pem"
    signed_image_path = "signed_image.png"
    original_image_path = "original_image.jpg"

    public_key = load_public_key(public_key_path)

    signature_b64 = get_signature_from_png(signed_image_path)
    if not signature_b64:
        print("Not found")
        sys.exit(1)

    signature = base64.b64decode(signature_b64)
    image_hash = calculate_image_hash(original_image_path)

    if verify_signature(public_key, signature, image_hash):
        print("Correctly signature")
    else:
        print("Non correctly signature")


if __name__ == "__main__":
    main()
