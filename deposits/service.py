

def hide_owner_info(owner_info: tuple) -> str:
    return [i[:1] + '*' * len(i[1:]) if 3 > len(i) > 1 else i[:2] + '*' * len(i[2:]) for i in owner_info]
    