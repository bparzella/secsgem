#####################################################################
# sfdl_tokenizer.py
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
"""Secs function definition language tokenizer."""

from __future__ import annotations

import enum
import io

from secsgem.secs import data_items


class SFDLParseError(Exception):
    """Exception class for SFDL parse error."""

    def __init__(self, message: str, location: _SFDLSourceLocation, tokenizer: SFDLTokenizer, offset: int = 0):
        """Initialize parse error exception.

        Args:
            message: exception message
            location: source location of the error
            tokenizer: tokenizer that split this message
            offset: error pointer offset

        """
        prefix = (location.column + offset - 1) * " "
        message = f"\n{tokenizer.source_line(location.line - 1)}\n{prefix}^-- {message}"

        super().__init__(message)

        self.location = location
        self.tokenizer = tokenizer
        self.offset = offset

    @classmethod
    def from_token(cls, message: str, token: SFDLToken, end: bool = False) -> SFDLParseError:
        """Initialize parse error exception from SFDLToken.

        Args:
            message: error message
            token: token to create message for
            end: error pointer at the end of the token

        Returns:
            SFDLParseError object

        """
        return SFDLParseError(message, token.location, token.tokenizer, len(token.value) if end else 0)


class SFDLTokenType(enum.Enum):
    """Types for SFDL token."""

    OPEN_TAG = 1
    CLOSE_TAG = 2
    DATA_ITEM = 10
    LIST = 20
    LIST_NAME = 21


class SFDLToken:
    """SFDL token representation."""

    def __init__(self, typ: SFDLTokenType, value: str, location: _SFDLSourceLocation, tokenizer: SFDLTokenizer):
        """Initialize an SFDL token.

        Args:
            typ: token type
            value: token content
            location: location in source code
            tokenizer: tokenizer that generated this token

        """
        self._type = typ
        self._value = value
        self._location = location
        self._tokenizer = tokenizer

    @property
    def type(self) -> SFDLTokenType:
        """Get the token type.

        Returns:
              token type

        """
        return self._type

    @property
    def value(self) -> str:
        """Get the value property.

        Returns:
              token value

        """
        return self._value

    @property
    def location(self) -> _SFDLSourceLocation:
        """Get the location property.

        Returns:
              token source location

        """
        return self._location

    @property
    def tokenizer(self) -> SFDLTokenizer:
        """Get the tokenizer property.

        Returns:
              token tokenizer

        """
        return self._tokenizer

    def __repr__(self):
        """Generate string representation of object."""
        return f"[{self.location.line:05d}|{self.location.column:05d}] {self.value}"

    def exception(self, message: str, end: bool = False) -> SFDLParseError:
        """Return exception for a source code error output for a token.

        Args:
            message: error message
            end: point to the end of the token

        Returns:
            Parser error

        """
        return SFDLParseError.from_token(message, self, end)


class _SFDLElementList:
    def __init__(self) -> None:
        self._items: list[tuple[str, _SFDLSourceLocation]] = []

    def append(self, value: str, location: _SFDLSourceLocation):
        """Add an element to the list.

        Args:
            value: element value
            location: element location

        """
        self._items.append((value, location))

    def pop(self) -> tuple[str, _SFDLSourceLocation]:
        """Pop the first element of the list.

        Returns:
            Tuple of element valueand code location

        """
        return self._items.pop(0)

    def peek(self, ahead: int = 0) -> tuple[str, _SFDLSourceLocation]:
        """Look at an element in the list.

        Args:
            ahead: number of items too look ahead

        Returns:
            Tuple of element value and code location

        """
        return self._items[ahead]

    @property
    def available(self) -> bool:
        """Check if an item is available."""
        return len(self._items) > 0


class SFDLTokens:
    """Container for SFDL tokens."""

    def __init__(self, tokens: list[SFDLToken]) -> None:
        """Initialize SFDL token list."""
        self._tokens: list[SFDLToken] = tokens
        self._token_pointer = -1

    def next(self) -> SFDLToken:
        """Get the next available token.

        Returns:
              next token

        """
        self._token_pointer += 1
        return self._tokens[self._token_pointer]

    @property
    def available(self) -> bool:
        """Check if a token is available."""
        return len(self._tokens) > self._token_pointer + 1

    def peek(self, ahead: int = 1) -> SFDLToken:
        """Get an available token without incrementing the current position.

        Returns:
              token

        """
        return self._tokens[self._token_pointer + ahead]

    @property
    def data_items(self) -> list[str]:
        """Get a list of data item names used in the tokens."""
        return [token.value for token in self._tokens if token.type == SFDLTokenType.DATA_ITEM]


