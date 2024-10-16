import re
import typing
from functools import lru_cache


def _multiple_replace(replacements: typing.Dict[bytes, bytes], regex: re.Pattern[bytes], text: bytes) -> bytes:
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: replacements[mo.group()], text)


Processors = set[typing.Literal["sentencepiece", "<0xHH>", "dot_G"]]


def _autodetect_processors(vocab: typing.Dict[str, int]) -> list[tuple[str, typing.Callable]]:
    result = []
    llama_present = any(i.find('<0xF0>') != -1 for i in vocab.keys())
    underscore_present = (len([1 for i in vocab.keys() if i.find('\u2581') != -1]) / len(vocab)) > 0.2
    g_present = (len([1 for i in vocab.keys() if i.find('\u0120') != -1]) / len(vocab)) > 0.2
    if llama_present:
        def update_vocab(old_char_to_new_char):
            for j in range(256):
                old_char_to_new_char[("<0x" + f"{j:02x}".upper() + ">").encode("UTF-8")] = bytes([j])
        result.append(("<0xHH>", update_vocab))
    if underscore_present:
        def update_vocab(old_char_to_new_char):
            old_char_to_new_char["\u2581".encode("UTF-8")] = b" "
        result.append(("sentencepiece", update_vocab))
    elif g_present:
        def update_vocab(old_char_to_new_char):
            old_char_to_new_char.update(huggingface_bytelevel_decoder())
        result.append(("dot_G", update_vocab))
    return result


def get_original_characters(vocab: typing.Dict[str, int], processors: typing.Optional[list[tuple[str, typing.Callable]]] = None) -> typing.Dict[int, bytes]:
    old_char_to_new_char = {}
    assert len(set(vocab.values())) == len(vocab), "Vocabulary contains duplicate token IDs!"
    if processors is None:
        processors = _autodetect_processors(vocab)
    for processor, update_vocab in processors:
        update_vocab(old_char_to_new_char)
    # Create a regular expression from the dictionary keys with longest keys first to avoid conflicts
    regex = re.compile(b"(%s)" % b"|".join(sorted(list(map(re.escape, old_char_to_new_char.keys())), key=lambda x: len(x), reverse=True)))
    new_vocab = {}
    for k in vocab:
        token_id = vocab[k]
        new_k = _multiple_replace(old_char_to_new_char, regex, k.encode("UTF-8"))
        new_vocab[token_id] = new_k
    return new_vocab


@lru_cache()
def huggingface_bytelevel_decoder():
    """
    I hate legacy code.
    """
    bs = list(range(ord("!"), ord("~")+1))+list(range(ord("¡"), ord("¬")+1))+list(range(ord("®"), ord("ÿ")+1))
    cs = bs[:]
    n = 0
    for b in range(2**8):
        if b not in bs:
            bs.append(b)
            cs.append(2**8+n)
            n += 1
    cs = [chr(n).encode("UTF-8") for n in cs]
    for i in range(len(bs)):
        bs[i] = bytes([bs[i]])
    return dict(zip(cs, bs))