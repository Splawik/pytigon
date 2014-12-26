import time

def fun(id, input_queue, output_queue, *args, **kwargs):
	print("Hello world 100", args, kwargs)
	time.sleep(100)
	print("END", id)
	return "OK"