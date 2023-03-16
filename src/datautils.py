"""
This module contains parsing utils for the PPDB data

TODO: implement strategies for handling errors (skip feature / skip data point / raise error)
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, Tuple, TextIO


@dataclass(frozen=True)
class ParaphraseDataPoint:
    phrase: str 
    paraphrase: str
    lhs: str = ""
    features: Dict[str, str] = field(default_factory=dict)
    alignment: str = ""
    entailment: str = ""


class ParaphraseParsingError(ValueError):
    """
    Represents an error when parsing paraphrases
    """


FeatureValue = float | None


def _parse_safe(value, dtype: Any) -> Any | None:
    """
    Converts value to specified data type. 

    Returns None if the conversion cannot be done.
    """
    try: 
        return dtype(value)
    except ValueError:
        return None


def _parse_feature_to_kv(feature_str: str) -> Tuple[str, FeatureValue]:
    """
    Separates name of a feature from its value.

    Raises ParaphraseParsingError when the format is not as expected.
    """
    try: 
        feature_name, value_str = feature_str.split(r"=", 2)
    except ValueError:
        raise ParaphraseParsingError("Feature string doesn't satisfy the format.")
    
    value = _parse_safe(value_str, float)

    return feature_name, value


def _parse_ppdb_features(features_string: str) -> Dict[str, FeatureValue]:
    """
    Parses all the PPDB data point fatures stored as a raw string into a dictionary format.
    """
    features_list = [feature for feature in features_string.split()]
    features_dict = {feature: val for feature, val in map(_parse_feature_to_kv, features_list)}

    return features_dict



def parse_data_ppdb(file_stream: TextIO) -> Iterator[ParaphraseDataPoint]:
    """
    Parses locally stored PPBD data into the unified format.
    Returns an iterator over individual parsed data points. 

    Raw PPBD data format: 
        LHS ||| PHRASE ||| PARAPHRASE ||| (FEATURE=VALUE )* ||| ALIGNMENT ||| ENTAILMENT
    """
    while file_stream:
        # split individual parts of the row
        line_split = file_stream.readline().split("|||")
        lhs, phrase, paraphrase, features_str, alignment, entailment = (
            [line.strip() for line in line_split]
        )
        # parse features into the dict format
        features_dict = _parse_ppdb_features(features_str)

        yield ParaphraseDataPoint(
            lhs=lhs, 
            phrase=phrase, 
            paraphrase=paraphrase,
            features=features_dict,
            alignment=alignment,
            entailment=entailment,
        )

