class ViewRequests(object):
    def process_request(self, request):
        print(request.method, request.path)


def view_post(get_response):
    def middleware(request):
        try:
            if request.method == "POST":
                print("=================== POST ======================")
                print(request.path)
                print(request.POST)
                print("===============================================")
        except:
            pass
        response = get_response(request)
        return response

    return middleware


class ViewPost(object):
    def process_request(self, request):
        try:
            if request.method == "POST":
                print("=================== POST ======================")
                print(request.path)
                print(request.POST)
                print("===============================================")
        except:
            pass


class BeautyHtml:
    def process_response(self, request, response):
        if not response.streaming:
            if type(response.content) == str:
                response.content = "\n".join(
                    [line for line in response.content.split("\n") if line.strip()]
                )
            elif type(response.content) == bytes:
                response.content = "\n".join(
                    [
                        line
                        for line in response.content.decode("utf-8").split("\n")
                        if line.strip()
                    ]
                )
        return response
