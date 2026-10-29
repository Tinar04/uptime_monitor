import requests
import time

def check(url):
    try:
        start = time.perf_counter()
        r = requests.get(url,timeout=5)
        end = time.perf_counter()
        ms = round((end-start)*1000)
        if r.status_code >=400:
            result = {
                "url":url, 
                "status":"DOWN",
                "status_code":r.status_code,
                "response_time_ms":ms
            }
            return result
        else:
                result = {
                            "url":url, 
                            "status":"UP",
                            "status_code":r.status_code,
                            "response_time_ms":ms
                        }
                return result
    except requests.RequestException :
            result = {
                        "url":url, 
                        "status":"DOWN",
                        "error": "No answer"
                    }

            return result