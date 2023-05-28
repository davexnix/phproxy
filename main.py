from flask import Flask, request
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

import requests

app = Flask(__name__)

@app.route('/')
def home():
    load = request.args.get('load')

    if not load:
        ipif = requests.get('https://api.ipify.org/')
        if ipif.status_code == 200:
            ipif = ipif.text.strip()
            load = 'http://ip-api.com/json/' + ipif
        else:
            load = 'https://api.ipify.org/'

    response = requests.get(load)
    soup = BeautifulSoup(response.content, 'html.parser')

    main_load = urlparse(load)
    main_load = f"{main_load.scheme}://{main_load.netloc}"

    
    body_tag = soup.find('body')
    script_tag = soup.new_tag('script')
    script_tag.string = '''
    document.addEventListener("DOMContentLoaded", function(event){
        const a = document.querySelectorAll("a");

        if (a) {
            a.forEach((el) => {
                if (el.href && !el.href.includes('load')) {
                    const brl = window.location.protocol + "//" + window.location.host;
                    const url = el.href.replace(brl, "");
                    el.href = brl + "?load=" + "#HOST_URL_ORI#" + url;
                }
            });
        }
    });
    '''.replace('#HOST_URL_ORI#', main_load)
    if body_tag:
        body_tag.insert(len(body_tag.contents), script_tag)

    return str(soup)

if __name__ == "__main__":
    app.run(debug=True)
