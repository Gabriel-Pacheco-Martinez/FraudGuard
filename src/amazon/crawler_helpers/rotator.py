# General
import random

# Configuration
from config import settings

class ProxyRotator:
    def get_proxy(self):

        proxy = random.choice(settings.proxies)
        ip, port = proxy.split(":")

        return {
            "ip": ip,
            "port": int(port),
            "user": settings.proxy_user,
            "pass": settings.proxy_pass
        }




