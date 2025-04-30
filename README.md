# RSA Image Signature System

This project demonstrates how to digitally sign an image using RSA (4096-bit keys) and SHA-256, embedding the signature directly into the image metadata. The image remains visually unchanged, yet can be verified for authenticity using a corresponding public key.

---

## Use Case: Why Digitally Sign Images?

Digital signatures for images ensure:
- **Authenticity** – the image was created or approved by the known source.
- **Integrity** – the image has not been modified since it was signed.
- **Non-repudiation** – the signer cannot deny having signed the image.

Potential applications include:
- Signing official scans and digital documents.
- Verifying the source of published media content.
- Detecting tampering or manipulation of images in journalism, forensics, or legal workflows.

---

## How It Works

### 1. **Key Generation (Outside the Script)**
Keys are generated using OpenSSL:
```bash
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:4096
openssl rsa -pubout -in private_key.pem -out public_key.pem
```

---

## Signing Process (`sign.py`)

The `sign.py` script performs the following steps:

- **Loads** an image in PNG format.
- **Saves** the image's pixel data to memory (excluding any metadata).
- **Hashes** the image data using the SHA-256 algorithm.
- **Signs** the hash using a 4096-bit RSA private key.
- **Encodes** the signature in Base64 format.
- **Embeds** the encoded signature into the image’s metadata using PNG key-value pairs.
- **Saves** the signed image as `signed_image.png`.

> This process ensures the image appears unchanged to the human eye, but cryptographically contains a hidden signature in its metadata that can later be verified.

---

## Verification Process (`verify.py`)

The `verify.py` script performs the following steps:

- **Loads** the `signed_image.png` file.
- **Extracts** the embedded signature from the image’s metadata.
- **Hashes** the visual pixel content of the image (ignoring metadata).
- **Uses** the RSA public key to verify the extracted signature against the computed hash.
- **Displays** whether the signature is valid and whether the image has been modified.

> This ensures that any unauthorized changes to the image — even a single pixel — will be detected during verification.

---

## How to Run

1. Place your image as `original_image.png` in the project folder.
2. Run the signing script:
```bash
python3 sign.py
```
3. Then run the verification script:
```bash
python3 verify.py
```

---

## Requirements

To run the project, the following tools and libraries must be installed:

- **Python 3.8 or higher**
- The following Python libraries (installable via `pip` or using `requirements.txt`):
  - `cryptography` – used for RSA key handling and digital signature operations
  - `Pillow` – used for image loading, saving, and metadata manipulation

### Installation Instructions

To install all required dependencies, use the following command:

```bash
pip install -r requirements.txt
```

---

## File Structure

├── original_image.png        # Input image
├── private_key.pem           # Private RSA key (keep secret)
├── public_key.pem            # Public RSA key (shareable)
├── signed_image.png          # Output image with embedded signature
├── sign.py                   # Script to sign the image
├── verify.py                 # Script to verify the signature
├── requirements.txt          # List of required Python dependencies
└── README.md                 # Documentation

---

## Notes & Innovation

- The solution **avoids signing metadata or unnecessary binary noise**, focusing only on the meaningful visual content of the image.
- The signature is **embedded using native PNG key-value metadata**, making it invisible to users but accessible to verification scripts.
- The signed image **opens normally in any standard image viewer** and looks identical to the original.
- The code is **modular, readable, and conforms to [PEP 8](https://peps.python.org/pep-0008/) and `pylint` best practices**.
- **Advanced users** may explore enhancements such as:
  - steganographic embedding of the signature (hidden in pixels)
  - encryption of the signature for additional confidentiality
  - multi-signature support or watermark integration

---

## Result

The system successfully signs and verifies the integrity of images,  
providing an elegant and secure method to detect tampering in visual digital content.

---

## Author

Created by **Yelyzaveta Laveikina**  
Course: *Fundamentals of Information Security*  
Ukrainian Catholic University (UCU)
