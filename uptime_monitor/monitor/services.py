from . test_check import check
from . models import Check

def  run_check(site):
    result = check(site.url)
    check_obj = Check.objects.create(site=site,
                                    status = result['status'],
                                    status_code = result.get('status_code',None),
                                    response_time_ms=result.get('response_time_ms',None),
                                    error = result.get('error',"NO Errors Found"))
    return check_obj
    


