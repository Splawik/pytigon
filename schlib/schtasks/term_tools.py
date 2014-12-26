import re
from io import StringIO

ansi_pattern = '\033\[((?:\d|;)*)([a-zA-Z])'
ansi_eng = re.compile(ansi_pattern)

COLORS = ('000', 'f00', '0f0', 'ff0', '00f', 'f0f', '0ff', 'fff' )

def convert_m(code):
    if code == '0':
        return (None, None)
    else:
        start = ""
        end = ""
        codes = code.split(";")
        for c in codes:
            cc = int(c)
            if cc==1:
                start = start + "<strong>"
                end = "</strong>" + end
            if cc>=30 and cc<=37:
                start = start + "<span color='#%s'>" % COLORS[cc-30]
                end = "</span>"+end
        return (start, end)

def convert_ansi_codes(code):
    if code[-1]=='m':
        return convert_m(code[:-1])
    return ("", "")

def ansi_to_txt(ansi_txt):
    last = 0
    output = StringIO()
    matches = []
    stack = ""
    txt = ansi_txt.replace('\n','').replace('\r','')
    for match in ansi_eng.finditer(txt):
        start = match.start()
        end = match.end()
        output.write(txt[last:start])

        code = "".join(match.groups())
        x = convert_ansi_codes(code)
        if x[0]==None:
            output.write(stack)
            stack = ""
        else:
            output.write(x[0])
            stack += x[1]

        last = end
    output.write(txt[last:])
    if len(stack)>0:
        output.write(stack)

    return output.getvalue()
