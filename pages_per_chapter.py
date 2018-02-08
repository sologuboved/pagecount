def count_pages(pages):
    count = dict()
    start = pages[0]
    next_index = 1
    while next_index < len(pages):
        finish = pages[next_index]
        if start == finish:
            next_index += 1
            continue
        count[start] = finish - start
        start = finish
        next_index += 1
    return count


def groupcount_pages(pages):
    groupcount = dict()
    count = count_pages(pages)
    for val in count.values():
        groupcount[val] = groupcount.get(val, 0) + 1
    return groupcount


def fill_in_zeros(num):
    num = str(num)
    return num + ':' + ' ' * (10 - len(num))


def prettyprint_count(pages, grouped=False, sort_by_val=False):
    if grouped:
        count = list(groupcount_pages(pages).items())
    else:
        count = list(count_pages(pages).items())
    if sort_by_val:
        index = 1
    else:
        index = 0
    count.sort(key=lambda p: p[index])
    for page, length in count:
        print("%s %d" % (fill_in_zeros(page), length))


if __name__ == '__main__':
    m_d = (17, 21, 24, 37, 40, 42, 44, 47, 49, 57, 60, 61, 63, 67, 69, 71, 83, 88, 91, 94, 96, 99, 102, 103, 107, 108,
           110, 114, 117, 119, 120, 122, 133, 135, 140, 145, 152, 153, 154, 155, 161, 169, 176, 177, 181, 189, 191, 193,
           202, 203, 206, 209, 211, 214, 231, 235, 238, 240, 243, 245, 248, 252, 253, 254, 261, 263, 264, 266, 268, 269,
           271, 276, 280, 285, 288, 291, 293, 294, 298, 300, 302, 311, 313, 315, 317, 321, 325, 335, 338, 341, 344, 349,
           351, 355, 358, 359, 363, 363, 365, 370, 376, 380, 384, 386, 389, 392, 394, 397, 400, 402, 407, 408, 410, 413,
           414, 416, 418, 419, 421, 426, 427, 428, 428, 431, 434, 436, 439, 441, 444, 445, 449, 450, 454, 461, 469, 479,
           480)
    dervish = (19, 23, 37, 45, 63, 93, 117, 140, 154, 177, 204, 209, 224, 255, 270, 285)
    tvrdjava = (325, 332, 343, 361, 377, 397, 413, 425, 437, 451, 463, 478, 493, 513, 528, 549, 567, 584, 599)
    phen = (1, 13, 45, 69, 89, 107, 129, 153, 171, 197, 217)

    # prettyprint_count(dervish, grouped=False, val=False)
    # prettyprint_count(tvrdjava, grouped=False, val=False)
    prettyprint_count(phen, grouped=True, sort_by_val=False)


