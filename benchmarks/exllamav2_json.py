from timeit import timeit
import formatron.integrations.exllamav2
from exllamav2 import ExLlamaV2, ExLlamaV2Config, ExLlamaV2Cache, ExLlamaV2Tokenizer
from exllamav2.generator.base import ExLlamaV2Filter
from exllamav2.generator import ExLlamaV2DynamicGenerator, ExLlamaV2Sampler
from formatron.formatter import FormatterBuilder
from formatron.integrations.exllamav2 import create_formatter_filter
from lmformatenforcer.integrations.exllamav2 import ExLlamaV2TokenEnforcerFilter
from utils import load_address, load_linkedlist, load_orders, force_gc, address_lfe, linked_list_lfe, \
    order_lfe
from utils import LinkedList
from utils import Address, BenchResult, Context, log
from utils import Order


def create_exllamav2_6bpw_llama3_8b():
    model_dir = "../tests/local_assets/Meta-Llama-3-8B-Instruct-32k/"
    config = ExLlamaV2Config(model_dir)
    model = ExLlamaV2(config)
    cache = ExLlamaV2Cache(model, max_seq_len=4096, lazy=True)
    model.load_autosplit(cache, progress=True)
    tokenizer = ExLlamaV2Tokenizer(config)
    generator = ExLlamaV2DynamicGenerator(
        model=model,
        cache=cache,
        tokenizer=tokenizer,
    )
    return generator


def create_exllamav2_4bpw_llama2_7b():
    model_dir = "../tests/local_assets/Mistral-7B-Instruct-v0.3/"
    config = ExLlamaV2Config(model_dir)
    model = ExLlamaV2(config)
    cache = ExLlamaV2Cache(model, max_seq_len=4096, lazy=True)
    model.load_autosplit(cache, progress=True)
    tokenizer = ExLlamaV2Tokenizer(config)
    generator = ExLlamaV2DynamicGenerator(
        model=model,
        cache=cache,
        tokenizer=tokenizer,
    )
    return generator


def f_get_address_filter():
    f = FormatterBuilder()
    f.append_line(f"{f.json(Address, capture_name='json')}")
    exllama_filter = create_formatter_filter(
        generator.model, generator.tokenizer, f)
    return exllama_filter

# adapted from https://gist.github.com/floer32/a928b801ca5c7705e94e
def bind(instance, func, as_name):
    """ Turn a function to a bound method on an instance
    .. doctest::
        >>> class Foo(object):
        ...     def __init__(self, x, y):
        ...         self.x = x
        ...         self.y = y
        >>> foo = Foo(2, 3)
        >>> my_unbound_method = lambda self: self.x * self.y
        >>> bind(foo, my_unbound_method, 'multiply')
        >>> # noinspection PyUnresolvedReferences
        ... foo.multiply()
        6
    :param instance: some object
    :param func: unbound method (i.e. a function that takes `self` argument, that you now
        want to be bound to this class as a method)
    :param as_name: name of the method to create on the object
    SIDE EFFECTS:
        - creates the new bound method on this instance, like you asked for
    """
    setattr(instance, as_name, func.__get__(instance, instance.__class__))

def monkey_patch_lfe(exllama_filter: ExLlamaV2TokenEnforcerFilter):
    exllama_filter.background_result = None
    use_background_worker = lambda self: True
    bind(exllama_filter, use_background_worker, "use_background_worker")
    bind(exllama_filter, ExLlamaV2Filter.background_next, "background_next")
    bind(exllama_filter, ExLlamaV2Filter.background_drop, "background_drop")
    bind(exllama_filter, ExLlamaV2Filter.get_next, "get_next")


def lfe_get_address_filter():
    exllama_filter = ExLlamaV2TokenEnforcerFilter(
        address_lfe, generator.tokenizer)
    monkey_patch_lfe(exllama_filter)
    return exllama_filter


def f_get_linkedlist_filter():
    f = FormatterBuilder()
    f.append_line(f"{f.json(LinkedList, capture_name='json')}")
    exllama_filter = create_formatter_filter(
        generator.model, generator.tokenizer, f)
    return exllama_filter


def lfe_get_linkedlist_filter():
    exllama_filter = ExLlamaV2TokenEnforcerFilter(
        linked_list_lfe, generator.tokenizer)
    monkey_patch_lfe(exllama_filter)
    return exllama_filter


def f_get_order_filter():
    f = FormatterBuilder()
    f.append_line(f"{f.json(Order, capture_name='json')}")
    exllama_filter = create_formatter_filter(
        generator.model, generator.tokenizer, f)
    return exllama_filter


def lfe_get_order_filter():
    exllama_filter = ExLlamaV2TokenEnforcerFilter(
        order_lfe, generator.tokenizer)
    monkey_patch_lfe(exllama_filter)
    return exllama_filter


def execute():
    prompt = f"""{system_prompt}{inputs[context.index]}{tail}\n\nHere is the extracted information in JSON format:\n\n```\n"""
    output = generator.generate(
        prompt=prompt,
        max_new_tokens=max_new_tokens,
        gen_settings=settings,
        decode_special_tokens=True,
        add_bos=False,
        filters=context.filters,
        completion_only=True,
    )
    # print(repr(output)) # for debug purpose
    context.index += 1
    if context.filters:
        if isinstance(context.filters[0], formatron.integrations.exllamav2.FormatterFilter):
            context.tokens += len(context.filters[0]._formatter._token_ids)
        elif isinstance(context.filters[0], ExLlamaV2TokenEnforcerFilter):
            context.tokens += len(list(filter(lambda x: x != generator.tokenizer.eos_token_id,
                                              context.filters[0].token_sequence)))+1
            # Remove all eos_token_id and supposes only one is generated
            # Currently lm format enforcer forces eos_token_id and does not stop until max_new_token,
            # which does not really contribute to effective tps.
        else:
            raise ValueError(f"Unsupported filter {type(context.filters[0])}")
    else:
        assert not output.endswith(
            generator.tokenizer.eos_token), "Something is wrong"
        context.tokens += max_new_tokens


