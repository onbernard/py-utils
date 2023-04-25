from itertools import chain as iterchain
from typing import (
    Any,
    Sequence,
    Tuple,
    Iterator,
    TypeVar,
    Callable,
    Iterable,
)

T = TypeVar("T")
ParseInputT = Iterator[T]
BacktrackT = Iterable[T]
ParseOutputT = Tuple[BacktrackT,Any]
ParserT = Callable[[ParseInputT],ParseOutputT]


class ParseFailure(Exception):
    def __init__(self, reason: str, backtrack: BacktrackT) -> None:
        super().__init__(reason)
        self.backtrack = backtrack
        self.reason = reason


def try_parse(parser: ParserT):
    def outp_parser(sequence: ParseInputT) -> ParseOutputT:
        try:
            return parser(sequence)
        except ParseFailure as exc:
            return iterchain(exc.backtrack, sequence), ()
    return outp_parser


def join(*parsers: ParserT):
    def outp_parser(sequence: ParseInputT) -> ParseOutputT:
        results = []
        backtrack: BacktrackT = []
        for p in parsers:
            b, r = p(iterchain(backtrack,sequence))
            backtrack = b
            results.append(r)
        return b, results
    return outp_parser


def try_choice(*parsers):
    def outp_parser(sequence: ParseInputT) -> ParseOutputT:
        reasons = []
        backtrack: BacktrackT = []
        for p in parsers:
            try:
                return p(iterchain(backtrack, sequence))
            except ParseFailure as exc:
                reasons.append(exc.reason)
                backtrack = exc.backtrack
                continue
        raise ParseFailure("\n•".join(reasons), backtrack)
    return outp_parser


def zero_or_more(parser):
    def outp_parser(sequence: ParseInputT) -> ParseOutputT:
        backtrack: BacktrackT = []
        results = []
        try:
            while True:
                b,r = parser(iterchain(backtrack, sequence))
                results.append(r)
                backtrack = b
        except ParseFailure as exc:
            return exc.backtrack, results
        except StopIteration:
            return backtrack, results
    return outp_parser


def negated(parser):
    """Only works on parsers that backtracks everything they consume"""
    def outp_parser(sequence: ParseInputT) -> ParseOutputT:
        try:
            b, r = parser(sequence)
        except ParseFailure as exc:
            return [], exc.backtrack
        else:
            raise ParseFailure("Negated parser matched", b)
    return outp_parser


def one_or_more(parser):
    return join(
        parser,
        zero_or_more(parser)
    )

def skip_left(p_left: ParserT, p_right: ParserT) -> ParserT:
    def outp_parser(sequence: ParseInputT) -> ParseOutputT:
        b, r = p_left(sequence)
        return p_right(iterchain(b, sequence))
    return outp_parser

def skip_right(parser):
    """TODO"""

def sepby(parser):
    """TODO"""


def alpha(sequence: Iterator[str]) -> ParseOutputT:
    c = next(sequence)
    if c.isalpha():
        return [], c
    raise ParseFailure("Expected a letter", [c,])


def numeric(sequence: Iterator[str]) -> ParseOutputT:
    c = next(sequence)
    if c.isnumeric():
        return [], c
    raise ParseFailure("Expected a numeric", [c,])


def space(sequence: Iterator[str]) -> ParseOutputT:
    c = next(sequence)
    if c.isspace():
        return [], c
    raise ParseFailure("Expected a numeric", [c,])


def term(t: str) -> ParserT:
    def outp_parser(sequence: Iterator[str]) -> Tuple[Sequence[str],str]:
        n = next(sequence)
        if n==t:
            return [],n
        raise ParseFailure(f"Expected {t}", n)
    return outp_parser

def string(s: str) -> ParserT:
    return join(
        *(term(c) for c in s)
    )

def term_set(s: Sequence) -> ParserT:
    def outp_parser(sequence: Iterator[str]) -> Tuple[Sequence[str],str]:
        n = next(sequence)
        if n in s:
            return [],n
        raise ParseFailure(f"Expected {s}", n)
    return outp_parser


def term_backtrack(t: str) -> ParserT:
    def outp_parser(sequence: Iterator[str]) -> Tuple[Sequence[str],str]:
        n = next(sequence)
        if n==t:
            return [n,], n
        raise ParseFailure(f"Expected {t}", n)
    return outp_parser


def term_set_backtrack(s: Sequence) -> ParserT:
    def outp_parser(sequence: Iterator[str]) -> Tuple[Sequence[str],str]:
        n = next(sequence)
        if n in s:
            return [n,], n
        raise ParseFailure(f"Expected {s}", n)
    return outp_parser

def transform(parser, fn):
    def wrap_parser(seq):
        b, r = parser(seq)
        return b, fn(r)
    return wrap_parser

def eof(s: Sequence):
    """TODO"""