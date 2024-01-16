STR_CLASS_LENGHT = 20


def cut_str(func,
            length: int = STR_CLASS_LENGHT):
    def wrapper(*args):
        str_res = func(*args)
        if len(str_res) < length:
            return str_res
        return str_res[:length] + '...'
    return wrapper
