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

from html.parser import HTMLParser, HTMLParseError
import io


def _convert_strings(lines):
    line_buf = None
    in_string = False
    #for line in lines.getvalue().split('\n'):
    lines.seek(0)
    #lines.newlines = '\n'
    #print "X1", lines.readlines()
    for line2 in lines: #.getvalue().split('\n'):        
        line = line2.replace('\n','')
        #print "X2:", line
        id = line.find('"""')
        if in_string:
            if id >= 0:
                yield line_buf + '\n' + line.replace('\n', '')
                line_buf = None
                in_string = False
            else:
                if line_buf:
                    line_buf = line_buf + line.replace('\n', '')
                else:
                    line_buf = line.replace('\n', '')
        else:
            if line.lstrip()[:1] == '#':
                continue
            if id >= 0:
                id2 = line[id:].find('"""')
                if id2 >= 0:
                    if line_buf:
                        yield line_buf + line.replace('\n', '')
                        line_buf = None
                    else:
                        yield line.replace('\n', '')
                else:
                    in_string = True
                    if line_buf:
                        line_buf = line_buf + '\n' + line.replace('\n', '')
                    else:
                        line_buf = line.replace('\n', '')
            else:
                yield line.replace('\n', '')
                line_buf = None


def spaces_count(s):
    il = 0
    for znak in s:
        if znak == ' ':
            il += 1
        else:
            return il
    return il


def norm_tab(f):
    old_il = 0
    poziom = 0
    tabpoziom = [0]
    tabkod = []
    for l in _convert_strings(f):
        line = l.replace('\t', '        ').replace('\n', '').rstrip()
        if line.lstrip() == '':
            continue
        il = spaces_count(line)
        if il > old_il:
            poziom += 1
            tabpoziom.append(il)
        else:
            if il < old_il:
                while il < tabpoziom[-1]:
                    poziom -= 1
                    del tabpoziom[-1]
        if len(line[il:]) > 0:
            tabkod.append((poziom, line[il:]))
        old_il = il
    return tabkod


def reformat_js(tabkod):
    #postfixs = [(0, '', ';'), (0, '', ';')]
    postfixs = [(0, '', ';'),]
    tabkod2 = []
    last_line = ''
    last_poziom = 0
    sep = ''
    for pos in tabkod:        
        code = pos[1]
        postfix = ''
        if code[:4] == 'def ' and code[-1] == ':':
            code = 'function ' + code[4:]
        if code.endswith('({'):
            postfix = '})'
            code = code[:-2] + '({'
            sep = ','
        elif code.endswith('('):
            postfix = ')'
            code = code[:-1] + '('
            sep = ','
        elif code.endswith('['):
            postfix = '];'
            code = code[:-1] + '['
            sep = ','
        elif code.endswith('[,'):
            postfix = '],'
            code = code[:-2] + '['
            sep = ','
        elif code.endswith(':'):
            postfix = '}'
            sep = ';'
            code = code[:-1] + '{'
        elif code.endswith('/:'):
            postfix = ''
            sep = ''
            code = code[:-2]
        elif code.endswith('='):
            postfix = '}'
            code = code[:-1] + '= {'
            sep = ','
        elif code.endswith('{'):
            postfix = '}'
            code = code[:-1] + '{'
            sep = ','
        tabkod2.append((pos[0], code, postfix, sep))
    oldpos = None
    oldpoziom = 0
    tabkod3 = []
    #postfixs = [(0, '', ';')]
    #print tabkod2
    print("-----------------------------------")
    for pos in tabkod2:
        print(pos)
    for pos in tabkod2:
        if pos[0] <= oldpoziom:
            for i in range(oldpoziom - pos[0] + 1):
                #tabkod3.append((postfixs[-1][0], postfixs[-1][1],
                #               postfixs[-1][2]))
                tabkod3.append((postfixs[-1][0], postfixs[-1][1],''))
                #print ">1>>", tabkod3[-1]
                del postfixs[-1]
        if len(pos[2]) > 0:
            #print ">2>>", tabkod3[-1]
            tabkod3.append((pos[0], pos[1], ''))
        else:
            #print ">3>>", tabkod3[-1]
            tabkod3.append((pos[0], pos[1], postfixs[-1][2]))
        postfixs.append((pos[0], pos[2], pos[3]))
        oldpos = pos
        oldpoziom = pos[0]
    for id in range(len(postfixs), 0, -1):
        if id > 1:
            tabkod3.append((postfixs[id - 1][0], postfixs[id - 1][1],
                           postfixs[id - 2][2]))
        else:
            tabkod3.append((postfixs[id - 1][0], postfixs[id - 1][1], ''))
    tmp = []
    print("-----------------------------------")
    for pos in tabkod3:
        print(pos)
        if len(pos[1]) > 0:
            tmp.append(pos)
    tabkod3 = tmp
    tabkod4 = []
    postfix = ''
    for i in range(len(tabkod3)):
        pos = tabkod3[i]
        if len(pos[1]) > 0:
            if i < len(tabkod3) - 1:
                if pos[0] > tabkod3[i + 1][0]:
                    tabkod4.append((pos[0], pos[1]))
                else:
                    tabkod4.append((pos[0], pos[1] + pos[2]))
            else:
                tabkod4.append((pos[0], pos[1] + pos[2]))
    print("-----------------------------------")
    for pos in tabkod4:
        print(pos)
    return tabkod4


