#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"


import os
import os.path
import sys
import io
import re
import gettext
import codecs
import subprocess
import itertools
import tempfile

from .indent_tools import convert_js


PY_TO_JS = None

try:
    from react import jsx
except:
    jsx = None


def list_with_next_generator(l):
    old = l[0]
    for pos in l[1:]:
        yield (old, pos)
        old = pos
    yield (l[-1], None)

def translate(s):
    return s

def iter_lines(f, f_name, lang):    
    in_table = 0
    if f_name:
        if 'app_pack' in f_name:
            l = f_name.replace('\\','/').split('app_pack')
            base_path = l[0]+"app_pack/" + l[1].split('/')[1]+"/"
        else:
            l = f_name.replace('\\','/').split('templates_src')
            base_path = l[0]+"schserw/"
    else:
        base_path = "./"
    locale_path = os.path.join(base_path,"locale")

    tab_translate = []

    if lang!='en':
        try:
            t = gettext.translation('django', locale_path, languages=[lang,])
            t.install()

            try:
                p = open(os.path.join(base_path,"translate.py"), "rt")
                for line in p.readlines():
                    fr = line.split("_(\"")
                    if len(fr)>1:
                        fr = fr[1].split("\")")
                        if len(fr)==2:
                            tab_translate.append(fr[0])
                p.close()
            except:
                tab_translate = []

            def trans(word):
                if len(word) < 2:
                    return word
                if word[0]==word[-1]=="\"" or word[0]==word[-1]=="'":
                    if word[0]=="'":
                        strtest = "'"
                    else:
                        strtest="\""
                    word2 = word[1:-1]
                else:
                    strtest = None
                    word2 = word

                if not word2 in tab_translate:
                    tab_translate.append(word2)
                ret = t.gettext(word2)
                if strtest != None:
                    return strtest+ret+strtest
                else:
                    return ret
            gt = trans
        except:
           gt = translate
    else:
        gt = translate

    for line in f:
        if len(line.lstrip())==0:
            continue
        if line.lstrip().startswith('_'):
            nr = line.find('_')
            line2=' '*nr+'.'+gt(line.strip()[1:])
        else:
            if '_(' in line:
                out = []
                fr = line.split('_(')
                out.append(fr[0])
                for pos in fr[1:]:
                    id2 = pos.find(')')
                    if id2>=0:
                        out.append(gt(pos[:id2]))
                        out.append(pos[id2+1:])
                    else:
                        out.append(gt(pos))
                line2 = ''.join(out)
            else:
                line2=line
        
        line3 = line2.strip()
        if len(line3)>0 and ( line3[0]=='[' or line3[-1]==']' or '|' in line3 ):
            if line3[0]=='[' and (line3[-1]=='|' or (line3[-1]==']' and '|' in line3)):
                if line3[1]=='[':
                    in_table = 2
                else:
                    in_table = 1
            if in_table==1:
                line2 = line2.replace('[', '<tr><td>').replace(']', '</td></tr>').replace(' |', ' </td><td>')                
            if in_table==2:
                line2 = line2.replace('[[', '<tr><th>').replace(']]', '</th></tr>').replace(' |', ' </th><th>')
            if line3[-1]==']':
                in_table = False
        yield line2
    yield "."
    if len(tab_translate)>0:
        p = open(os.path.join(base_path,"translate.py"), "wt")
        for word in tab_translate:
            p.write("_(\""+word+"\")\n")
        p.close()

