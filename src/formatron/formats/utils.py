VALID_IDENTIFIER_CHARACTERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"

def escape_identifier(s: str) -> str:
    """
    For each character in the string, if it is a valid kbnf identifier character,
    add it to the result. Otherwise, add its Unicode code point to the result.

    Args:
        s: The string to escape.

    Returns:
        The escaped string.

    Examples:
        >>> escape_identifier("hello")
        "hello"
        >>> escape_identifier("hello_world")
        "hello_world"
        >>> escape_identifier("hello world")
        "hellou20world"
    """
    result = []
    for c in s:
        if c in VALID_IDENTIFIER_CHARACTERS:
            result.append(c)
        else:
            result.append(f"u{ord(c):x}")
    return "".join(result)