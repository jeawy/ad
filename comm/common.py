from django.conf import settings
from django.contrib.auth.models import User
from .models import  Product
import pdb
class Common(): 
    def get_client_ip(self,request):
        PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', )
        """get the client ip from the request
        """
        remote_address = request.META.get('REMOTE_ADDR')
        # set the default value of the ip to be the REMOTE_ADDR if available
        # else None
        ip = remote_address
        # try to get the first non-proxy ip (not a private ip) from the
        # HTTP_X_FORWARDED_FOR
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            proxies = x_forwarded_for.split(',')
            # remove the private ips from the beginning
            while (len(proxies) > 0 and
                    proxies[0].startswith(PRIVATE_IPS_PREFIX)):
                proxies.pop(0)
            # take the first ip which is not a private one (of a proxy)
            if len(proxies) > 0:
                ip = proxies[0]
        return ip
