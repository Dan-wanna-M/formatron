from pydantic import BaseModel, Field

class StringLengthModel(BaseModel):
    short_string: bool = Field(...)
    medium_string: str = Field(..., min_length=5, max_length=50)
    long_string: str = Field(..., min_length=10, max_length=100, pattern="[a-zA-Z0-9]+")

model = StringLengthModel(
    short_string=False,
    medium_string="This is a medium length string",
    long_string="This is a longer string that can contain more characters"
)
print(model.model_fields["long_string"].metadata[1])