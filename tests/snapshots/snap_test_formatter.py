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
My food's ID is lime.

What's more, indentations
are handled
appropriately.My weight is 14.4kg and my color is pink. This is my personal info json: { \t
\t"name": "Van",
\t"weight": 120,
\t"color": "pink"
}
'''

snapshots['test_formatter 3'] = {
    'ID': GenericRepr("<re.Match object; span=(0, 4), match='lime'>"),
    'food': 'orange',
    'json': GenericRepr("Test(name='Van', weight=120.0, color='pink')")
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

snapshots['test_formatter_callable_schema 2'] = '''{"a": 1, "b": 2, "c": 3}
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

snapshots['test_formatter_dict_inference 2'] = '''{"name":"[1,2,3,4,5]","gender":"male"}
'''

snapshots['test_formatter_dict_inference 3'] = {
    'json': {
        'gender': 'male',
        'name': '[1,2,3,4,5]'
    }
}

snapshots['test_formatter_json_no_properties 1'] = {
    'data': {
        'key': 'value',
        'number': 42
    }
}

snapshots['test_formatter_json_schema 1'] = '''{"name":"Jack","age":100}
'''

snapshots['test_formatter_json_schema 2'] = {
    'json': {
        'age': 100,
        'name': 'Jack'
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

snapshots['test_formatter_regex_complement 2'] = '''Text: 'Y'

Assistant: Y + (int(x) - int(y)) / (int(x) - int(y))
The result is a floating point number that represents the difference between two integers. The integer value is multiplied by the number of decimal places to get the remainder, which is then added to the integer value to get the final result. In this case, the final result is (int(x) - int(y)) / (int(x) - int(y)). This is a simple way to represent a number in a floating point format.
The function uses the integer value of x and y to represent the difference between them. The result is then multiplied by the number of decimal places to get the remainder, which is then added to the integer value to get the final result. This process repeats until the final result is obtained.
Hope this explanation helps! Let me know if you have any other questions.

User: Can you explain how the multiplication operator works in Python?

Assistant: Yes, of course! 
In Python, we can use the `*` operator to multiply two numbers together. Here's an example:
```python
my_list = [i for i in range'''

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

snapshots['test_formatter_str 2'] = '˚av, for short. I am a little boy, but I have an awesome uncle who is my best friend." Van\'s voice sounded a little timid, but he was smiling at the young girl. "I am going to go now, so I hope you have a nice day." He said as he turned around and left the house. The young girl just stared at him for a moment before smiling and walking out of the house. She then ran into her house and locked the door. She looked around and noticed that her window was open. She went to her window and saw that it was open. She then heard a loud thud. She ran out of her house and saw that someone had knocked her down. She tried to get up, but she was too weak. The man who had knocked her down walked over to her and picked her up by the collar of her shirt. He looked at her with an evil smile on his face. "Why did you run away from home?" He asked. "I don\'t know," she said as she struggled to get out of his grip. "You see, I was running away from home, and I ran into your house." He said as he grabbed her arms and pulled her close to him. "Now'

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

snapshots['test_formatter_top_level_array_json_schema 2'] = '''[{"name": "Adam", "email": "adam@example.com"}, {"name": "Lisa", "email": "lisa@example.com"}, {"name": "John", "email": "john@example.com"}]
'''

snapshots['test_formatter_top_level_array_json_schema 3'] = {
    'json': [
        {
            'email': 'adam@example.com',
            'name': 'Adam'
        },
        {
            'email': 'lisa@example.com',
            'name': 'Lisa'
        },
        {
            'email': 'john@example.com',
            'name': 'John'
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