def warm_up(f):
    f()
    context.index = 0
    context.tokens = 0


def bench(result: BenchResult, context: Context, func, bench_name: str, f):
    global settings
    context.index = 0
    context.tokens = 0
    result.s1 = (timeit(func, setup=lambda: warm_up(func), number=len(inputs)))
    result.t1 = context.tokens
    context.index = 0
    context.tokens = 0
    context.filters = None
    settings.disallow_tokens(generator.tokenizer, [
                             generator.tokenizer.eos_token_id])
    result.s2 = (timeit(func, number=len(inputs)))
    result.t2 = context.tokens
    settings = ExLlamaV2Sampler.Settings()
    log(bench_name, result, f)


if __name__ == '__main__':

    data = BenchResult(0, 0, 0, 0)
    context = Context(0, 0)
    with open("exllamav2_json.txt", "w") as f:
        generator = create_exllamav2_6bpw_llama3_8b()
        settings = ExLlamaV2Sampler.Settings()
        settings.disallow_tokens(generator.tokenizer, [
                                 generator.tokenizer.eos_token_id])
        generator.generate("Something", max_new_tokens=4080,
                           gen_settings=settings)  # warm up exllamav2 itself
        system_prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

        You are a helpful AI assistant for information extraction<|eot_id|><|start_header_id|>user<|end_header_id|>

        Extract information into json format: """
        tail = "<|eot_id|><|start_header_id|>assistant<|end_header_id|>```"
        settings = ExLlamaV2Sampler.Settings()
        # --------------------------------------------------------------------------------------------------------------
        inputs = load_address()
        context.filters = [f_get_address_filter()]
        max_new_tokens = 50
        bench(data, context, execute,
              "formatron_llama3_8b_6pw_exl2_address_json_exllamav2", f)
        context.filters = [lfe_get_address_filter()]
        bench(data, context, execute,
              "lm_format_enforcer_llama3_8b_6pw_exl2_address_json_exllamav2", f)
        # --------------------------------------------------------------------------------------------------------------
        context.filters = [f_get_linkedlist_filter()]
        inputs = load_linkedlist()
        max_new_tokens = 100
        bench(data, context, execute,
              "formatron_llama3_8b_6pw_exl2_linkedlist_json_exllamav2", f)
        context.filters = [lfe_get_linkedlist_filter()]
        bench(data, context, execute,
              "lm_format_enforcer_llama3_8b_6pw_exl2_linkedlist_json_exllamav2", f)
        # --------------------------------------------------------------------------------------------------------------
        context.filters = [f_get_order_filter()]
        inputs = load_orders()
        max_new_tokens = 256
        bench(data, context, execute,
              "formatron_llama3_8b_6pw_exl2_orders_json_exllamav2", f)
        context.filters = [lfe_get_order_filter()]
        bench(data, context, execute,
              "lm_format_enforcer_llama3_8b_6pw_exl2_orders_json_exllamav2", f)
        # --------------------------------------------------------------------------------------------------------------
        del generator
        force_gc()
        generator = create_exllamav2_4bpw_llama2_7b()
        settings = ExLlamaV2Sampler.Settings()
        settings.disallow_tokens(generator.tokenizer, [
                                 generator.tokenizer.eos_token_id])
        generator.generate("Something", max_new_tokens=4080,
                           gen_settings=settings)  # warm up exllamav2 itself
        settings = ExLlamaV2Sampler.Settings()
        system_prompt = """[INST]
                    You are a helpful AI assistant for information extraction.

                    Extract information into json format: """
        tail = "[/INST]```"
        # --------------------------------------------------------------------------------------------------------------
        inputs = load_address()
        context.filters = [f_get_address_filter()]
        max_new_tokens = 100
        bench(data, context, execute,
              "formatron_llama2_7b_4pw_exl2_address_json_exllamav2", f)
        context.filters = [lfe_get_address_filter()]
        bench(data, context, execute,
              "lm_format_enforcer_llama2_7b_4pw_exl2_address_json_exllamav2", f)
        # --------------------------------------------------------------------------------------------------------------
        context.filters = [f_get_linkedlist_filter()]
        inputs = load_linkedlist()
        max_new_tokens = 100
        bench(data, context, execute,
              "formatron_llama2_7b_4pw_exl2_linkedlist_json_exllamav2", f)
        context.filters = [lfe_get_linkedlist_filter()]
        bench(data, context, execute,
              "lm_format_enforcer_llama2_7b_4pw_exl2_linkedlist_json_exllamav2", f)
        # --------------------------------------------------------------------------------------------------------------
        context.filters = [f_get_order_filter()]
        inputs = load_orders()
        max_new_tokens = 350
        bench(data, context, execute,
              "formatron_llama2_7b_4pw_exl2_orders_json_exllamav2", f)
        context.filters = [lfe_get_order_filter()]
        bench(data, context, execute,
              "lm_format_enforcer_llama2_7b_4pw_exl2_orders_json_exllamav2", f)
