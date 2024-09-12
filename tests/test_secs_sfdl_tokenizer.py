#####################################################################
# test_secs_sfdl_tokenizer.py
#
# (c) Copyright 2024, Benjamin Parzella. All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#####################################################################
import pytest

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.functions.sfdl_tokenizer import SFDLTokenizer, SFDLParseError


class TestSFDLTokenizer:
    def test_compact_source(self):
        source = """< L SAMPLE_NAME <L <DVNAME> <DVVAL> >>"""

        tokenizer = SFDLTokenizer(source)
        print(tokenizer)

        expected_tokens = [
            {"value": "<", "line": 1, "col": 1},
            {"value": "L", "line": 1, "col": 3},
            {"value": "SAMPLE_NAME", "line": 1, "col": 5},
            {"value": "<", "line": 1, "col": 17},
            {"value": "L", "line": 1, "col": 18},
            {"value": "<", "line": 1, "col": 20},
            {"value": "DVNAME", "line": 1, "col": 21},
            {"value": ">", "line": 1, "col": 27},
            {"value": "<", "line": 1, "col": 29},
            {"value": "DVVAL", "line": 1, "col": 30},
            {"value": ">", "line": 1, "col": 35},
            {"value": ">", "line": 1, "col": 37},
            {"value": ">", "line": 1, "col": 38},
        ]

        for expected_token in expected_tokens:
            token = tokenizer.tokens.next()
            assert token.value == expected_token["value"]
            assert token.location.line == expected_token["line"]
            assert token.location.column == expected_token["col"]


    def test_multiline_source(self):
        source = """< L SAMPLE_NAME
    <L
        <DVNAME>
        < DVVAL >
    >
>"""

        tokenizer = SFDLTokenizer(source)
        print(tokenizer)

        expected_tokens = [
            {"value": "<", "line": 1, "col": 1},
            {"value": "L", "line": 1, "col": 3},
            {"value": "SAMPLE_NAME", "line": 1, "col": 5},
            {"value": "<", "line": 2, "col": 4},
            {"value": "L", "line": 2, "col": 5},
            {"value": "<", "line": 3, "col": 8},
            {"value": "DVNAME", "line": 3, "col": 9},
            {"value": ">", "line": 3, "col": 15},
            {"value": "<", "line": 4, "col": 8},
            {"value": "DVVAL", "line": 4, "col": 10},
            {"value": ">", "line": 4, "col": 16},
            {"value": ">", "line": 5, "col": 4},
            {"value": ">", "line": 6, "col": 1},
        ]

        for expected_token in expected_tokens:
            token = tokenizer.tokens.next()
            assert token.value == expected_token["value"]
            assert token.location.line == expected_token["line"]
            assert token.location.column == expected_token["col"]


    def test_source_with_comment(self):
        source = """< L SAMPLE_NAME
    <L # comment1
        <DVNAME>  # comment2
        < DVVAL >  # comment 3 until eol
    >
>"""

        tokenizer = SFDLTokenizer(source)
        print(tokenizer)

        expected_tokens = [
            {"value": "<", "line": 1, "col": 1},
            {"value": "L", "line": 1, "col": 3},
            {"value": "SAMPLE_NAME", "line": 1, "col": 5},
            {"value": "<", "line": 2, "col": 4},
            {"value": "L", "line": 2, "col": 5},
            {"value": "<", "line": 3, "col": 8},
            {"value": "DVNAME", "line": 3, "col": 9},
            {"value": ">", "line": 3, "col": 15},
            {"value": "<", "line": 4, "col": 8},
            {"value": "DVVAL", "line": 4, "col": 10},
            {"value": ">", "line": 4, "col": 16},
            {"value": ">", "line": 5, "col": 4},
            {"value": ">", "line": 6, "col": 1},
        ]

        for expected_token in expected_tokens:
            token = tokenizer.tokens.next()
            assert token.value == expected_token["value"]
            assert token.location.line == expected_token["line"]
            assert token.location.column == expected_token["col"]

    def test_empty_source(self):
        source = """"""

        with pytest.raises(SFDLParseError) as exc:
            SFDLTokenizer(source)

        assert str(exc.value) == "\n\n^-- Opening tag '<' expected"