class ConwertToHtml:
    def __init__(self, file_name, simple_close_elem, auto_close_elem, no_auto_close_elem, input_str = None, lang='en'):
        self.file_name = file_name
        self.input_str = input_str
        self.code = []
        self.bufor = []
        self.output = []
        self.no_conwert = False
        self.simple_close_elem = simple_close_elem
        self.auto_close_elem = auto_close_elem
        self.no_auto_close_elem = no_auto_close_elem
        self.lang = lang

    def _output_buf(self, nr):
        for pos in reversed(self.bufor):
            if pos[0] >= nr:
                self.output.append([pos[0], pos[1], pos[2]])
                self.bufor.remove(pos)
            else:
                break

    def _space_count(self, buf):
        i = 0
        for z in buf:
            if z == ' ':
                i = i + 1
            else:
                break
        return i

    def _get_elem(self, elem):
        elem2 = elem.lstrip()
        id = elem2.find(' ')
        if id > 0:
            return elem2[:id]
        return elem2

    def _transform_elem(self, elem):
        id = elem.find(' ')
        if id > 0:
            elem0 = elem[:id]
            elem1 = ''
            tmp = elem[id + 1:].split(',,,')
            for pos in tmp:
                id2 = pos.find('=')
                if id2 > 0:
                    elem1 = elem1 + ' ' + pos[:id2] + '="' + pos[id2 + 1:] + '"'
                else:
                    elem1 = elem1 + ' ' + pos
            return elem0 + elem1
        else:
            return elem

    def _pre_process_line(self, line):
        n = self._space_count(line)
        line2 = line[n:]
        if line2.rstrip() == '':
            return [None]
        if not ((line2[0] >= 'a' and line2[0] <= 'z') or (line2[0] >= 'A' and line2[0] <= 'Z') or line2[0] == '%'):
            if line2[0] == '.':
                return [(n, None, line2[1:], 0)]
            else:
                return [(n, None, line2, 0)]
        nr = line2.find('...')
        if nr >= 0:
            code = line2[:nr]
            html = line2[nr + 3:]
            if code == '':
                code = None
        else:
            code = line2
            html = None
        if code:
            if code[0] != '%':
                code2 = code.split(':::')
                if len(code2) > 1:
                    out = []
                    i = n
                    for pos in code2[:-1]:
                        out.append((i, self._transform_elem(pos), None, 3 if i
                                    == n else 1))
                        i = i + 1
                    out.append((i, self._transform_elem(code2[-1]), html, 4))
                    return out
                else:
                    code = self._transform_elem(code)
        return [(n, code, html, 0)]

    def _status_close(self, status, line, next_line):
        if status == 0:
            return 0
        if status == 1:
            return 1
        if status == 2:
            return 0
        if status == 3:
            return 2
        if status == 4:
            if next_line[0] > line[0]:
                return 3
            else:
                return 1
        return status

    def transform_line(self, line, next_line):
        self._output_buf(line[0])
        if line[1]:
            if line[1][0] == '%':
                if line[1][1] == '%':
                    if next_line[0] <= line[0]:
                        self.output.append([line[0], '{% block ' + (line[1])[2:].lstrip() + ' %}' +
                                (line[2] if line[2] else '') + '{% endblock %}', line[3]])
                    else:
                        self.output.append([line[0], '{% block ' + (line[1])[2:].lstrip() + ' %}', line[3]])
                        if line[2]:
                            self.output.append([line[0], line[2], line[3]])
                        self.bufor.append([line[0], '{% endblock %}', line[3]])
                else:
                    auto_end = False
                    tag = (line[1])[1:].split()[0].strip()
                    full_tag = (line[1])[1:].strip()
                    if full_tag.endswith(':'):
                        auto_end = True
                        tag = tag.replace(':','')
                        full_tag = full_tag[:-1]
                        if tag in self.no_auto_close_elem:
                            auto_end = False

                    self.output.append([line[0], '{% ' + full_tag + ' %}', line[3]])

                    if auto_end or tag in self.auto_close_elem or '_ext' in tag:
                        self.bufor.append([line[0], '{% end' + tag + ' %}', line[3]])
                    if line[2]:
                        self.output.append([line[0], line[2], line[3]])
            else:
                if next_line[0] <= line[0]:
                    if line[2] or not self._get_elem(line[1])\
                         in self.simple_close_elem:
                        s = line[2] if line[2] else ''
                        self.output.append([line[0], '<' + line[1] + '>' + s + '</' + self._get_elem(line[1]) + '>',
                                self._status_close(line[3], line, next_line)])
                    else:
                        self.output.append([line[0], '<' + line[1] + ' />', line[3]])
                else:
                    self.output.append([line[0], '<' + line[1] + '>', line[3]])
                    if line[2]:
                        self.output.append([line[0], line[2], line[3]])
                    self.bufor.append([line[0], '</' + self._get_elem(line[1])
                            + '>', self._status_close(line[3], line, next_line)])
        else:
            self.output.append([line[0], line[2], line[3]])

    def transform(self):
        old_line = None
        for line in self.code:
            if old_line == None:
                old_line = line
            else:
                self.transform_line(old_line, line)
                old_line = line
        if old_line:
            self.transform_line(old_line, (0, None, None))
        self._output_buf(-1)

    def process(self):
        if self.file_name:
            file = codecs.open(self.file_name, 'r', encoding='utf-8')
        else:
            file = io.StringIO(self.input_str)
        old_pos = 0
        buf = None
        buf0 = ''
        test = 0
        cont = False
        indent_pos = 0
        for _line in iter_lines(file, self.file_name, self.lang):
            line = _line.replace('\n', '').replace('\r', '').replace('\t', '        ')
            if line.replace(' ', '') == '%else' or line.replace(' ', '') == '%else:':
                line = ' ' + line
            if '!!!' in line:
                self.no_conwert = True
                file.close()
                return
            if test:
                if test > 1 and len(line.strip()) > 0 and self._space_count(line) <= indent_pos:
                    cont = True
                if cont or '<<<' in line:
                    if test == 1:
                        l = line.replace('\n', '').replace('\r', ''
                                ).replace('\t', '        ').replace('<<<', ''
                                ).rstrip()
                        buf.write(l)
                        x = self._pre_process_line(buf0 + buf.getvalue())
                        for pos in x:
                            if pos:
                                self.code.append((pos[0] * 4, pos[1], pos[2],
                                        pos[3]))
                                old_pos = pos[0]
                            else:
                                self.code.append((old_pos * 4, None, None, 1))
                        buf = None
                        test = 0
                    if test > 1:
                        if not cont:
                            l = line.replace('\n', '').replace('\r', '').replace('\t', '        ').\
                                    replace('<<<','').rstrip()
                            buf.write(l)
                        if test == 2:
                            buf2 = io.StringIO()
                            convert_js(buf, buf2)
                            x = self._pre_process_line(buf0 + buf2.getvalue())
                        elif test == 3:
                            x = self._pre_process_line(buf0.replace('pscript', 'script language=python') + buf.getvalue())
                        #elif test == 4:
                        #    v = buf.getvalue()
                        #    codejs = pjsx_to_js(v, None)
                        #    x = self._pre_process_line(buf0 + codejs)
                        #elif test == 5:
                        #    codejs = pjsx_to_js('"""'+buf.getvalue()+'"""', None)
                        #    x = self._pre_process_line(buf0 + codejs)
                        else:
                            x = self._pre_process_line(buf0 + buf.getvalue())
                        for pos in x:
                            if pos:
                                self.code.append((pos[0] * 4, pos[1], pos[2],
                                        pos[3]))
                                old_pos = pos[0]
                            else:
                                self.code.append((old_pos * 4, None, None, 1))
                        buf = None
                        buf2 = None
                        test = 0
                else:
                    buf.write(line.replace('\n', '').replace('\r', '' ).replace('\t', '        ').rstrip() + '\n')
            if cont or not test:
                cont = False
                if '>>>' in line:
                    pos = line.find('>>>')
                    if len(line[:pos].strip()) > 0:
                        buf0 = line[:pos + 3].replace('>>>', '...|||')
                    else:
                        buf0 = line[:pos + 3].replace('>>>', '.|||')
                    buf = io.StringIO()
                    buf.write(line[pos + 3:].replace('\n', '').replace('\r', '' ).replace('\t', '        ').rstrip())
                    test = 1
                elif '{:}' in line:
                    indent_pos = self._space_count(line)
                    pos = line.find('{:}')
                    if len(line[:pos].strip()) > 0:
                        buf0 = line[:pos + 4].replace('{:}', '...|||')
                    else:
                        buf0 = line[:pos + 4].replace('{:}', '.|||')
                    buf = io.StringIO()
                    buf.write(line[pos + 4:].replace('\n', '').replace('\r', '').replace('\t', '        ').rstrip())
                    test = 2
                elif '===>' in line:
                    indent_pos = self._space_count(line)
                    pos = line.find('===>')
                    if len(line[:pos].strip()) > 0:
                        buf0 = line[:pos + 4].replace('===>', '...|||')
                    else:
                        buf0 = line[:pos + 4].replace('===>', '.|||')
                    buf = io.StringIO()
                    buf.write(line[pos + 4:].replace('\n', '').replace('\r', '').replace('\t', '        ').rstrip())
                    test = 3
                elif 'script language=python' in line:
                    indent_pos = self._space_count(line)
                    pos = line.find('script language=python')
                    buf0 = line + '...|||'
                    buf = io.StringIO()
                    buf.write(line[pos + 22:].replace('\n', '').replace('\r', '').replace('\t', '        ').rstrip())
                    test = 3
                elif 'pscript' in line:
                    indent_pos = self._space_count(line)
                    buf0 = line + '...|||'
                    buf = io.StringIO()
                    test = 3
                elif line.strip().replace(' ','')=='script':
                    indent_pos = self._space_count(line)
                    buf0 = line + '...|||'
                    buf = io.StringIO()
                    test = 4
                elif line.strip().replace(' ','').startswith('%component'):
                    indent_pos = self._space_count(line)
                    pos = line.rfind(':')
                    buf0 = line + '...|||'
                    buf = io.StringIO()
                    test = 5
                else:
                    l = line.replace('\n', '').replace('\r', '').replace('\t', '        ').rstrip()
                    x = self._pre_process_line(l)
                    for pos in x:
                        if pos:
                            self.code.append((pos[0] * 4, pos[1], pos[2],
                                    pos[3]))
                            old_pos = pos[0]
                        else:
                            self.code.append((old_pos * 4, None, None, 1))
        file.close()
        self.code.append((0, None, None, 1))
        self.transform()

    def to_str(self, beauty=True):
        if self.no_conwert:
            if self.file_name:
                file = codecs.open(self.file_name, 'r', encoding='utf-8')
                output = file.read().replace('!!!', '')
                file.close()
            else:
                output = self.input_str.replace('!!!', '')
            return output
        else:
            output = ''
            if beauty:
                if len(self.output)>0:
                    for (line, nextline) in list_with_next_generator(self.output):
                        if line[0] >= 0 and (line[2] == 0 or line[2] == 3):
                            output = output + ' ' * int(line[0] / 2)
                        if line[1]:
                            output = output + line[1]
                        if line[2] == 0 or line[2] == 2:
                            output = output + '\n'
                        if line[2] == 4 and nextline and nextline[0] > line[0]:
                            output = output + '\n'
                return output.replace('|||', '\n')
            else:
                if len(self.output)>0:
                    for (line, nextline) in list_with_next_generator(self.output):
                        if (line[0] >= 0 and line[2] == 3):
                            output = output + ' ' * int(line[0] / 2)
                        if line[1]:
                            output = output + line[1]
                        if line[2] == 2:
                            output = output + '\n'
                        elif line[2] == 4 and nextline and nextline[0] > line[0]:
                            output = output + '\n'
                        elif line[1] and nextline[1] and not (line[1].strip().startswith('<') or
                                line[1].strip().startswith('{')) and not (nextline[1].strip().startswith('<') or
                                nextline[1].strip().startswith('{')):
                            output = output + '\n'
                ret = output
                ret = ret.replace('|||', '\n')
                return ret


