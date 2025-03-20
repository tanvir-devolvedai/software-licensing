from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta
import json

def generate_keys():
    """Generate RSA key pair and save to PEM files"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    # Save private key (keep this secure!)
    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Save public key (embed this in client)
    public_key = private_key.public_key()
    with open("public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    
    return private_key, public_key

def create_license(user_id, expiry_date, tier, private_key):
    """Create signed license file"""
    license_data = {
        "user_id": user_id,
        "expiry_date": expiry_date.isoformat(),
        "tier": tier
    }
    
    # Create signature
    data_str = json.dumps(license_data, sort_keys=True)
    signature = private_key.sign(
        data_str.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    
    # Package license
    license = {
        "data": license_data,
        "signature": signature.hex()  # Store as hex for JSON
    }
    
    # Save to file
    with open("license.json", "w") as f:
        json.dump(license, f, indent=2)
    
    return license

if __name__ == "__main__":
    # Generate sample license
    private_key, _ = generate_keys()
    expiry_date = datetime.utcnow().replace(
        microsecond=0, second=0, minute=0, hour=0
    ) + timedelta(days=30)
    
    license = create_license(
        user_id="mac_user_001",
        expiry_date=expiry_date,
        tier="premium",
        private_key=private_key
    )
    
    print("Generated license:")
    print(json.dumps(license, indent=2))