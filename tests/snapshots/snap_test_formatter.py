# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['test_formatter 1'] = '''__choice_food_0 ::= 'railroad' | 'orange' | 'banana';
__regex_0_0 ::= #'[0-9]+';
__regex_1_0 ::= #'[a-z]+';
__choice_ID_0 ::= __regex_0_0 | __regex_1_0;
__str_2_0_excepted ::= '\\\\.';
__str_2_0 ::= except!(__str_2_0_excepted)('\\\\.');
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
__schema_json_0 ::= object_begin \'"name"\' colon __schema_json_0_name comma \'"weight"\' colon __schema_json_0_weight comma \'"color"\' colon __schema_json_0_color object_end;
__schema_json_0_color ::= string;
__schema_json_0_weight ::= number;
__schema_json_0_name ::= string;

start ::= \'Today, I want to eat \' __choice_food_0 \'\\n\' "My food\'s ID is " __choice_ID_0 \'.\\n\' "\\nWhat\'s more, indentations\\nare handled\\nappropriately. Let\'s " __str_2_0 \'My weight is 14.4kg and my color is pink. This is my personal info json: \' __schema_json_0 \'\\n\';'''

snapshots['test_formatter 2'] = '''Today, I want to eat orange
My food's ID is a.

What's more, indentations
are handled
appropriately.My weight is 14.4kg and my color is pink. This is my personal info json: {"name":"Van","weight":1.4,"color":"#F9F9F9"}
'''

snapshots['test_formatter 3'] = {
    'ID': GenericRepr("<re.Match object; span=(0, 1), match='a'>"),
    'food': 'orange',
    'json': GenericRepr("Test(name='Van', weight=1.4, color='#F9F9F9')")
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
__schema_json_0 ::= object_begin \'"a"\' colon __schema_json_0_a comma \'"b"\' colon __schema_json_0_b comma \'"c"\' colon __schema_json_0_c object_end;
__schema_json_0_c ::= integer;
__schema_json_0_b ::= integer;
__schema_json_0_a ::= integer;

start ::= __schema_json_0 '\\n';'''

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
__schema_json_0 ::= object_begin \'"name"\' colon __schema_json_0_name comma \'"gender"\' colon __schema_json_0_gender object_end;
__schema_json_0_gender ::= string;
__schema_json_0_name ::= string;

start ::= __schema_json_0 '\\n';'''

snapshots['test_formatter_dict_inference 2'] = '''{"name":"Ryan","gender":"male"}
'''

snapshots['test_formatter_dict_inference 3'] = {
    'json': {
        'gender': 'male',
        'name': 'Ryan'
    }
}

snapshots['test_formatter_str 1'] = '''__str_0_0_excepted ::= '\\\\.' | '!';
__str_0_0 ::= except!(__str_0_0_excepted)('\\\\.'|'!');
start ::= __str_0_0 '\\n';'''

snapshots['test_formatter_str 2'] = '''🤗"
"I am the father of three beautiful girls, all of whom are also famous in the world of martial arts," said Van, "I want to thank you for taking care of my girls and my mother, and I hope that you will continue to support me in my quest to bring happiness to the world, because I believe that we are all connected through love and kindness, and that\'s why I am happy to have met you today and hope that we can make a new life together as a family, one where we can be happy together and love each other more than anything else in the world, even if we do not know it yet"
"I hope that this relationship will last forever, and that we can find happiness in our lives together, because we are both very special people who are willing to do anything for each other," said Van, "I wish you all the best in your future endeavors, and I look forward to seeing you again soon, and may God bless you all"
Van, a martial artist from the Philippines, is known for his passion for martial arts and has been involved in various martial arts competitions around the world, including the Asian Championships held in Japan, Thailand, Singapore, Malaysia, Hong Kong, and Taiwan'''

snapshots['test_formatter_str 3'] = {
}