class SFDLTokenizer:
    """Tokenizer for secs function definition."""

    whitespaces = " \t\n\r"
    operators = "<>"

    def __init__(self, source: str) -> None:
        """Parse the sfdl text to a structure."""
        self._source = io.StringIO(source)

        self._line = 1
        self._col = 1

        self._source_lines = [""]

        self._tokens = SFDLTokens([])

        self.parse_all()

    @property
    def tokens(self) -> SFDLTokens:
        """Get the token container."""
        return self._tokens

    def source_line(self, line: int) -> str:
        """Get line of the source code.

        Args:
            line: line number of the code

        Returns:
            code line

        """
        return self._source_lines[line]

    def _process_tokens(self, elements: _SFDLElementList, tokens: list[SFDLToken] | None = None) -> list[SFDLToken]:
        if tokens is None:
            tokens = []

        self._process_opening_token(elements, tokens)
        self._process_item_token(elements, tokens)
        self._process_closing_token(elements, tokens)

        return tokens

    def _process_opening_token(self, elements: _SFDLElementList, tokens: list[SFDLToken]):
        if not elements.available:
            message = "Opening tag '<' expected"
            if tokens:
                raise tokens[-1].exception(message, end=True)
            raise SFDLParseError(message, _SFDLSourceLocation(1, 1), self)

        opening_value, opening_location = elements.pop()

        if opening_value != "<":
            raise SFDLParseError("Opening tag '<' expected", opening_location, self)

        tokens.append(SFDLToken(SFDLTokenType.OPEN_TAG, opening_value, opening_location, self))

    def _process_item_token(self, elements: _SFDLElementList, tokens: list[SFDLToken]):
        if not elements.available:
            raise SFDLParseError.from_token("Item expected", tokens[-1], end=True)

        item_name, item_location = elements.pop()

        if item_name != "L":
            tokens.append(self._process_data_item_token(item_name, item_location))
        else:
            tokens.append(SFDLToken(SFDLTokenType.LIST, item_name, item_location, self))

            self._process_list_item_token(elements, tokens)

    def _process_closing_token(self, elements: _SFDLElementList, tokens: list[SFDLToken]):
        if not elements.available:
            raise SFDLParseError.from_token("Closing tag '>' expected", tokens[-1], end=True)

        closing_value, closing_location = elements.pop()

        if closing_value != ">":
            raise SFDLParseError("Closing tag '>' expected", closing_location, self)

        tokens.append(SFDLToken(SFDLTokenType.CLOSE_TAG, closing_value, closing_location, self))

    def _process_data_item_token(self, item_name: str, item_location: _SFDLSourceLocation) -> SFDLToken:
        item = getattr(data_items, item_name, None)

        if item is None:
            raise SFDLParseError(f"Unknown data type {item_name}", item_location, self)

        return SFDLToken(SFDLTokenType.DATA_ITEM, item_name, item_location, self)

    def _process_list_item_token(self, elements: _SFDLElementList, tokens: list[SFDLToken]):
        if not elements.available:
            raise SFDLParseError.from_token("Expected opening '<' or closing '>' tag", tokens[-1], end=True)

        if elements.peek()[0] not in "<>":
            item_key_value, item_key_location = elements.pop()
            tokens.append(SFDLToken(SFDLTokenType.LIST_NAME, item_key_value, item_key_location, self))

        while True:
            if not elements.available or elements.peek()[0] not in "<>":
                raise SFDLParseError.from_token("Expected opening '<' or closing '>' tag", tokens[-1], end=True)

            if elements.peek()[0] == ">":
                return

            self._process_tokens(elements, tokens)

    def parse_all(self):
        """Parse all tokens in the source code."""
        current_token = ""
        location = _SFDLSourceLocation()
        elements = _SFDLElementList()

        while True:
            location.update_uninitialized_line(self._line)
            location.update_uninitialized_column(self._col)

            char = self._get_char()

            if char == "":
                if current_token:
                    elements.append(current_token, location.clone())

                self._tokens = SFDLTokens(self._process_tokens(elements))
                return

            if char in self.whitespaces:
                current_token = self._process_whitespace(elements, current_token, location)
                continue

            if char in self.operators:
                current_token = self._process_operator(elements, char, current_token, location)
                continue

            current_token += char

    def _get_char(self) -> str:
        char = self._source.read(1)

        self._col += 1

        if char == "\n":
            self._source_lines.append("")
            self._line += 1
            self._col = 0
        elif char == "\r":
            self._col = 0
        else:
            self._source_lines[-1] = self._source_lines[-1] + char

        return char

    def _process_operator(
        self,
        elements: _SFDLElementList,
        char: str,
        current_token: str,
        location: _SFDLSourceLocation,
    ) -> str:
        line = location.line
        column = location.column

        if current_token:
            elements.append(current_token, location.clone())
            current_token = ""

            line = self._line
            column = self._col - 1 if self._col > 1 else self._col

        elements.append(char, _SFDLSourceLocation(line, max(column, 1)))
        location.reset()

        return current_token

    def _process_whitespace(self, elements: _SFDLElementList, current_token: str, location: _SFDLSourceLocation) -> str:
        if current_token:
            elements.append(current_token, location.clone())
            current_token = ""

        location.reset()

        return current_token


class _SFDLSourceLocation:
    def __init__(self, line: int = -1, column: int = -1):
        self._line = line
        self._column = column

    @property
    def line(self) -> int:
        """Get current line."""
        return self._line

    @property
    def column(self) -> int:
        """Get current column."""
        return self._column

    def reset_line(self):
        """Reset the line to uninitialized."""
        self._line = -1

    def reset_column(self):
        """Reset the column to uninitialized."""
        self._column = -1

    def reset(self):
        """Reset line and column to uninitialized."""
        self.reset_line()
        self.reset_column()

    def update_uninitialized_line(self, line: int):
        """Update the line if it is uninitialized."""
        if self._line == -1:
            self._line = line

    def update_uninitialized_column(self, column: int):
        """Update the column if it is uninitialized."""
        if self._column == -1:
            self._column = column

    def clone(self) -> _SFDLSourceLocation:
        """Get a clone of the location."""
        return self.__class__(self._line, self.column)
