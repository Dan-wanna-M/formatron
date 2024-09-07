from pydantic import BaseModel
from typing import List, Any

class AnotherTupleModel(BaseModel):

    additional_elements: tuple[int,str,float,...]

# Creating an instance of the model
another_tuple = AnotherTupleModel(
    additional_elements=(1, "hello", 3.14, True, [1, 2, 3])
)

print(another_tuple.additional_elements)