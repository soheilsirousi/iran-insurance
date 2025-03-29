

def generate_response(success:bool, content, error):
    return dict(success=success, content=content, error=error)