def ihtml_to_html_base(file_name, input_str=None, lang='en'):
    """Convert file in ihtml format and return standard html

    Args:
        file_name - ihtml file name
        input_str - if not None - convert input_str instead input file
    Returns:
        converted html string
    """
    conwert = ConwertToHtml(file_name, ['br', 'meta', 'input'], [], [], input_str, lang)
    try:
        conwert.process()
        return conwert.to_str()
    except:
        import sys, traceback
        print(sys.exc_info())
        traceback.print_exc()
        return ""


def py2js(script, module_path):
    """Compile python script to javascript script

    Args:
        script - python script source
        module_path - path for target script
    """
    error = False
    tempdir = tempfile.gettempdir()

    cwd = os.getcwd()
    os.chdir(tempdir)

    script_name = os.path.join(tempdir, "pytigon_module.py")

    f = open(script_name, "wt")
    f.write(script)
    f.close()

    import transcrypt
    transcrypt_lib = transcrypt.__path__._path[0]
    cmd = [sys.executable, os.path.join(transcrypt_lib, "__main__.py"), '-n', 'pytigon_module.py' ]

    def process_output(line):
        if line.startswith('Error in program'):
            nonlocal error
            error = True
            print(line)
            m = re.search(".*line (\d*):(.*)", line)
            if m:
                try:
                    row = int(m.groups()[0])-1
                    description = m.groups()[1]
                    print("Python to javascript compile error:")
                    print(description)
                    lines = script.split('\n')
                    start = row-4
                    end = row+4
                    if start < 0:
                        start = 0
                    if end >= len(lines):
                        end = len(lines)-1
                    for i in range(start, end):
                        if row == i:
                            print(lines[i], " <===")
                        else:
                            print(lines[i])
                    print()
                except:
                    pass
    if module_path:
        old_path = os.getcwd()
        os.chdir(module_path)
    else:
        old_path = None

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
    ret, stderr_value = proc.communicate() #script)

    if stderr_value:
        for line in stderr_value.split('\n'):
            process_output(line)
    if ret:
        for line in ret.split('\n'):
            process_output(line)

    if error:
        raise Exception('Python to javascript compile error!')

    js_script_name = os.path.join(tempdir, "__javascript__/pytigon_module.mod.js")
    f = open(js_script_name, "rt")
    s = f.read()
    f.close()
    s = s.split('(function () {', 1)[1]
    s = s.rsplit('}) ();', 1)[0]
    ret = s

    if old_path:
        os.chdir(old_path)

    return ret


