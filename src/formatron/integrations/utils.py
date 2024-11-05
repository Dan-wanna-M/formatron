import re
import typing
from functools import lru_cache

__all__ = ["get_original_characters", "update_vocab_0xHH", "update_vocab_sentencepiece", "update_vocab_dot_G"]

def _multiple_replace(replacements: typing.Dict[bytes, bytes], regex: re.Pattern[bytes], text: bytes) -> bytes:
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: replacements[mo.group()], text)


def get_original_characters(vocab: typing.Dict[str, int],
                            processors: typing.Optional[list[typing.Callable]] = None) -> typing.Dict[int, bytes]:
    """
    Get a vocabulary of original characters unmangled to raw UTF-8 bytes by the provided processors.

    Args:
        vocab: The mangled vocabulary.
        processors: List of callables with signature (token_to_char: typing.Dict[bytes, bytes])->None.
            Callables can be used to "unmangle" encoded characters to original characters. If None, processors will be auto-detected.
    """
    old_char_to_new_char = {}
    assert len(set(vocab.values())) == len(vocab), "Vocabulary contains duplicate token IDs!"
    if processors is None:
        processors = autodetect_processors(vocab)
    for update_vocab in processors:
        update_vocab(old_char_to_new_char)
    # Create a regular expression from the dictionary keys with longest keys first to avoid conflicts
    regex = re.compile(b"(%s)" % b"|".join(sorted(list(map(re.escape, old_char_to_new_char.keys())), key=lambda x: len(x), reverse=True)))
    new_vocab = {}
    for k in vocab:
        token_id = vocab[k]
        new_k = _multiple_replace(old_char_to_new_char, regex, k.encode("UTF-8"))
        new_vocab[token_id] = new_k
    return new_vocab


def autodetect_processors(vocab: typing.Dict[str, int]) -> typing.List[typing.Callable]:
    """
    Autodetect vocabulary processors.
    """
    result = []
    llama_present = any(i.find('<0xF0>') != -1 for i in vocab.keys())
    underscore_present = (len([1 for i in vocab.keys() if i.find('\u2581') != -1]) / len(vocab)) > 0.2
    g_present = (len([1 for i in vocab.keys() if i.find('\u0120') != -1]) / len(vocab)) > 0.2
    if llama_present:
        result.append(update_vocab_0xHH)
    if underscore_present:
        result.append(update_vocab_sentencepiece)
    elif g_present:
        result.append(update_vocab_dot_G)
    return result


def update_vocab_0xHH(token_to_char: typing.Dict[bytes, bytes]):
    """
    Vocabulary processor for <0xHH> tokens (used in llama tokenizers)
    """
    for j in range(256):
        token_to_char[("<0x" + f"{j:02x}".upper() + ">").encode("UTF-8")] = bytes([j])


def update_vocab_sentencepiece(token_to_char: typing.Dict[bytes, bytes]):
    """
    Vocabulary processor for ▁ token (used in sentencepiece tokenizers)
    """
    token_to_char["\u2581".encode("UTF-8")] = b" "


def update_vocab_dot_G(token_to_char: typing.Dict[bytes, bytes]):
    """
    Vocabulary processor for GPT2 style token mangling, like from \\n to Ġ(used in huggingface bytelevel preprocessors)
    """
    token_to_char.update(_huggingface_bytelevel_decoder())


@lru_cache()
def _huggingface_bytelevel_decoder():
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
