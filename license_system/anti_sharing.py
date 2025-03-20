import platform, subprocess

def get_hardware_fingerprint():
    # Get unique system identifiers
    try:
        mac = subprocess.check_output("cat /sys/class/net/eth0/address", shell=True)
        return hashlib.sha256(mac).hexdigest()
    except:
        # Fallback for other platforms
        return hashlib.sha256(platform.node().encode()).hexdigest()