def py_to_js(script, module_path):
    """Compile python script to javascript. Additional indentation are removed from python scrip before compile.

    Args:
        script - python script source
        module_path - path for target script
    """
    tab = -1
    out_tab = []
    for line in script.split('\n'):
        if tab < 0:
            if line.strip()!="":
                tab = len(line) - len(line.lstrip())
            else:
                continue
        out_tab.append(line[tab:])

    code = py2js(script, module_path)

    return code


def pjsx_to_js(script, module_path):
    tabrepl = []
    if '"""' in script:
        if jsx:
            ret = []
            transformer = jsx.JSXTransformer()
            in_html = False
            for pos in script.split('"""'):
                if in_html:
                    z = ihtml_to_html_base(None, pos)
                    z=z.rstrip()
                    if z[-1] == '\n':
                        z = z[:-1]
                    tabrepl.append(transformer.transform_string(z))
                    ret.append('xxyyzz11')
                else:
                    if pos:
                        ret.append(pos)
                in_html = not in_html
            script2 = "".join(ret)
        else:
            return None
    else:
        script2 = script
    script2 = script2.replace('{{', 'xxyyzz22').replace('}}', 'xxyyzz33' )

    spaces = sum( 1 for _ in itertools.takewhile(str.isspace,script2) )
    if spaces>0:
        script2 = script2[spaces:].replace('\n'+spaces*' ', '\n')

    code = py_to_js(script2, module_path)
    for pos in tabrepl:
        pos2 = pos
        code = code.replace('xxyyzz11', '(\n'+pos2+')', 1)

    code = code.replace('xxyyzz22', '{{').replace('xxyyzz33', '}}')
    return code
