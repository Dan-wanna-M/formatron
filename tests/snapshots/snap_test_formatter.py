# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['test_formatter 1'] = '''__choice_0_0_food ::= 'railroad' | 'orange' | 'banana';
__regex_1_0 ::= #'[0-9]+';
__regex_2_0 ::= #'[a-z]+';
__choice_3_0_ID ::= __regex_1_0 | __regex_2_0;
integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*,(\\u0020|\\u000A|\\u000D|\\u0009)*";
colon ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*:(\\u0020|\\u000A|\\u000D|\\u0009)*";
object_begin ::= #"\\\\{(\\u0020|\\u000A|\\u000D|\\u0009)*";
object_end ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*\\\\}";
array_begin ::= #"\\\\[(\\u0020|\\u000A|\\u000D|\\u0009)*";
array_end ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*\\\\]";
__json_4_0_json ::= object_begin \'"name"\' colon __json_4_0_json_name comma \'"weight"\' colon __json_4_0_json_weight comma \'"color"\' colon __json_4_0_json_color object_end;
__json_4_0_json_color ::= string;
__json_4_0_json_weight ::= number;
__json_4_0_json_name ::= string;

start ::= \'Today, I want to eat \' __choice_0_0_food \'\\n\' "My food\'s ID is " __choice_3_0_ID \'.\\n\' "\\nWhat\'s more, indentations\\nare handled\\nappropriately." \'My weight is 14.4kg and my color is pink. This is my personal info json: \' __json_4_0_json \'\\n\';'''

snapshots['test_formatter 2'] = '''Today, I want to eat banana
My food's ID is banana.

What's more, indentations
are handled
appropriately.My weight is 14.4kg and my color is pink. This is my personal info json: {"name":"Van","weight":1.4,"color":"pink"}
'''

snapshots['test_formatter 3'] = {
    'ID': GenericRepr("<re.Match object; span=(0, 6), match='banana'>"),
    'food': 'banana',
    'json': GenericRepr("Test(name='Van', weight=1.4, color='pink')")
}

snapshots['test_formatter_callable_schema 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*,(\\u0020|\\u000A|\\u000D|\\u0009)*";
colon ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*:(\\u0020|\\u000A|\\u000D|\\u0009)*";
object_begin ::= #"\\\\{(\\u0020|\\u000A|\\u000D|\\u0009)*";
object_end ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*\\\\}";
array_begin ::= #"\\\\[(\\u0020|\\u000A|\\u000D|\\u0009)*";
array_end ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*\\\\]";
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

snapshots['test_formatter_dict_inference 1'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*,(\\u0020|\\u000A|\\u000D|\\u0009)*";
colon ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*:(\\u0020|\\u000A|\\u000D|\\u0009)*";
object_begin ::= #"\\\\{(\\u0020|\\u000A|\\u000D|\\u0009)*";
object_end ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*\\\\}";
array_begin ::= #"\\\\[(\\u0020|\\u000A|\\u000D|\\u0009)*";
array_end ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*\\\\]";
__json_0_0_json ::= object_begin \'"name"\' colon __json_0_0_json_name comma \'"gender"\' colon __json_0_0_json_gender object_end;
__json_0_0_json_gender ::= string;
__json_0_0_json_name ::= string;

start ::= __json_0_0_json '\\n';'''

snapshots['test_formatter_dict_inference 2'] = '''{"name":"P3","gender":"M"}
'''

snapshots['test_formatter_dict_inference 3'] = {
    'json': {
        'gender': 'M',
        'name': 'P3'
    }
}

snapshots['test_formatter_json_schema 1'] = '''{"name":"Test","age":23}
'''

snapshots['test_formatter_json_schema 2'] = {
    'json': {
        'age': 23,
        'name': 'Test'
    }
}

snapshots['test_formatter_json_schema 3'] = '''integer ::= #"-?(0|[1-9]\\\\d*)";
number ::= #"-?(0|[1-9]\\\\d*)(\\\\.\\\\d+)?([eE][+-]?\\\\d+)?";
string ::= #\'"([^\\\\\\\\"\\u0000-\\u001f]|\\\\\\\\["\\\\\\\\bfnrt/]|\\\\\\\\u[0-9A-Fa-f]{4})*"\';
boolean ::= "true"|"false";
null ::= "null";
array ::= array_begin (json_value (comma json_value)*)? array_end;
object ::= object_begin (string colon json_value (comma string colon json_value)*)? object_end;
json_value ::= number|string|boolean|null|array|object;
comma ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*,(\\u0020|\\u000A|\\u000D|\\u0009)*";
colon ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*:(\\u0020|\\u000A|\\u000D|\\u0009)*";
object_begin ::= #"\\\\{(\\u0020|\\u000A|\\u000D|\\u0009)*";
object_end ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*\\\\}";
array_begin ::= #"\\\\[(\\u0020|\\u000A|\\u000D|\\u0009)*";
array_end ::= #"(\\u0020|\\u000A|\\u000D|\\u0009)*\\\\]";
__json_0_0_json ::= object_begin \'"name"\' colon __json_0_0_json_name comma \'"age"\' colon __json_0_0_json_age object_end;
__json_0_0_json_age ::= integer;
__json_0_0_json_name ::= string;

start ::= __json_0_0_json '\\n';'''

snapshots['test_formatter_str 1'] = '''__str_0_0 ::= #e'.*?(?:\\\\.)';
start ::= __str_0_0 '\\n';'''

snapshots['test_formatter_str 2'] = '请帮我找一下哪里有有卖免费的iphone手机，谢谢了！最近买了个小红书推荐的一款手机，这个手机没有网络连接，但是可以通过蓝牙发送信息。我想知道这个手机的价格是多少？还有有没有可以下载安装的软件，比如说手机app等等。谢谢！（提问：是否有任何其他问题需要我回答呢？） 我已经在看了一些电子商务的资料，但是还是没有找到适合自己的产品。您能给我推荐一些适合自己的产品吗？我想了解一下这个产品的特点和优缺点，并且对于自己的需求有什么具体的要求吗？谢谢！（提问：请问您能给我一些具体的问题吗？或者说对于这个产品的特点和优缺点是什么？我想'

snapshots['test_formatter_str 3'] = {
}

snapshots['test_formatter_substr 1'] = '''__substr_0_0_substr ::= #substrs'Name: Umbrella; Price: 114.514 dollars;';
start ::= __substr_0_0_substr '<eos>';'''

snapshots['test_formatter_substr 2'] = ' 114.514 dollars;<eos>'

snapshots['test_formatter_substr 3'] = {
    'substr': ' 114.514 dollars;'
}
