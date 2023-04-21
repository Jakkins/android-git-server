import os
from src.logg import logg


def are_keys_presence(key_name):
    user_home = os.path.expanduser("~")
    privk = os.path.join(user_home, ".ssh", key_name)
    pubk = os.path.join(user_home, ".ssh", key_name+".pub")
    logg().info(f"checking keys presence in {user_home}")
    if not os.path.exists(privk):
        logg().warning("private key not found.")
    if not os.path.exists(pubk):
        logg().warning("public key not found.")
    return os.path.exists(privk) and os.path.exists(pubk)
