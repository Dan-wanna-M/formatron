# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['test_formatter 1'] = '''__choice_0_0_food ::= 'railroad' | 'orange' | 'banana';
__regex_1_0 ::= #'[0-9]+';
__regex_2_0 ::= #'[a-z]+';
__choice_3_0_ID ::= __regex_1_0 | __regex_2_0;
integer ::= #"-?(0|[1-9][0-9]*)";
number ::= #"-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
__json_4_0_json ::= object_begin \'"name"\' colon __json_4_0_json_name comma \'"weight"\' colon __json_4_0_json_weight comma \'"color"\' colon __json_4_0_json_color object_end;
__json_4_0_json_color ::= string;
__json_4_0_json_weight ::= number;
__json_4_0_json_name ::= string;

start ::= \'Today, I want to eat \' __choice_0_0_food \'\\n\' "My food\'s ID is " __choice_3_0_ID \'.\\n\' "\\nWhat\'s more, indentations\\nare handled\\nappropriately." \'My weight is 14.4kg and my color is pink. This is my personal info json: \' __json_4_0_json \'\\n\';'''

snapshots['test_formatter 2'] = '''Today, I want to eat orange
My food's ID is red.

What's more, indentations
are handled
appropriately.My weight is 14.4kg and my color is pink. This is my personal info json: {                                                                                                                                                                  '''

snapshots['test_formatter 3'] = {
}

snapshots['test_formatter_alternate_accept 1'] = {
    'age': GenericRepr("<re.Match object; span=(0, 2), match='30'>"),
    'name': GenericRepr("<re.Match object; span=(0, 5), match='John,'>")
}

snapshots['test_formatter_callable_schema 1'] = '''integer ::= #"-?(0|[1-9][0-9]*)";
number ::= #"-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
__json_0_0_json ::= object_begin \'"a"\' colon __json_0_0_json_a comma \'"b"\' colon __json_0_0_json_b comma \'"c"\' colon __json_0_0_json_c object_end;
__json_0_0_json_c ::= integer;
__json_0_0_json_b ::= integer;
__json_0_0_json_a ::= integer;

start ::= __json_0_0_json '\\n';'''

snapshots['test_formatter_callable_schema 2'] = '''{"a":1,"b":2,"c":3}
'''

snapshots['test_formatter_callable_schema 3'] = {
    'json': 6
}

snapshots['test_formatter_dict_inference 1'] = '''integer ::= #"-?(0|[1-9][0-9]*)";
number ::= #"-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
__json_0_0_json ::= object_begin \'"name"\' colon __json_0_0_json_name comma \'"gender"\' colon __json_0_0_json_gender object_end;
__json_0_0_json_gender ::= string;
__json_0_0_json_name ::= string;

start ::= __json_0_0_json '\\n';'''

snapshots['test_formatter_dict_inference 2'] = '''{"name":"A","gender":"male"}
'''

snapshots['test_formatter_dict_inference 3'] = {
    'json': {
        'gender': 'male',
        'name': 'A'
    }
}

snapshots['test_formatter_json_no_properties 1'] = {
    'data': {
        'key': 'value',
        'number': 42
    }
}

snapshots['test_formatter_json_schema 1'] = '''{"name":"A","age":30}
'''

snapshots['test_formatter_json_schema 2'] = {
    'json': {
        'age': 30,
        'name': 'A'
    }
}

snapshots['test_formatter_json_schema 3'] = '''integer ::= #"-?(0|[1-9][0-9]*)";
number ::= #"-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
__json_0_0_json ::= object_begin \'"name"\' colon __json_0_0_json_name comma \'"age"\' colon __json_0_0_json_age object_end;
__json_0_0_json_age ::= integer;
__json_0_0_json_name ::= string;

start ::= __json_0_0_json '\\n';'''

snapshots['test_formatter_regex_complement 1'] = '''__regex_complement_0_0_non_numeric ::= #ex'[0-9]';
__regex_1_0_numeric ::= #'[0-9]+';
start ::= 'Text: ' __regex_complement_0_0_non_numeric 'Number: ' __regex_1_0_numeric '\\n';'''

snapshots['test_formatter_regex_complement 2'] = '''Text: The two of them went to the zoo.

Assistant: The zoo was on the second floor.
So, the answer is "The zoo was on the second floor". So, let\'s think of the answer as a group of two integers, and we can break it down into two groups of two integers.
Group #A:
The first group of two integers is (int x, int y) where x and y are integers.
Group #B:
The second group of two integers is (int x, int y) where x and y are integers.
Group #C:
The third group of two integers is (int x, int y) where x and y are integers.
Group #D:
The fourth group of two integers is (int x, int y) where x and y are integers.
Group #E:
The fifth group of two integers is (int x, int y) where x and y are integers.
Group #F:
The sixth group of two integers is (int x, int y) where x and y are integers.
Group #G:
The seventh group of two integers is (int x, int y) where x and y are integers.
'''

snapshots['test_formatter_regex_complement 3'] = {
    'non_numeric': 'Hello, world! Number: ',
    'numeric': GenericRepr("<re.Match object; span=(0, 2), match='42'>")
}

snapshots['test_formatter_regex_complement 4'] = {
    'non_numeric': 'Hello, world! Number: ',
    'numeric': GenericRepr("<re.Match object; span=(0, 2), match='42'>")
}

snapshots['test_formatter_str 1'] = '''__str_0_0 ::= #'.*?(?:\\\\.)';
start ::= __str_0_0 '\\n';'''

