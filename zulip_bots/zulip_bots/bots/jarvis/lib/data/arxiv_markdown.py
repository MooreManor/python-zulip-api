'''
This file is used to generate markdown format titles, authors, PDF links, Abstract links, Paperswithcode and Github links from the input ArXiv website. The text will be copied to clipboard. Use ctrl+v to paste it in markdown.
@usage: python arxiv_markdown.py param
@param: website of papers in arxiv/Paperswithcode
@example: python arxiv_markdown.py https://arxiv.org/abs/2105.02465
          python arxiv_markdown.py https://paperswithcode.com/paper/multi-scale-networks-for-3d-human
'''


import requests
from bs4 import BeautifulSoup
import re
import pyperclip
import sys
import os

def analyze_arxiv(url):

    resp = requests.get(url)
    page = BeautifulSoup(resp.text, "html.parser")
    sub_url = url[url.rfind('/') + 1:]

    # print(page)
    table = page.find(class_="tablecell comments mathjax")
    # # print(table)
    # code = re.findall(r"https://github.com.*?\"", str(page))
    # # code = re.search(r"https://github.com.*?\"", str(table))
    # code.sort(key = lambda i:len(i))
    # # print(code)
    # if code != None:
    #     code = code[0][:-1]
    #     code = " ([Code](" + code + "))"
    #     # print(code)
    # else:
    #     code = ''
    sub_url = f"https://arxiv.paperswithcode.com/api/v0/repos-and-datasets/{sub_url}"
    res = requests.get(sub_url)
    code = ''
    try:
        datas = res.json()['code']['all_official']
        assert len(datas)==1
        code = datas[0]['url']
        code = " ([Code](" + code + "))"
    except:
        pass


    paperswithcode = res.json()['data']['paper_url']
    paperswithcode = " ([PWC](" + paperswithcode + "))"

    # comment = re.search(r"CVPR.....", str(table))
    # comment = re.search(r"CVPR|ICCV|SIGGRAPH|ECCV|ACM-MM|AAAI", str(table))
    comment = re.search(r"[^> ]* \d{4}", str(table))

    if comment != None:
        comment = comment.group()
        comment = "**" + comment + "**"
        # print(comment)
    else:
        year = page.find('div', class_='dateline')
        year = str(year).replace("\n", "")
        year = re.search(r">.*?<", str(year))
        year = year.group()[1:-1].lstrip().rstrip()[14:-1]
        comment = "**" + year + "**"

    # author = page.find(class_="authors")
    authors = ""
    num_authors = 0
    for ss0 in page.find_all(class_="authors"):
        ss1 = ss0.find_all('a')
        num_authors = len(ss1)
        for i, ii in enumerate(ss1):
            if(num_authors<=2 and i<2):
                authors = authors+ii.string+', '
            elif(num_authors>2 and i==0):
                authors = authors + ii.string + ', '
                # print(ii.string)

    authors = authors[:-2]
    if(num_authors > 2):
        authors = authors + " et. al."
    else:
        authors = authors + "."
    # print(num_authors)
    # print(authors)

    title = page.find(class_="title mathjax")
    title = re.search(r"</span>.*?</h1>", str(title))
    title = title.group()[7:-5]
    title = title + '.'

    pdf = "https://arxiv.org/pdf/" + url.split("/")[-1]
    return title, authors, comment, pdf, url, code, paperswithcode
# print(title)

