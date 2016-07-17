import thread,threading
import re 
from statistics.models import Stat

"""
provide queries for each url page view
"""
class StatComm():
    """
    add comment for this function and parameters
    """
    @staticmethod
    def count_page_traffic(self, request):
        url = request.META['PATH_INFO']
        '''
        handle exception
        '''
        
        try:
            stat_instance = Stat.objects.get(url=url)
            stat_instance.count += 1
        except Stat.DoesNotExist:
            stat_instance = Stat.objects.create(url=url)
            
        #pdb.set_trace()    
        stat_instance.save()    

    


    
           






