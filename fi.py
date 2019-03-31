#!/usr/bin/env python3

import sys
from parsy import *

def emit_link(key, target):
    return "<a href='#' id='%s'>%s</a>" % (target, key)

label = regex(r'\w+')
optional_spaces = string(' ').many().optional()
chars = regex(r'[^{}\n]+')

link = seq(
        string('{') >> chars << string('}'),
        string('{') >> label << string('}')).combine(emit_link)
word = link | chars

@generate
def heading():
    l = yield label
    yield (optional_spaces >> string(':') >> optional_spaces)
    t = yield word.many().optional()
    yield string('\n')
    out = "<p id='%s' class='content'>" % l
    if t:
        out = out + ("<strong>%s</strong></br>" % ''.join(t))
    return out

@generate
def paragraph():
    h = yield heading
    line = word.at_least(1) << string('\n')
    lines = line.at_least(1)
    t = yield lines
    empty_lines = string('\n').at_least(1)
    yield empty_lines
    out = h
    out = out + '</br>'.join([''.join(l) for l in t])
    out = out + '</br></p>'
    return out

@generate
def document():
    p = yield paragraph.at_least(1)
    out = """
<html> <head> <script type="text/javascript">
window.onload = function(){
    for (elem of document.getElementsByClassName("content")){
        elem.style.display = 'none';
    }
    let start = document.querySelector("p#start");
    start.style.display = 'inline';
    document.querySelectorAll("p.content a").forEach((link) => {
        link.onclick = () => {
            link.parentElement.style.display = 'none';
            document.querySelector("p#" + link.id).style.display = 'inline';
        };
    });
}
</script> <style type="text/css">a {font-style: italic; color: black }</style>
</head> <body>
"""
    out += '\n'.join(p)
    out += "\n</body> </html>"
    return out

if __name__ == '__main__':
    print(document.parse(sys.stdin.read()))

