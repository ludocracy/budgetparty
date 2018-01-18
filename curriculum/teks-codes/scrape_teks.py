from urllib.request import urlopen
import re
import json

url = "http://ritter.tea.state.tx.us/rules/tac/chapter113/ch113c.html"
html = str(urlopen(url).read())
in_correct_section = False
in_correct_subsection = False
current_paragraph = {}
teks_dict = {}
for paragraph in html.split('<p'):
    text = re.search(r'(?<=>).+(?=<)', paragraph).group()
    if not in_correct_section:
        if re.search('United States Government', text):
            in_correct_section = True
    elif not in_correct_subsection:
        if re.search('Knowledge and skills', text):
            in_correct_subsection = True
    else:
        m = re.search(r'(?<=class=)\w+(?=(>))', paragraph)
        if m:
            klass = m.group()
            if klass == 'SOURCENOTE':
                break
            code, text = text.split('&nbsp;&nbsp;')
            text = text.replace(' \\r\\n ', '')
            code = code[1:-1].lower()
            if klass == 'PARAGRAPH1':
                l = text.split('. ')
                subject_code = l[0][:3].lower()
                text = '. '.join(l[1:])

                current_paragraph = {
                    'code': code,
                    'text': text,
                    'subject_code': subject_code
                }
            elif klass == 'SUBPARAGRAPHA':
                key = subject_code + current_paragraph['code'] + code
                teks_dict[key] = current_paragraph['text'] + text

with open('teks_dict.json', 'w') as teks_file:
    json.dump(teks_dict, teks_file)
