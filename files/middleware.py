class LogRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"[LOG] {request.method} {request.path} Params: {request.GET}")
        response = self.get_response(request)
        return response