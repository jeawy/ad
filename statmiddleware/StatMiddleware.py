from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
import pdb
class Device(object):
    
    def process_view(self, request, view_func, view_args, view_kwargs):
     
        mobile = DetectMobileBrowser.process_request(request)
        request.mobile = mobile 
        return None