class TestSFDLFunction:
    def test_sfdl_function(self):
        class SecsS02F30(SecsStreamFunction):
            _stream = 2
            _function = 30

            _to_host = True
            _to_equipment = False

            _has_reply = False
            _is_reply_required = False

            _is_multi_block = True

            _data_format = """
                < L
                    < L
                        < ECID >
                        < ECNAME >
                        < ECMIN >
                        < ECMAX >
                        < ECDEF >
                        < UNITS >
                    >
                >
            """

        function = SecsS02F30([[1, "NAME", 0, 10, 5, "mm"], [2, "NEWNAME", 10, 20, 15, "qm"]])

        assert function[0].ECID == 1
        assert function[0].ECNAME == "NAME"
        assert function[0].ECMIN == 0
        assert function[0].ECMAX == 10
        assert function[0].ECDEF == 5
        assert function[0].UNITS == "mm"
        assert function[1].ECID == 2
        assert function[1].ECNAME == "NEWNAME"
        assert function[1].ECMIN == 10
        assert function[1].ECMAX == 20
        assert function[1].ECDEF == 15
        assert function[1].UNITS == "qm"

        assert str(function) == 'S2F30\n  <L [2]\n    <L [6]\n      <U1 1 >\n      <A "NAME">\n      <I8 0 >\n      <I8 10 >\n      <I8 5 >\n      <A "mm">\n    >\n    <L [6]\n      <U1 2 >\n      <A "NEWNAME">\n      <I8 10 >\n      <I8 20 >\n      <I8 15 >\n      <A "qm">\n    >\n  > .'

        assert str(SecsS02F30) == '[\n    {\n        ECID: U1/U2/U4/U8/I1/I2/I4/I8/A\n        ECNAME: A\n        ECMIN: BOOLEAN/I8/I1/I2/I4/F8/F4/U8/U1/U2/U4/A/B\n        ECMAX: BOOLEAN/I8/I1/I2/I4/F8/F4/U8/U1/U2/U4/A/B\n        ECDEF: BOOLEAN/I8/I1/I2/I4/F8/F4/U8/U1/U2/U4/A/B\n        UNITS: A\n    }\n    ...\n]'

    def test_custom_sfdl_function(self):
        class Dummy(SecsStreamFunction):
            _stream = 1
            _function = 1

            _to_host = True
            _to_equipment = False

            _has_reply = False
            _is_reply_required = False

            _is_multi_block = True

            _data_format = """
                < L
                    < DSID >
                    < L DV
                        < L
                            <DVNAME>
                            <DVVAL>
                        >
                    >
                >
            """

        function = Dummy({
            "DSID": "TESTDSID",
            "DV": [
                {
                    "DVNAME": "DVNAME1",
                    "DVVAL": "DVVAL1"
                },
                {
                    "DVNAME": "DVNAME2",
                    "DVVAL": "DVVAL2"
                },
            ]
        })

        assert function.DSID == "TESTDSID"
        assert function.DV[0].DVNAME == "DVNAME1"
        assert function.DV[0].DVVAL == "DVVAL1"
        assert function.DV[1].DVNAME == "DVNAME2"
        assert function.DV[1].DVVAL == "DVVAL2"

        assert str(function) == 'S1F1\n  <L [2]\n    <A "TESTDSID">\n    <L [2]\n      <L [2]\n        <A "DVNAME1">\n        <A "DVVAL1">\n      >\n      <L [2]\n        <A "DVNAME2">\n        <A "DVVAL2">\n      >\n    >\n  > .'

        assert str(Dummy) == '{\n    DSID: U1/U2/U4/U8/I1/I2/I4/I8/A\n    DV: [\n        {\n            DVNAME: U1/U2/U4/U8/I1/I2/I4/I8/A\n            DVVAL: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B\n        }\n        ...\n    ]\n}'

    def test_missing_opening_tag(self):
        class Dummy(SecsStreamFunction):
            _stream = 1
            _function = 1

            _to_host = True
            _to_equipment = False

            _has_reply = False
            _is_reply_required = False

            _is_multi_block = True

            _data_format = "DSID"

        with pytest.raises(SFDLParseError) as exc:
            function = Dummy({
                "DSID": "TESTDSID",
            })

        assert str(exc.value) == "\nDSID\n^-- Opening tag '<' expected"

    def test_missing_opening_tag_extra_whitespace(self):
        class Dummy(SecsStreamFunction):
            _stream = 1
            _function = 1

            _to_host = True
            _to_equipment = False

            _has_reply = False
            _is_reply_required = False

            _is_multi_block = True

            _data_format = " DSID "

        with pytest.raises(SFDLParseError) as exc:
            function = Dummy({
                "DSID": "TESTDSID",
            })

        assert str(exc.value) == "\n DSID \n ^-- Opening tag '<' expected"

    def test_missing_closing_tag(self):
        class Dummy(SecsStreamFunction):
            _stream = 1
            _function = 1

            _to_host = True
            _to_equipment = False

            _has_reply = False
            _is_reply_required = False

            _is_multi_block = True

            _data_format = "< DSID"

        with pytest.raises(SFDLParseError) as exc:
            function = Dummy({
                "DSID": "TESTDSID",
            })

        assert str(exc.value) == "\n< DSID\n      ^-- Closing tag '>' expected"

    def test_invalid_closing_tag(self):
        class Dummy(SecsStreamFunction):
            _stream = 1
            _function = 1

            _to_host = True
            _to_equipment = False

            _has_reply = False
            _is_reply_required = False

            _is_multi_block = True

            _data_format = "< DSID INVALID_DATA"

        with pytest.raises(SFDLParseError) as exc:
            function = Dummy({
                "DSID": "TESTDSID",
            })

        assert str(exc.value) == "\n< DSID INVALID_DATA\n       ^-- Closing tag '>' expected"

    def test_invalid_item(self):
        class Dummy(SecsStreamFunction):
            _stream = 1
            _function = 1

            _to_host = True
            _to_equipment = False

            _has_reply = False
            _is_reply_required = False

            _is_multi_block = True

            _data_format = "< INVALID >"

        with pytest.raises(SFDLParseError) as exc:
            function = Dummy({
                "INVALID": "TESTDSID",
            })

        assert str(exc.value) == "\n< INVALID >\n  ^-- Unknown data type INVALID"

    def test_invalid_closing_tag_in_list(self):
        class Dummy(SecsStreamFunction):
            _stream = 1
            _function = 1

            _to_host = True
            _to_equipment = False

            _has_reply = False
            _is_reply_required = False

            _is_multi_block = True

            _data_format = "< L < DSID >< DVVAL >"

        with pytest.raises(SFDLParseError) as exc:
            function = Dummy({
                "DSID": "TESTDSID",
            })

        assert str(exc.value) == "\n< L < DSID >< DVVAL >\n                     ^-- Expected opening '<' or closing '>' tag"
