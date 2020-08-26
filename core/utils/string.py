
def words_separator(words_list, sep=", ", end_sep=" and "):
    """Words Separator

    Args:
        words_list (list): list of words
        sep (str): word separator
        end_sep (str): end word separator

    Returns:
        str: list of words separated. e.g. "1, 2, 3 and 4"
    """

    if len(words_list) > 1:
        return f"{sep.join(words_list[:-1])}{end_sep}{words_list[-1]}"
    try:
        return words_list[0]
    except IndexError as e:
        raise ValueError('Must pass at least one element in words_list') from e
