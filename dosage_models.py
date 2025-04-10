from pydantic import BaseModel, Field
from typing import List
import json


class Event(BaseModel):
    frequency: str = Field(
        description="How often the drug is prescribed.", examples=["twice daily"]
    )
    amount: dict = Field(
        description="Phyiscal amount of prescription to take.",
        examples=[{"value": 0.25, "unit": "tablet"}],
    )
    strength: dict = Field(
        description="Prescription strength.", examples=[{"value": 20, "unit": "mg"}]
    )

    @staticmethod
    def get_prompt_repr(nest=1):
        model_json_schema = Event.model_json_schema()
        example_str_response = "{\n"
        for field, details in model_json_schema["properties"].items():
            line_str = f""""{field}": {json.dumps(details["examples"][0])}, # {details["description"]}"""
            example_str_response += "\t" * nest + line_str + "\n"
        example_str_response += "\t" * (nest - 1) + "}"
        return example_str_response


class Summary(BaseModel):
    events: List[Event] = Field(
        description="",
        examples=[
            Event(
                frequency="twice daily",
                amount={"value": 0.25, "unit": "tablet"},
                strength={"value": 20, "unit": "mg"},
            )
        ],
    )
    total_amount: dict = Field(
        description="Sum of all Events individual prescription amounts.",
        examples=[{"value": 0.5, "unit": "tablet"}],
    )
    total_strength: dict = Field(
        description="Sum of all Events individual prescription strength. The total amount of drug prescribed.",
        examples=[{"value": 10, "unit": "mg"}],
    )

    @staticmethod
    def get_prompt_repr():
        model_fields = Summary.model_fields
        example_str_response = "{\n"
        for field, details in model_fields.items():
            try:
                line_str = "\t"
                line_str += f'"{field}": ['
                line_str += type(details.examples[0]).get_prompt_repr(nest=2) + "],"
            except AttributeError as e:
                line_str = f"""\t"{field}": {json.dumps(details.examples[0])}, # {details.description}"""
            example_str_response += line_str + "\n"
        example_str_response += "}"
        return example_str_response


if __name__ == "__main__":
    testA = Event.model_validate(
        {
            "frequency": "twice daily",
            "amount": {"value": 0.5, "unit": "tablet"},
            "strength": {"value": 50, "unit": "mg"},
        }
    )
    print(testA.get_prompt_repr())

    """Albuterol 50mg. take 0.5 tablet by mouth 2 (two) times daily"""
    test1 = Summary.model_validate(
        {
            "events": [
                {
                    "frequency": "twice daily",
                    "amount": {"value": 0.5, "unit": "tablet"},
                    "strength": {"value": 50, "unit": "mg"},
                }
            ],
            "total_amount": {"value": 1, "unit": "tablet"},
            "total_strength": {"value": 50, "unit": "mg"},
        }
    )
    print(test1.get_prompt_repr())
