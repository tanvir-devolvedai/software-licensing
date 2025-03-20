from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from datetime import datetime
import json

def validate_license():
    """Validate license signature and expiration"""
    try:
        # Load public key
        with open("public_key.pem", "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())
        
        # Load license
        with open("license.json", "r") as f:
            license = json.load(f)
        
        # Verify signature
        data_str = json.dumps(license["data"], sort_keys=True)
        public_key.verify(
            bytes.fromhex(license["signature"]),
            data_str.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # Check expiration
        expiry_date = datetime.fromisoformat(license["data"]["expiry_date"])
        if datetime.utcnow() > expiry_date:
            raise ValueError("License expired")
        
        return True
    
    except Exception as e:
        raise ValueError(f"Validation failed: {str(e)}")

if __name__ == "__main__":
    try:
        if validate_license():
            print("✅ License validation successful!")
            print(f"User ID: {json.load(open('license.json'))['data']['user_id']}")
            print(f"Tier: {json.load(open('license.json'))['data']['tier']}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")