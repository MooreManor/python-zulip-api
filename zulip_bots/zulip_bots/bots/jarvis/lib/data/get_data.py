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
        "-h/--help",
        "-e/--examples",
        "<url>",
        "-p/--paper <url>/<paper-title>",
        "-s/--server <server-id>"
    ]

    max_len = 20
    params_help= [
        "**None**",
        "**None**",
        "**<url>:** Paper homepage url from arxiv, paperswithcode, iccv, cvpr",
        "**<url>:** Paper homepage url from arxiv, paperswithcode, iccv, cvpr; **<paper-title>:** Paper title",
        "**<server-id>:** Currently only support 0 or 1",
    ]
    # self.params_help  =[
    #     self.sep_table(i, max_len) 
    #     for i in self.params_help
    # ]

    descriptions_help = [
        f"Display {name} usage",
        f"Display {name} examples",
        "Get paper info with url",
        "Get paper info with url or paper title",
        "Get server info",
    ]
    for command, param, description in zip(commands_help, params_help, descriptions_help):
        content += f"| **{command}** | {param} | {description}\n"
    return content

def get_examples(name):
    content = "**Here are some examples about how to use Jarvis Bot.**\n"
    pic_url = [
        "https://github.com/MooreManor/Image/blob/main/img/zulip/jarvisBot-help.png",
        "https://github.com/MooreManor/Image/blob/main/img/zulip/jarvisBot-paper.png",
        "https://github.com/MooreManor/Image/blob/main/img/zulip/jarvisBot-server.png",
    ]
    content += f"You can get access to Jarvis Bot by creating a private chat with the bot or use `@**{name}**` in the channel.\n"
    content += f"## Instrcutions\nYou can get the instruction book through `@**{name}** --help`.\n\n{pic_url[0]}\n"
    content += f'## Get paper info\nYou can get a quick info through typing in paper homepage url from arxiv, paperswithcode, iccv and cvpr, or paper name.\n\n{pic_url[1]}\n'
    content += f'## Get VPX server info\nGet server info.\n\n{pic_url[2]}\n'
    return content


def get_paper(para, type=0):
    """
    Get paper info

    Args
        para: url or paper_title
        type: 0 means url; 1 means paper_title
    Returns
        res: paper info
    """
    if type==0:
        if "arxiv" in para:
            title, authors, comment, pdf, url, code, paperswithcode = analyze_arxiv(para)
        elif "paperswithcode" in para:
            title, authors, comment, pdf, url, code, paperswithcode = analyze_paperswithcode(para)
        elif "iccv" or "cvpr" in para:
            title, authors, comment, pdf, url, code, paperswithcode = analyze_cv(para)
    elif type==1:
        PWC_search_url = search_paper_name_PWC(para)
        PWC_url = get_PWChomeUrl_with_searchUrl(PWC_search_url)
        title, authors, comment, pdf, url, code, paperswithcode = analyze_paperswithcode(PWC_url)
        
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
    # cpolar ip, the last part will change so match the first three 
    ip_list=[
        "222.66.117",
        "49.52.5",
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
        # server_chosen_id = ip.index(ip_list[int(server_id)])
        for i, cr_ip in enumerate(ip):
            if ip_list[int(server_id)] in cr_ip:
                server_chosen_id = i
                break
        server_chosen_tcp = tcp[server_chosen_id]
        cmd_out = f'ssh {usr_name}@1.tcp.cpolar.cn -p {server_chosen_tcp[-5:]}'
    except:
        cmd_out = 'The service is not open currently.'
    cmd_vpn = f'ssh {usr_name}@{vpn_list[int(server_id)]}'
    return cmd_out, cmd_vpn