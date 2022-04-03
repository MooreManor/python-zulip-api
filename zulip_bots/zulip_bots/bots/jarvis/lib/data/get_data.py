#-----------------------------Get data-----------------------------
from .arxiv_markdown import *

def get_help(name):
    content = "**Available Commands:** \n\n"
    
    content += "| Commands | Params | Description |\n"
    content += "| :--: | :--: | :--: |\n"
    # |  a   |  b   |  c   |
    # | :--: | :--: | :--: |
    # |  aa  |  bb  |  cc  |
    commands_help = [
        "help",
        "paper <url>",
    ]

    max_len = 20
    params_help= [
        "**None**",
        "**<url>:** Paper url from arxiv, paperswithcode"
    ]
    # self.params_help  =[
    #     self.sep_table(i, max_len) 
    #     for i in self.params_help
    # ]

    descriptions_help = [
        f"Display {name} usage",
        "Get the paper archives from arxiv, paperswithcode",
    ]
    for command, param, description in zip(commands_help, params_help, descriptions_help):
        content += f"| **{command}** | {param} | {description}\n"
    return content

def get_paper(url):
    if "arxiv" in url:
        title, authors, comment, pdf, url, code, paperswithcode = analyze_arxiv(url)
    elif "paperswithcode" in url:
        title, authors, comment, pdf, url, code, paperswithcode = analyze_paperswithcode(url)
        
    res = "**" + title + "**" + " " + authors + " " + comment + " " + "([PDF](" + pdf + "))" + " " + \
        "([Abstract](" + url + "))" + paperswithcode + code
    return res