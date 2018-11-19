def xinggan(start, end):
    for page in range(start, end+1):
        yield 'https://www.uumtu.com/xinggan/list_' + str(page) + '.html'