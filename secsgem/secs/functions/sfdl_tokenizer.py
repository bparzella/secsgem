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

import io


class SFDLParseError(Exception):
    """Exception class for SFDL parse error."""

    def __init__(self, message: str, token: SFDLToken):
        """Initialize parse error exception.

        Args:
            message: exception message
            token: token the error occurred in

        """
        super().__init__(message)

        self.token = token


class SFDLToken:
    """SFDL token representation."""

    def __init__(self, value: str, line: int, col: int, tokenizer: SFDLTokenizer):
        """Initialize an SFDL token.

        Args:
            value: token
            line: line in source code
            col: column in source code
            tokenizer: tokenizer that generated this token

        """
        self._value = value
        self._line = line
        self._col = col
        self._tokenizer = tokenizer

    @property
    def value(self) -> str:
        """Get the value property.

        Returns:
              token value

        """
        return self._value

    @property
    def line(self) -> int:
        """Get the line property.

        Returns:
              token line

        """
        return self._line

    @property
    def col(self) -> int:
        """Get the col property.

        Returns:
              token col

        """
        return self._col

    @property
    def tokenizer(self) -> SFDLTokenizer:
        """Get the tokenizer property.

        Returns:
              token tokenizer

        """
        return self._tokenizer

    def __repr__(self):
        """Generate string representation of object."""
        return f"[{self.line:05d}|{self.col:05d}] {self.value}"

    def get_error(self, message: str, end: bool = False) -> str:
        """Format a source code error output for this token.

        Args:
            message: error message
            end: point to the end of the token


        Returns:
            formatted error message

        """
        line = self.line - 1
        prefix = (self.col - 1) * " " if not end else (self.col + len(self.value) - 1) * " "

        return f"{self.tokenizer.source_line(line)}\n{prefix}^-- {message}"

    def exception(self, message: str, end: bool = False) -> SFDLParseError:
        """Return exception for a source code error output for a token.

        Args:
            message: error message
            end: point to the end of the token

        Returns:
            Parser error

        """
        return SFDLParseError(f"\n{self.get_error(message, end)}", self)


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

        self._tokens: list[SFDLToken] = []
        self._token_counter = -1

        self.parse_all()

    def source_line(self, line: int) -> str:
        """Get line of the source code.

        Args:
            line: line number of the code

        Returns:
            code line

        """
        return self._source_lines[line]

    def parse_all(self):
        """Parse all tokens in the source code."""
        current_token = ""
        location = _SFDLSourceLocation()

        while True:
            location.update_uninitialized_line(self._line)
            location.update_uninitialized_column(self._col)

            char = self._get_char()

            if char == "":
                if current_token:
                    self._tokens.append(SFDLToken(current_token, location.line, location.column, self))
                return

            if char in self.whitespaces:
                current_token = self._process_whitespace(current_token, location)
                continue

            if char in self.operators:
                current_token = self._process_operator(char, current_token, location)
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

    def _process_operator(self, char: str, current_token: str, location: _SFDLSourceLocation) -> str:
        line = location.line
        column = location.column

        if current_token:
            self._tokens.append(SFDLToken(current_token, location.line, location.column, self))
            current_token = ""

            line = self._line
            column = self._col - 1 if self._col > 1 else self._col

        self._tokens.append(SFDLToken(char, line, max(column, 1), self))
        location.reset()

        return current_token

    def _process_whitespace(self, current_token: str, location: _SFDLSourceLocation) -> str:
        if current_token:
            self._tokens.append(SFDLToken(current_token, location.line, location.column, self))
            current_token = ""

        location.reset()

        return current_token

    def get_token(self) -> SFDLToken:
        """Get the next available token.

        Returns:
              next token

        """
        self._token_counter += 1
        return self._tokens[self._token_counter]

    @property
    def token_available(self) -> bool:
        """Check if a token is available."""
        return len(self._tokens) > self._token_counter + 1

    def peek_token(self, ahead: int = 1) -> SFDLToken:
        """Get an available token without incrementing the current position.

        Returns:
              token

        """
        return self._tokens[self._token_counter + ahead]


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
