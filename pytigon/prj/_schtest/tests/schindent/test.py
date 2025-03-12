class Test:
    def __init__(self):
        self.a = 1

    def test(self):
        assert self.a == 1
        self.a = 2
        assert self.a == 2


def test():
    t = Test()
    t.test()


def test2():
    window.Alert("test")
