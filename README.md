# Individual-task

This task implements a basic image digital signature system based on RSA (4096-bit key) and SHA-256 hashing.
The idea is to protect image authenticity and detect any tampering by embedding a cryptographic signature into the image metadata.

## Potential Applications
- Digital certificates for artworks (proof of authorship of paintings, NFTs, or design work)
- Secure document imaging (embedding signatures into scanned legal documents)
- Watermarking for digital media without visible alterations
- Proof of origin for scientific images or evidence photos

The system ensures:
- The integrity of the original image
- Verification of the author/owner through public key cryptography

## Approach Description
### 1. RSA Key Generation
- A 4096-bit RSA private/public key pair is generated using the cryptography Python library (generation_keys.py)
- The private key is used for signing, while the public key is used for verifying the signature

### 2. Hash Calculation
- The input image (original_image.jpg) is read as bytes
- A SHA-256 hash of the image is computed to uniquely represent its content

### 3. Digital Signature Creation
- The SHA-256 hash is signed with the private RSA key using the PKCS#1 v1.5 padding scheme
- The signature is then encoded using Base64 to make it safely embeddable in text-based image metadata

### 4. Embedding Signature
- The signature is embedded into the PNG metadata of the new image (signed_image.png)
- I use the PIL (Pillow) library and PngInfo to add a textual field "Signature" containing the Base64-encoded signature

### 5. Verification Process
- The system extracts the embedded signature from the PNG file (signed_image.png)
- The original image file (original_image.jpg) is hashed again using SHA-256
- Using the public key, the system checks whether the signature correctly matches the new hash
- If verification passes, the image is authentic and unmodified; otherwise, it is either altered or forged

## Project Structure
| File | Description |
|:-----|:------------|
| `generation_keys.py` | Generates RSA key pair and saves them to PEM files. |
| `sign_image.py` | Signs the image and embeds the signature into PNG metadata. |
| `verify_image.py` | Verifies the embedded signature against the original image. |
| `original_image.jpg` | The image used for signing (input). |
| `signed_image.png` | The resulting image containing the digital signature. |
| `private_key.pem` | Private RSA key used for signing. |
| `public_key.pem` | Public RSA key used for verification. |

## Requirements
Language: 
Python

Libraries:
- cryptography Pillow

## Notes
- Only PNG images can carry embedded metadata using this method
- The private key must be securely stored and never shared