def file_norm_tab(file_in, file_out):
    if file_in and file_out:
        tabkod = norm_tab(x1)
        for pos in tabkod:
            file_out.write((' ' * 4) * pos[0] + pos[1].replace('\n', '') + '\n')
        return True
    return False


def convert_js(stream_in, stream_out):
    if stream_in and stream_out:
        tabkod = norm_tab(stream_in)
        #print tabkod
        tabkod = reformat_js(tabkod)
        #print tabkod
        for pos in tabkod:
            stream_out.write((' ' * 4) * pos[0] + pos[1].replace('\n', ''
                             ).replace('};', '}').replace(';;', ';') + '\n')
        return True
    return False



class NormParser(HTMLParser):

    def __init__(self):
        self.txt = io.StringIO()
        self.tab = 0
        HTMLParser.__init__(self)

    def _remove_spaces(self, value):
        return value.strip()

    def _print_attr(self, attr):
        ret = ''
        for pos in attr:
            if ret != '':
                ret += ',,,'
            if pos[1]:
                ret += pos[0] + '=' + pos[1]
            else:
                ret += pos[0]
        return ret

    def handle_starttag(self, tag, attrs):
        self.txt.write('\n')
        self.txt.write((' ' * self.tab) * 4)
        self.txt.write(tag + ' ' + self._print_attr(attrs))
        self.tab += 1

    def handle_endtag(self, tag):
        self.tab -= 1


    def handle_startendtag(self, tag, lattrs):
        self.handle_starttag(tag, lattrs)
        self.handle_endtag(tag)

    def handle_data(self, data):
        if self._remove_spaces(data).replace('\n', '') != '':
            self.txt.write('...')
            self.txt.write(self._remove_spaces(data).replace('\n', '\\n'))

    def process(self, data):
        try:
            self.feed(data)
        except HTMLParseError as error:
            lines = data.split('\n')
            print(error)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            print(lines[error.lineno - 2])
            print((lines[error.lineno - 1])[:error.offset] + '!!!'\
                 + (lines[error.lineno - 1])[error.offset:])
            print(lines[error.lineno])
            print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        return self.txt.getvalue()[1:] + '\n'


class IndentHtmlParser(NormParser):

    def _print_attr(self, attr):
        ret = ''
        for pos in attr:
            if ret != '':
                ret += ',,,'
            if pos[1]:
                ret += pos[0] + '=' + pos[1]
            else:
                ret += pos[0]
        return ret

    def handle_starttag(self, tag, attrs):
        self.txt.write('\n')
        self.txt.write((' ' * self.tab) * 4)
        self.txt.write(self.get_starttag_text())
        self.tab += 1

    def handle_endtag(self, tag):
        self.tab -= 1
        if self.tab < 0:
            self.tab = 0
        self.txt.write('\n')
        self.txt.write((' ' * self.tab) * 4)
        self.txt.write('</' + tag + '>\n')

    def handle_data(self, data):
        self.txt.write('\n')
        self.txt.write((' ' * self.tab) * 4)
        tmp = ('\n' + (' ' * self.tab) * 4).join([x.strip() for x in
                data.split('\n')])
        self.txt.write(tmp)


def norm_html(txt):
    try:
        n = NormParser()
        ret = n.process(txt)
    except:
        ret = txt
    return ret


def indent_html(txt):
    try:
        n = IndentHtmlParser()
        ret = n.process(txt)
        lines = ret.split('\n')
        lines = [x for x in lines if x.strip() != '']
        ret = '\n'.join(lines)
    except:
        ret = txt
    return ret


if __name__ == '__main__':
    
    #f_in = open('./test/input2.js', 'r')    
    #f_out = open('./test/output.js', 'w')
    
    #convert_js(f_in, f_out)
    #f_in.close()
    #f_out.close()
    
    if False:
        print("x1")
        f_in = open('./test/test11.html', 'r')    
        print("x2", f_in)
        f_out = open('./test/test11.ihtml', 'w')
        print("x3", f_out)
        
        ret = norm_html(f_in.read())
        f_out.write(ret)
        f_in.close()
        f_out.close()
    
    if True:
        print("x1")
        f_in = open('./test/test11.ihtml', 'r')    
        print("x2", f_in)
        f_out = open('./test/_test11.html', 'w')
        print("x3", f_out)
        
        ret = indent_html(f_in.read())
        f_out.write(ret)
        f_in.close()
        f_out.close()
        