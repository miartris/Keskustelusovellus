def validate_post_request(req_csrf: int, u_csrf: int):
    return session.get("username") and req_csrf == u_csrf

def validate_post_content(content: str, min_length: int, max_length: int):
    return len(content) <= max_length and len(content) >= min_length and content