# deal with format
def sep_table(str, len_line):
        i = 0
        str_list = list(str)
        while i < len(str_list):
            if i%len_line == 0 and i:
                # if str[i].isalpha():

                str_list.insert(i, "<br>")
                i += 1
            i += 1
        str = "".join(str_list)
        return str
    

def sep_cont(content):
    cont_list = content.split()
    return cont_list