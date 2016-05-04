f = open("./__javascript__/pytigon.js", "rt")
prg = f.read()
f.close()

x = prg.split("__all__.__call__ = __call__;")
if len(x)==2:
    x0 = x[0].replace("function pytigon () {", "")
    x1 = "\n\nfunction pytigon () {" + x[1] 
    xx = x0+"__all__.__call__ = __call__;"+x1
    f2 = open("../../static/sch/pytigon.js", "wt")
    f2.write(xx)
    f2.close()