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
My food's ID is soo.

What's more, indentations
are handled
appropriately.My weight is 14.4kg and my color is pink. This is my personal info json: {  "name" : "Van" ,"weight" : 1.4, "color" : "pink"}
'''

snapshots['test_formatter 3'] = {
    'ID': GenericRepr("<re.Match object; span=(0, 3), match='soo'>"),
    'food': 'orange',
    'json': GenericRepr("Test(name='Van', weight=1.4, color='pink')")
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

snapshots['test_formatter_dict_inference 2'] = '''{"name":"Tom","gender":"male"}
'''

snapshots['test_formatter_dict_inference 3'] = {
    'json': {
        'gender': 'male',
        'name': 'Tom'
    }
}

snapshots['test_formatter_json_schema 1'] = '''{"name":"value","age":0}
'''

snapshots['test_formatter_json_schema 2'] = {
    'json': {
        'age': 0,
        'name': 'value'
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

snapshots['test_formatter_regex_complement 2'] = '''Text: I got $l worth of money from $b.
A: $l worth of money from $b is $l worth of money from $b.
$l worth of money from $b is $l worth of money from $b.
$l worth of money from $b is $l worth of money from $b.
$l worth of money from $b is $l worth of money from $b.
$l worth of money from $b is $l worth of money from $b.
$l worth of money from $b is $l worth of money from $b.
$l worth of money from $b is $l worth of money from $b.
$l worth of money from $b is $l worth of money from $b.
$l worth of money from $b is $l worth of money from $b.
$l worth of money from $b is $l worth of money from $b.
$l worth of money from $b is $l worth of money from $b.
$l worth of money from $b is $l worth of money from $b.
$l worth of money from $b is $l worth'''

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

snapshots['test_formatter_str 2'] = '请将上述英文翻译成中文，并且返回正确的翻译方式为英文，因为它不在这个问题中。Answer: 我的名字是Van。请问你想问什么？（我不知道你想问什么，所以我只能回答你）。这是一个简单的问题，你可以告诉我你想问什么。（我不知道你想问什么，所以我只能回答你）。请告诉我你想要了解的是什么？（我不知道你想要了解的是什么，所以我只能回答你）。这是一个有趣的问题，可以让我们聊天。（我不知道你想要聊什么，所以我只能回答你）。请告诉我你想要聊什么？（我不知道你想要聊什么，所以我只能回答你）。这是一个有趣的问题，可以让我们聊天。（我不知道你'

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

snapshots['test_formatter_top_level_array_json_schema 2'] = '''[{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}, {"id": 3, "name": "Mary"}]
'''

snapshots['test_formatter_top_level_array_json_schema 3'] = {
    'json': [
        {
            'id': 1,
            'name': 'John'
        },
        {
            'id': 2,
            'name': 'Jane'
        },
        {
            'id': 3,
            'name': 'Mary'
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
__json_0_0_json_a ::= "\\"114\\"" | "\\"514\\"";

start ::= __json_0_0_json '\\n';'''

snapshots['test_grammar_literal 2'] = '''{"a":"114"}
'''

snapshots['test_grammar_literal 3'] = {
    'json': GenericRepr("A(a='114')")
}
