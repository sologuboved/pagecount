from pages_per_chapter import count_pages, group_count, fill_in_blanks


def check_pages(user_input):
    pages = list(map(int, user_input.split()))
    if len(pages) < 2:
        raise ValueError("too few pages")
    if sorted(pages) != pages:
        raise ValueError("wrong order")
    return pages


def get_count(user_input):
    try:
        pages = check_pages(user_input)
    except ValueError as e:
        return e
    count = count_pages(pages)
    return count


def convert_arg(arg):
    return {'Yes': True, 'No': False}[arg]


def produce_output(count, group, by_val):
    if group:
        count = group_count(count)
    count = list(count.items())
    if by_val:
        ind = 1
    else:
        ind = 0
    count.sort(key=lambda p: p[ind])
    output = str()
    for page, length in count:
        output += "{page} {length}\n".format(page=fill_in_blanks(page), length=length)
    return output