snapshots['test_formatter_str 2'] = '这是我的名字。 我在这里住着。 我有一个朋友。 我想知道， 你们知道什么叫做爱吗？ 它是什么？ 它是什么样子的？ 我想知道。 你们知道什么叫做爱吗？ 它是什么样子的？ 它是什么样子的？ 它是什么样子的？ 这是我的朋友， 他正在跟我说话。 我很喜欢他。 他说： “我想知道， 你们知道什么叫做爱吗？” 我想回答， “不，” 但是他问： “那就好了。” 于是我们就这样谈论了。 你们知道， 当然， 这也是我们的关系。 他和我一起住在这里。 我们都很好， 而且我很喜欢他。 你们知道， 我喜欢他， 但是他也很喜欢我。 因为他想'

snapshots['test_formatter_str 3'] = {
}

snapshots['test_formatter_substr 1'] = '''__substr_0_0_substr ::= #substrs'Name: Umbrella; Price: 114.514 dollars;';
start ::= __substr_0_0_substr '<eos>';'''

snapshots['test_formatter_substr 2'] = ' 114.514 dollars;<eos>'

snapshots['test_formatter_substr 3'] = {
    'substr': ' 114.514 dollars;'
}

snapshots['test_formatter_top_level_array_json_schema 1'] = '''integer ::= #"-?(0|[1-9][0-9]*)";
number ::= #"-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
__json_0_0_json_min ::= __json_0_0_json_item;
__json_0_0_json ::= array_begin __json_0_0_json_min comma __json_0_0_json_item array_end;
__json_0_0_json ::= array_begin __json_0_0_json_min comma __json_0_0_json_item comma __json_0_0_json_item array_end;
__json_0_0_json ::= array_begin __json_0_0_json_min comma __json_0_0_json_item comma __json_0_0_json_item comma __json_0_0_json_item array_end;
__json_0_0_json ::= array_begin __json_0_0_json_min comma __json_0_0_json_item comma __json_0_0_json_item comma __json_0_0_json_item comma __json_0_0_json_item array_end;
__json_0_0_json_item ::= json_value;

start ::= __json_0_0_json '\\n';'''

snapshots['test_formatter_top_level_array_json_schema 2'] = '''[{"id": 1, "name": "John"}, {"id": 2, "name": "Mary"}, {"id": 3, "name": "Jane"}, {"id": 4, "name": "Joe"}]
'''

snapshots['test_formatter_top_level_array_json_schema 3'] = {
    'json': [
        {
            'id': 1,
            'name': 'John'
        },
        {
            'id': 2,
            'name': 'Mary'
        },
        {
            'id': 3,
            'name': 'Jane'
        },
        {
            'id': 4,
            'name': 'Joe'
        }
    ]
}

snapshots['test_grammar_literal 1'] = '''integer ::= #"-?(0|[1-9][0-9]*)";
number ::= #"-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
__json_0_0_json ::= object_begin \'"a"\' colon __json_0_0_json_a object_end;
__json_0_0_json_a ::= \'"114"\' | \'"514"\';

start ::= __json_0_0_json '\\n';'''

snapshots['test_grammar_literal 2'] = '''{"a":"114"}
'''

snapshots['test_grammar_literal 3'] = {
    'json': GenericRepr("A(a='114')")
}

snapshots['test_utf8_json_key 1'] = '''integer ::= #"-?(0|[1-9][0-9]*)";
number ::= #"-?(0|[1-9][0-9]*)(\\\\.[0-9]+)?([eE][+-]?[0-9]+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"[ \t
\r]*,[ \t
\r]*";
colon ::= #"[ \t
\r]*:[ \t
\r]*";
object_begin ::= #"\\\\{[ \t
\r]*";
object_end ::= #"[ \t
\r]*\\\\}";
array_begin ::= #"\\\\[[ \t
\r]*";
array_end ::= #"[ \t
\r]*\\\\]";
__json_0_0_json ::= object_begin \'"土豆"\' colon __json_0_0_json_u571fu8c46 comma \'"\\\\(@^0^@)/"\' colon __json_0_0_json_u5cu28u40u5e0u5eu40u29u2f comma \'"🍎"\' colon __json_0_0_json_u1f34e object_end;
__json_0_0_json_u1f34e ::= __json_0_0_json_u1f34e_required?;
__json_0_0_json_u1f34e_required ::= string;
__json_0_0_json_u5cu28u40u5e0u5eu40u29u2f ::= __json_0_0_json_u5cu28u40u5e0u5eu40u29u2f_required?;
__json_0_0_json_u5cu28u40u5e0u5eu40u29u2f_required ::= string;
__json_0_0_json_u571fu8c46 ::= __json_0_0_json_u571fu8c46_required?;
__json_0_0_json_u571fu8c46_required ::= string;

start ::= __json_0_0_json '\\n';'''

snapshots['test_utf8_json_key 2'] = '''{"土豆": "是一种特殊的食品,有机和天然的配方,是一种含有淀粉、果糖、蛋白质和多种维生素的水果。"

,  "\\(@^0^@)/"

:  "\\"土豆\\""

,  "🍎"

:  "\\"大家好,我是 🍎 🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎\\n\\n[#上面](https://www.zhihu.com/search?q=土豆) **这个文章** 的标题是: 土豆: 一种特殊的食品,有机和天然的配方,是一种含有淀粉、果糖、蛋白质和多种维生素的水果'''

snapshots['test_utf8_json_key 3'] = {
}