def analyze_paperswithcode(url):

    resp = requests.get(url)
    paperswithcode = url
    paperswithcode = " ([PWC](" + paperswithcode + "))"

    page = BeautifulSoup(resp.text, "html.parser")
    # print(page)
    abstract = page.find('div', class_='paper-abstract').find('div', class_='col-md-12')
    # print(abstract)
    # print(abstract.find_all('div',class_='badge badge-light'))
    urls = []
    for i in abstract.find_all('a', class_='badge badge-light'):
        urls.append(i['href'])
    if(len(urls) == 2):
        pdf = urls[0]
        url = urls[1]
    elif(len(urls) == 4):
        pdf = urls[2]
        url = urls[1]

    title = page.find('div', class_='paper-title').find('div', class_='col-md-12').find('h1')
    title = str(title)[4:-5].lstrip().rstrip() + '.'

    try:
        code = page.find('div', class_='paper-implementations code-table').find('div', class_='paper-impl-cell').find('a')
        code = re.search(r"href=\".*?\"", str(code))
        code = code.group()[6:-1]
        code = " ([Code](" + code + "))"
    except:
        code=""
    
    try:
        # pub = page.find('div', class_='authors').find('span', class_='item-conference-link').find("a")
        pub = page.find('div', class_='paper-title').find('span', class_='item-conference-link').find('a')
        # print(pub)
        # print(str(pub).replace(' ', ''))
        # print(re.search(r">.*?<", str(pub).replace(' ', '').replace('\n', '')).group())
        # pub = re.search(r">.*?<", str(pub)).group()[1:-1]
        # pub = re.search(r">.*?<", str(pub).replace(' ', '').replace('\n', '')).group()[1:-1]
        pub = re.search(r">.*?<", str(pub).replace('\n', '')).group()
        # print(pub)
        # print(re.search(r"CVPR|ICCV|SIGGRAPH|ECCV|ACM-MM|AAAI", pub))
        # comment = re.search(r"CVPR|ICCV|SIGGRAPH|ECCV|ACM-MM|AAAI", pub)
        comment = re.search(r"[^> ]* \d{4}", pub)
        # print(comment)
        # year = re.search(r"\d{4}", pub)
        if comment!=None:
            comment = "**" + comment.group() + "**"
        else:
            comment = ""
    except:
        comment=""
    # print(comment.group())
    # print(year.group())

    authors = ""
    num_authors = 0
    ss1 = [i.find_all('a') for i in page.find_all(class_="author-span")]
    # print(ss1)
    if len(ss1[0])==0:
        ss1.pop(0)
        comment = re.search(r">.*?<", str(page.find(class_="author-span"))).group()[1:-1]
        comment = "**" + comment + "**"
    num_authors = len(ss1)
    for i, ii in enumerate(ss1):
        if (num_authors <= 2 and i < 2):
            authors = authors + ii[0].string + ', '
        elif (num_authors > 2 and i == 0):
            authors = authors + ii[0].string + ', '
    authors = authors[:-2]
    if (num_authors > 2):
        authors = authors + " et. al."
    else:
        authors = authors + "."

    return title, authors, comment, pdf, url, code, paperswithcode
# print(pdf)

def analyze_cv(url):
    resp = requests.get(url)
    page = BeautifulSoup(resp.text, "html.parser")
    for ss0 in page.find_all('a'):
        if "arxiv" in str(ss0):
            title, authors, comment, pdf, url, code, paperswithcode = analyze_arxiv((ss0['href']))
            return title, authors, comment, pdf, url, code, paperswithcode




def get_newest_pdf(path):
    list_pdf = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".pdf"):
                # print(os.path.join(root, file))
                list_pdf.append(os.path.join(root, file).replace('\\', '/'))
    # print(list)
    list_pdf.sort(key=lambda fn:os.path.getmtime(fn))  # 按时间排序
    file_new = os.path.join(path,list_pdf[-1]) # 获取最新的文件保存到file_new
    return file_new

def get_specify_pdf(path, pdf_name):
    list_pdf = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".pdf") and file == pdf_name:
                # print(os.path.join(root, file))
                return (os.path.join(root, file).replace('\\', '/'))
    raise FileNotFoundError

if __name__ == '__main__':
    # url = "https://arxiv.org/abs/2105.02465"
    # url = "https://arxiv.org/abs/2109.03462"

    path = 'D:/阅读论文'
    url = "https://paperswithcode.com/paper/multi-scale-networks-for-3d-human"
    # url = "https://paperswithcode.com/paper/poseaug-a-differentiable-pose-augmentation"
    # if (len(sys.argv) == 2):
    #     url = sys.argv[1]

    import argparse
    parser = argparse.ArgumentParser(description='Url, local path')
    parser.add_argument("-u", "--url", help="website of paper")
    parser.add_argument("-n", "--not_local", action="store_true",help="whether to generate local path to the pdf")
    parser.add_argument("-p", "--path", help="the directory of papers stored")
    args = parser.parse_args()

    import time
    test_time = time.time()
    if args.url:
        url = args.url
    if args.not_local == False:
        if args.path:
            path = args.path
        pdf_path = get_newest_pdf(path)
        pdf_path = " " + "([Local](" + pdf_path + "))"
    else:
        pdf_path = ''
    assert (time.time()-test_time)<3, 'Sorting time too long! Please change a smaller local directory!'

    if "arxiv" in url:
        title, authors, comment, pdf, url, code, paperswithcode = analyze_arxiv(url)
    elif "paperswithcode" in url:
        title, authors, comment, pdf, url, code, paperswithcode = analyze_paperswithcode(url)
    elif "iccv" or "cvpr" in url:
        title, authors, comment, pdf, url, code, paperswithcode = analyze_cv(url)

    res = "<mark>" + "**" + title + "**" + " " + authors + " " + comment + " " + "([PDF](" + pdf + "))" + " " + \
          "([Abstract](" + url + "))" + paperswithcode + code + pdf_path + "</mark>" + "\n<details>\n" + \
            "   <summary>Contents</summary>\n" + \
            "   <ul>\n" + \
            "	    <li></li>\n" + \
            "   </ul>\n" + \
            "</details>"
    print(res)

    pyperclip.copy(res)