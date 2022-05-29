def truncate(string, max_n_chars: int):
    assert max_n_chars > 3

    if len(string) <= max_n_chars:
        return string
    else:
        return f'{string[:max_n_chars - 3]}...'
