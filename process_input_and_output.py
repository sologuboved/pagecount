from pages_per_chapter import prettyprint_count

INVALID_INPUT = 'Invalid Input!'


def process_pages(user_input):
    try:
        pages = list(map(int, user_input.split()))
    except ValueError as e:
        # print(isinstance(e, Exception))
        return e
    # prettyprint_count(pages)
    return True


if __name__ == '__main__':
    process_pages('1 2 3')
