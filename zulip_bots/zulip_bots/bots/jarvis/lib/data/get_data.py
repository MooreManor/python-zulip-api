#-----------------------------Get data-----------------------------
from .arxiv_markdown import *
from . import cpolar

import configparser

def get_help(name):
    content = "**Available Commands:** \n\n"
    
    content += "| Commands | Params | Description |\n"
    content += "| :--: | :--: | :--: |\n"
    # |  a   |  b   |  c   |
    # | :--: | :--: | :--: |
    # |  aa  |  bb  |  cc  |
    commands_help = [
        "help",
        # "paper <url>",
        "<url>",
        "server <server-id>"
    ]

    max_len = 20
    params_help= [
        "**None**",
        "**<url>:** Paper homepage url from arxiv, paperswithcode, iccv, cvpr",
        "**<server-id>:** Currently only support 0 or 1",
    ]
    # self.params_help  =[
    #     self.sep_table(i, max_len) 
    #     for i in self.params_help
    # ]

    descriptions_help = [
        f"Display {name} usage",
        "Get paper info",
        "Get server info",
    ]
    for command, param, description in zip(commands_help, params_help, descriptions_help):
        content += f"| **{command}** | {param} | {description}\n"
    return content

def get_paper(url):
    if "arxiv" in url:
        title, authors, comment, pdf, url, code, paperswithcode = analyze_arxiv(url)
    elif "paperswithcode" in url:
        title, authors, comment, pdf, url, code, paperswithcode = analyze_paperswithcode(url)
    elif "iccv" or "cvpr" in url:
        title, authors, comment, pdf, url, code, paperswithcode = analyze_cv(url)
        
    res = "**" + title + "**" + " " + authors + " " + comment + " " + "([PDF](" + pdf + "))" + " " + \
        "([Abstract](" + url + "))" + paperswithcode + code
    return res

def get_cpolar(sender_email, server_id):
    email_list=[
        "liziqing9908@126.com",
        "yanglibingqaq@qq.com",
        "1524552292@qq.com",
        "bo23333@outlook.com",
    ]
    usr_list=[
        "zqli",
        "lbyang",
        "xyyang",
        "dblu",
    ]
    # cpolar ip
    ip_list=[
        "222.66.117.28",
        "49.52.5.37",
    ]
    # server ip
    vpn_list=[
        "49.52.10.55",
        "172.23.148.41",
    ]
    cmd_out = ''
    cmd_vpn = ''

    cf = configparser.ConfigParser()
    cf.read("/home/zqli/workspace/python/server/python-zulip-api/zulip_bots/zulip_bots/bots/jarvis/configs/config.ini")
    usr, pwd = cpolar.get_cpolar_config(cf)
    tcp, ip = cpolar.get_tcp(usr, pwd)
    if sender_email in email_list:
        id = email_list.index(sender_email)
        # print(id)
        usr_name = usr_list[id]
        # server_chosen_tcp = tcp[int(server_id)]
    else:
        usr_name = "<usr_name>"

    try:
        server_chosen_id = ip.index(ip_list[int(server_id)])
        server_chosen_tcp = tcp[server_chosen_id]
        cmd_out = f'ssh {usr_name}@1.tcp.cpolar.cn -p {server_chosen_tcp[-5:]}'
    except:
        cmd_out = 'The service is not open currently.'
    cmd_vpn = f'ssh {usr_name}@{vpn_list[int(server_id)]}'
    return cmd_out, cmd_vpn