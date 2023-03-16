"""
Data parsing tests
"""

import datautils
import io


# TODO: use fuxtures instead


def test_dummy_row() -> None:
    data_point_ref = datautils.ParaphraseDataPoint(
        lhs="[JJ]",
        phrase="transplant",
        paraphrase="transplantation",
        features={
            "PPDB2.0Score": 5.22098,
            "-logp(e2|e1,LHS)": -2.18813,
            "GlueRule": 0,
            "MVLSASim": None,
        },
        alignment="0-0",
        entailment="Equivalence",
    )
    row_str = (
        "[JJ] ||| transplant ||| transplantation |||"
        " PPDB2.0Score=5.22098 -logp(e2|e1,LHS)=-2.18813 GlueRule=0 MVLSASim=NA"
        "||| 0-0 ||| Equivalence"
    )
    row_stream = io.StringIO(row_str)

    data_generator = datautils.parse_data_ppdb(row_stream)
    row_parsed = next(data_generator)

    assert row_parsed == data_point_ref





