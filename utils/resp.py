def resp_success(data=None, message=None):
    return {
        "code": 0,
        "message": message,
        "data": data
    }


def resp_failed(code=None, data=None, message=None):
    failed_code = 500
    if code:
        failed_code = code
    return {
        "code": failed_code,
        "message": message,
        "data": data
    }
