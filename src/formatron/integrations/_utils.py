import re
import typing


def _multiple_replace(replacements, text):
    # Create a regular expression from the dictionary keys
    regex = re.compile(b"(%s)" % b"|".join(map(re.escape, replacements.keys())))
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo:replacements.get(mo.group(), b""), text)

Processors = set[typing.Literal["sentencepiece", "<0xHH>", "dot_G"]]

def _autodetect_processors(vocab:typing.Dict[str, int]):
    result = set()
    space_present = any(i.find(' ')!=-1 for i in vocab.keys())
    llama_present = any(i.find('<0xF0>')!=-1 for i in vocab.keys())
    underscore_present = any(i.find('\u2581')!=-1 for i in vocab.keys())
    g_present = any(i.find('\u0120')!=-1 for i in vocab.keys())
    if llama_present:
        result.add("<0xHH>")
    if not space_present and underscore_present:
        result.add("sentencepiece")
    elif not space_present and g_present:
        result.add("dot_G")
    return result

def get_original_characters(vocab:typing.Dict[str, int]) -> typing.Dict[bytes, int]:
    old_char_to_new_char = {}
    processors = _autodetect_processors(vocab)
    for i in processors:
        if i == "sentencepiece":
            old_char_to_new_char["\u2581".encode("UTF-8")] = b" "
        elif i == "dot_G":
            old_char_to_new_char["\u0120".encode("UTF-8")] = b" "
        elif i == "<0xHH>":
            for j in range(256):
                old_char_to_new_char[("<0x"+f"{j:02x}".upper()+">").encode("UTF-8")] = bytes([j])
        else:
            raise ValueError(f"{i} is not a valid processor name!")
    new_vocab = {}
    for k in vocab:
        token_id = vocab[k]
        k = k.encode("UTF-8")
        new_k = _multiple_replace(old_char_to_new_char, k)
        new_vocab[new_k] = token_id
    return new_vocab