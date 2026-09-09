"""DUB.SAR 1.0 — Parser.

Implements Section 6 Grammar and Mathematical Tablet Redesign:
- Tablet structure: Problem section (𒂊𒁹 / PROBLEM), Procedures (𒁾𒊬 / RECIPE), Result section (𒅗𒁹 / RESULT)
- Prescriptions: Quantity establishment, Postfix calculations, Determinations, Atomic Retain, Domain searches
- Explicit exact rational numbers, first-class units, and implicit result inscription
"""

from __future__ import annotations

from typing import Any, List, Optional, Set

from dubsar.ast import (
    Assignment,
    BinaryOp,
    CallExpr,
    CompareExpr,
    Conditional,
    Declaration,
    Determination,
    DomainRepetition,
    EmptyLiteral,
    Expression,
    ExpressionStatement,
    FieldAccess,
    Identifier,
    InputExpr,
    IsExpr,
    NumberLiteral,
    OutputStatement,
    PostfixExpr,
    ProblemSection,
    Procedure,
    Program,
    Recipe,
    Repetition,
    ResultSection,
    RetainStatement,
    ReturnStatement,
    Statement,
    StringLiteral,
    TupleExpr,
    UnaryOp,
)
from dubsar.errors import DubSarSyntaxError
from dubsar.tokens import Token, TokenType


class Parser:
    """Recursive descent parser for DUB.SAR 1.0 executable mathematical tablets."""

    def __init__(self, tokens: List[Token], source_file: Optional[str] = None) -> None:
        if not tokens or tokens[-1].type != TokenType.EOF:
            last_line = tokens[-1].line if tokens else 1
            last_col = tokens[-1].col if tokens else 1
            self.tokens = list(tokens) + [Token(TokenType.EOF, "", last_line, last_col, "")]
        else:
            self.tokens = tokens
        self.source_file = source_file
        self.pos = 0
        self.in_repetition_range = False

    def parse(self) -> Program:
        """Parses a complete DUB.SAR tablet."""
        self._skip_newlines()
        prog = self._parse_tablet()
        self._expect(TokenType.EOF, "Expected end of tablet")
        return prog

    # ==========================================================================
    # Helper methods
    # ==========================================================================

    @property
    def current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF

    def _peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def _advance(self) -> Token:
        tok = self.current
        if self.pos < len(self.tokens):
            self.pos += 1
        return tok

    def _check(self, type_: TokenType) -> bool:
        return self.current.type == type_

    def _match(self, *types: TokenType) -> Optional[Token]:
        for t in types:
            if self._check(t):
                return self._advance()
        return None

    def _expect(self, type_: TokenType, err_msg: str) -> Token:
        if not self._check(type_):
            raise DubSarSyntaxError(
                f"{err_msg}, got {self.current.type.name} ({self.current.raw!r})",
                line=self.current.line,
                col=self.current.col,
                source_file=self.source_file,
            )
        return self._advance()

    def _skip_newlines(self) -> None:
        while self._check(TokenType.NEWLINE):
            self._advance()

    # ==========================================================================
    # Program / Tablet structure (§5, §6)
    # tablet ::= problem-section procedure-section* result-section
    # ==========================================================================

    def _parse_tablet(self) -> Program:
        node_line, node_col = self.current.line, self.current.col
        problem: Optional[ProblemSection] = None
        procedures: List[Procedure] = []
        result: Optional[ResultSection] = None

        self._skip_newlines()
        while not self._check(TokenType.EOF):
            if self._check(TokenType.RECIPE):
                proc = self._parse_procedure()
                procedures.append(proc)
            elif self._check(TokenType.PROBLEM):
                if problem is not None:
                    raise DubSarSyntaxError("Duplicate problem section on tablet", line=self.current.line, col=self.current.col)
                problem = self._parse_problem_section()
            elif self._check(TokenType.RESULT):
                if result is not None:
                    raise DubSarSyntaxError("Duplicate result section on tablet", line=self.current.line, col=self.current.col)
                result = self._parse_result_section()
            else:
                break
            self._skip_newlines()

        if problem is None:
            problem = ProblemSection(line=node_line, col=node_col)
        if result is None:
            result = ResultSection(line=node_line, col=node_col)

        return Program(
            problem=problem,
            procedures=procedures,
            result=result,
            line=node_line,
            col=node_col,
        )

    def _parse_problem_section(self) -> ProblemSection:
        tok = self._expect(TokenType.PROBLEM, "Expected tablet problem section ('𒂊𒁹' or 'problem')")
        self._match(TokenType.COLON)  # Optional colon
        body = self._parse_block()
        return ProblemSection(body=body, line=tok.line, col=tok.col)

    def _parse_result_section(self) -> ResultSection:
        tok = self._expect(TokenType.RESULT, "Expected tablet result section ('𒅗𒁹' or 'result')")
        self._match(TokenType.COLON)  # Optional colon
        body = self._parse_block(in_result=True)
        return ResultSection(body=body, line=tok.line, col=tok.col)

    def _parse_procedure(self) -> Procedure:
        tok = self._expect(TokenType.RECIPE, "Expected procedure/recipe declaration ('𒁾𒊬' or 'recipe')")
        name_tok = self._expect(TokenType.IDENTIFIER, "Expected procedure name")

        params: List[str] = []
        if self._match(TokenType.LPAREN):
            if not self._check(TokenType.RPAREN):
                p = self._expect(TokenType.IDENTIFIER, "Expected parameter identifier")
                params.append(p.value)
                while self._match(TokenType.COMMA):
                    p = self._expect(TokenType.IDENTIFIER, "Expected parameter identifier")
                    params.append(p.value)
            self._expect(TokenType.RPAREN, "Expected ')' after parameter list")
        else:
            # Space-separated parameters until ':'
            while self._check(TokenType.IDENTIFIER):
                p = self._advance()
                params.append(p.value)

        self._expect(TokenType.COLON, "Expected ':' after procedure signature")
        body = self._parse_block()

        return Procedure(
            name=name_tok.value,
            parameters=params,
            body=body,
            line=tok.line,
            col=tok.col,
        )

    # ==========================================================================
    # Blocks and Statements
    # block ::= NEWLINE INDENT statement+ DEDENT
    # ==========================================================================

    def _parse_block(self, in_result: bool = False) -> List[Statement]:
        self._expect(TokenType.NEWLINE, "Expected newline before indented block")
        self._skip_newlines()
        self._expect(TokenType.INDENT, "Expected indented block")

        statements: List[Statement] = []
        while not self._check(TokenType.DEDENT) and not self._check(TokenType.EOF):
            self._skip_newlines()
            if self._check(TokenType.DEDENT) or self._check(TokenType.EOF):
                break
            stmt = self._parse_statement()
            # In result section, implicit inscription: expressions become OutputStatement
            if in_result and isinstance(stmt, ExpressionStatement):
                stmt = OutputStatement(value=stmt.expr, line=stmt.line, col=stmt.col)
            statements.append(stmt)
            self._skip_newlines()

        self._expect(TokenType.DEDENT, "Expected dedent at end of block")
        return statements

    def _parse_statement(self) -> Statement:
        tok = self.current

        # Finite Domain Repetition: consider cycle from 1 through limit:
        if self._check(TokenType.CONSIDER):
            return self._parse_domain_repetition()

        # Atomic Selection: retain candidate when error is lesser than best.error
        if self._check(TokenType.RETAIN):
            return self._parse_retain()

        # Conditional: 𒂊𒀀 / if / when
        if self._check(TokenType.WHEN):
            return self._parse_conditional()

        # Repetition: 𒄀 / repeat
        if self._check(TokenType.REPEAT):
            return self._parse_repetition()

        # Return: 𒄑 / return
        if self._check(TokenType.RETURN):
            return self._parse_return()

        # Output / Inscribe: 𒁹𒀀 / inscribe / output
        if self._check(TokenType.INSCRIBE):
            return self._parse_output()

        # Input statement: 𒀀𒁹 / ask / input
        if self._check(TokenType.ASK):
            input_expr = self._parse_input_expr()
            self._match(TokenType.NEWLINE)
            return ExpressionStatement(expr=input_expr, line=input_expr.line, col=input_expr.col)

        # Lookahead for declaration (name : expr) or assignment (name := expr or tuple unpack)
        if self._check(TokenType.IDENTIFIER):
            next1 = self._peek(1)
            # Quantity establishment: name : ...
            if next1.type == TokenType.COLON:
                return self._parse_establishment()

            # Single assignment: name := expr
            if next1.type == TokenType.ASSIGN:
                return self._parse_assignment()

            # Multiple assignment unpack: id1, id2, ... := expr
            if next1.type == TokenType.COMMA:
                is_tuple_assign = False
                j = 1
                while self._peek(j).type in (TokenType.IDENTIFIER, TokenType.COMMA):
                    if self._peek(j).type == TokenType.COMMA and self._peek(j + 1).type == TokenType.IDENTIFIER:
                        j += 2
                    else:
                        break
                if self._peek(j).type == TokenType.ASSIGN:
                    return self._parse_assignment()

        # Anonymous stack calculation / expression statement
        # Check if line contains a postfix sequence (e.g. 1 2 add)
        line_toks = self._peek_line_tokens()
        if len(line_toks) > 1 and any(self._is_op_token(t) for t in line_toks):
            # Consume tokens on line
            for _ in range(len(line_toks)):
                self._advance()
            self._match(TokenType.NEWLINE)
            steps = self._parse_postfix_steps([line_toks])
            return ExpressionStatement(
                expr=PostfixExpr(steps=steps, line=tok.line, col=tok.col),
                line=tok.line,
                col=tok.col,
            )

        expr = self._parse_expression()
        if self._match(TokenType.INSCRIBE) or self.current.raw in ("inscribe", "𒁹𒀀", "output"):
            self._match(TokenType.NEWLINE)
            return OutputStatement(value=expr, line=expr.line, col=expr.col)

        self._match(TokenType.NEWLINE)
        return ExpressionStatement(expr=expr, line=expr.line, col=expr.col)

    def _peek_line_tokens(self) -> List[Token]:
        res: List[Token] = []
        j = 0
        while True:
            t = self._peek(j)
            if t.type in (TokenType.NEWLINE, TokenType.DEDENT, TokenType.EOF):
                break
            res.append(t)
            j += 1
        return res

    def _parse_domain_repetition(self) -> Repetition:
        tok = self._expect(TokenType.CONSIDER, "Expected 'consider' or '𒄀'")
        target_tok = self._expect(TokenType.IDENTIFIER, "Expected domain variable identifier")

        # Optional 'from' / 'ta' / '𒋫'
        if self._check(TokenType.FROM) or (self._check(TokenType.MINUS) and self.current.raw in ("ta", "𒋫")):
            self._advance()

        self.in_repetition_range = True
        try:
            first_expr = self._parse_sum()
        finally:
            self.in_repetition_range = False

        if self._match(TokenType.COLON):
            body = self._parse_block()
            return Repetition(
                target=target_tok.value,
                start=None,
                end=first_expr,
                body=body,
                line=tok.line,
                col=tok.col,
            )

        # Separator: 'through', 'to', '..', 'iti', '𒌗'
        self._expect(TokenType.THROUGH, "Expected 'through', 'to', or '𒌗' in domain range")

        end_expr = self._parse_sum()

        self._expect(TokenType.COLON, "Expected ':' after domain specification")
        body = self._parse_block()

        return DomainRepetition(
            target=target_tok.value,
            start=first_expr,
            end=end_expr,
            body=body,
            line=tok.line,
            col=tok.col,
        )

    def _parse_retain(self) -> RetainStatement:
        tok = self._expect(TokenType.RETAIN, "Expected 'retain' or '𒋼'")
        candidate_tok = self._expect(TokenType.IDENTIFIER, "Expected candidate identifier")

        # Optional condition marker: 'when', 'if', 'e-a', '𒂊𒀀'
        if self._check(TokenType.WHEN):
            self._advance()

        cond_expr = self._parse_expression()
        self._match(TokenType.NEWLINE)

        target = "best"
        if isinstance(cond_expr, CompareExpr) and isinstance(cond_expr.right, FieldAccess) and isinstance(cond_expr.right.record, Identifier):
            target = cond_expr.right.record.name
        elif isinstance(cond_expr, IsExpr) and isinstance(cond_expr.target, Identifier):
            target = cond_expr.target.name

        return RetainStatement(
            candidate=candidate_tok.value,
            condition=cond_expr,
            target=target,
            line=tok.line,
            col=tok.col,
        )

    def _parse_establishment(self) -> Statement:
        name_tok = self._expect(TokenType.IDENTIFIER, "Expected identifier in quantity establishment")
        self._expect(TokenType.COLON, "Expected ':' after identifier")

        # Case 1: Indented block follows
        if self._check(TokenType.NEWLINE):
            self._advance()
            self._skip_newlines()
            self._expect(TokenType.INDENT, "Expected indented calculation or determination block")

            block_tokens: List[List[Token]] = []
            while not self._check(TokenType.DEDENT) and not self._check(TokenType.EOF):
                self._skip_newlines()
                if self._check(TokenType.DEDENT) or self._check(TokenType.EOF):
                    break
                line_toks: List[Token] = []
                while not self._check(TokenType.NEWLINE) and not self._check(TokenType.DEDENT) and not self._check(TokenType.EOF):
                    line_toks.append(self._advance())
                if line_toks:
                    block_tokens.append(line_toks)
                self._skip_newlines()

            self._expect(TokenType.DEDENT, "Expected dedent at end of block")

            # Check if block contains any mathematical operators
            has_operator = False
            for line_t in block_tokens:
                for t in line_t:
                    if self._is_op_token(t):
                        has_operator = True
                        break
                if has_operator:
                    break

            if has_operator:
                # Multiline postfix calculation
                steps = self._parse_postfix_steps(block_tokens)
                return Declaration(
                    name=name_tok.value,
                    value=PostfixExpr(steps=steps, line=name_tok.line, col=name_tok.col),
                    line=name_tok.line,
                    col=name_tok.col,
                )
            else:
                # Determination record definition
                fields = []
                field_values = {}
                for line_t in block_tokens:
                    if len(line_t) == 1 and line_t[0].type == TokenType.IDENTIFIER:
                        fields.append(line_t[0].value)
                    elif len(line_t) >= 3 and line_t[0].type == TokenType.IDENTIFIER and line_t[1].type == TokenType.COLON:
                        fname = line_t[0].value
                        fields.append(fname)
                        sub_p = Parser(line_t[2:], source_file=self.source_file)
                        field_values[fname] = sub_p._parse_expression()
                    else:
                        for t in line_t:
                            if t.type == TokenType.IDENTIFIER:
                                fields.append(t.value)

                return Determination(
                    name=name_tok.value,
                    fields=fields,
                    field_values=field_values if field_values else None,
                    line=name_tok.line,
                    col=name_tok.col,
                )

        # Case 2: On the same line
        # 1) empty / none / nu / 𒉡
        if self._check(TokenType.EMPTY) or self.current.raw in ("empty", "none", "nu", "𒉡"):
            tok_empty = self._advance()
            self._match(TokenType.NEWLINE)
            return Declaration(
                name=name_tok.value,
                value=EmptyLiteral(value="empty", line=tok_empty.line, col=tok_empty.col),
                line=name_tok.line,
                col=name_tok.col,
            )

        # 2) ask / input
        if self._check(TokenType.ASK) or self.current.raw in ("ask", "input", "a-dis", "a-diš", "𒀀𒁹"):
            input_expr = self._parse_input_expr()
            self._match(TokenType.NEWLINE)
            return Declaration(
                name=name_tok.value,
                value=input_expr,
                line=name_tok.line,
                col=name_tok.col,
            )

        # 3) Collect line tokens
        line_tokens: List[Token] = []
        while not self._check(TokenType.NEWLINE) and not self._check(TokenType.EOF):
            line_tokens.append(self._advance())
        self._match(TokenType.NEWLINE)

        # Check for single-line postfix calculation
        if len(line_tokens) > 1 and any(self._is_op_token(t) for t in line_tokens):
            # Check if this is a postfix expression (ends with operator)
            if self._is_op_token(line_tokens[-1]):
                steps = self._parse_postfix_steps([line_tokens])
                return Declaration(
                    name=name_tok.value,
                    value=PostfixExpr(steps=steps, line=name_tok.line, col=name_tok.col),
                    line=name_tok.line,
                    col=name_tok.col,
                )

        # Check if comma-separated determination
        if any(t.type == TokenType.COMMA for t in line_tokens):
            fields = [t.value for t in line_tokens if t.type == TokenType.IDENTIFIER]
            return Determination(
                name=name_tok.value,
                fields=fields,
                line=name_tok.line,
                col=name_tok.col,
            )

        # Standard expression parsing
        sub_parser = Parser(line_tokens, source_file=self.source_file)
        val_expr = sub_parser._parse_expression()
        unit_str = None
        if sub_parser._check(TokenType.IDENTIFIER) and not sub_parser._is_op_token(sub_parser.current):
            unit_str = sub_parser._advance().value

        return Declaration(
            name=name_tok.value,
            value=val_expr,
            unit=unit_str,
            line=name_tok.line,
            col=name_tok.col,
        )

    def _is_op_token(self, tok: Token) -> bool:
        if tok.type in (
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.STAR,
            TokenType.SLASH,
            TokenType.MOD,
            TokenType.POW,
            TokenType.FLOOR,
            TokenType.CEIL,
            TokenType.NEAREST,
            TokenType.ABSOLUTE,
        ):
            return True
        r = tok.raw.lower()
        return r in (
            "add", "zi", "𒍣", "+",
            "subtract", "sub", "ta", "𒋫", "-",
            "multiply", "mul", "sha", "ša", "𒊭", "*",
            "divide", "div", "ni", "𒉌", "/",
            "floor", "gur", "гур",
            "ceil", "nim", "𒉏",
            "nearest", "round", "ri", "𒊑",
            "absolute", "abs", "te", "𒋼",
            "lesser", "tur", "𒌉", "<",
            "greater", "gal", "𒃲", ">",
            "equal", "sa", "sá", "𒊓", "==",
        )

    def _canonical_op_name(self, tok: Token) -> str:
        r = tok.raw.lower()
        if r in ("add", "zi", "𒍣", "+"):
            return "add"
        if r in ("subtract", "sub", "ta", "𒋫", "-"):
            return "subtract"
        if r in ("multiply", "mul", "sha", "ša", "𒊭", "*"):
            return "multiply"
        if r in ("divide", "div", "ni", "𒉌", "/"):
            return "divide"
        if r in ("floor", "gur", "гур"):
            return "floor"
        if r in ("ceil", "nim", "𒉏"):
            return "ceil"
        if r in ("nearest", "round", "ri", "𒊑"):
            return "nearest"
        if r in ("absolute", "abs", "te", "𒋼"):
            return "absolute"
        if r in ("lesser", "tur", "𒌉", "<"):
            return "lesser"
        if r in ("greater", "gal", "𒃲", ">"):
            return "greater"
        if r in ("equal", "sa", "sá", "𒊓", "=="):
            return "equal"
        if r in ("not-equal", "!="):
            return "not-equal"
        return r

    def _parse_postfix_steps(self, token_lines: List[List[Token]]) -> List[Any]:
        flat: List[Token] = [t for line in token_lines for t in line]
        steps: List[Any] = []
        i = 0
        n = len(flat)
        while i < n:
            t = flat[i]
            if self._is_op_token(t):
                steps.append(self._canonical_op_name(t))
                i += 1
            elif t.type == TokenType.NUMBER:
                val = t.value
                unit = None
                if i + 1 < n and flat[i + 1].type in (TokenType.IDENTIFIER, TokenType.THROUGH) and not self._is_op_token(flat[i + 1]):
                    unit = flat[i + 1].value
                    i += 1
                steps.append(NumberLiteral(value=val, unit=unit, line=t.line, col=t.col))
                i += 1
            elif t.type == TokenType.IDENTIFIER:
                # Field access id.field
                if i + 2 < n and flat[i + 1].type == TokenType.DOT and flat[i + 2].type == TokenType.IDENTIFIER:
                    steps.append(FieldAccess(record=Identifier(name=t.value, line=t.line, col=t.col), field=flat[i + 2].value, line=t.line, col=t.col))
                    i += 3
                else:
                    steps.append(Identifier(name=t.value, line=t.line, col=t.col))
                    i += 1
            elif t.type == TokenType.STRING:
                steps.append(StringLiteral(value=t.value, line=t.line, col=t.col))
                i += 1
            elif t.type == TokenType.EMPTY or t.raw in ("empty", "none", "nu", "𒉡"):
                steps.append(EmptyLiteral(value="empty", line=t.line, col=t.col))
                i += 1
            else:
                i += 1
        return steps

    def _parse_assignment(self) -> Assignment:
        line, col = self.current.line, self.current.col
        targets: List[str] = []

        first = self._expect(TokenType.IDENTIFIER, "Expected identifier in assignment target")
        targets.append(first.value)

        while self._match(TokenType.COMMA):
            nxt = self._expect(TokenType.IDENTIFIER, "Expected identifier in assignment target list")
            targets.append(nxt.value)

        self._expect(TokenType.ASSIGN, "Expected ':=' in assignment")

        first_expr = self._parse_expression()
        if len(targets) > 1 and self._match(TokenType.COMMA):
            elements = [first_expr]
            nxt_e = self._parse_expression()
            elements.append(nxt_e)
            while self._match(TokenType.COMMA):
                elements.append(self._parse_expression())
            val_expr: Expression = TupleExpr(elements=elements, line=first_expr.line, col=first_expr.col)
        else:
            val_expr = first_expr

        self._match(TokenType.NEWLINE)
        return Assignment(
            targets=targets,
            value=val_expr,
            line=line,
            col=col,
        )

    def _parse_conditional(self) -> Conditional:
        tok = self._expect(TokenType.WHEN, "Expected '𒂊𒀀', 'when', or 'if'")
        cond_expr = self._parse_expression()
        self._expect(TokenType.COLON, "Expected ':' after conditional expression")
        body = self._parse_block()

        alternative = None
        self._skip_newlines()
        if self._check(TokenType.ELSE):
            self._advance()
            self._expect(TokenType.COLON, "Expected ':' after 'nu-e-a' or 'else'")
            alternative = self._parse_block()

        return Conditional(
            condition=cond_expr,
            body=body,
            alternative=alternative,
            line=tok.line,
            col=tok.col,
        )

    def _parse_repetition(self) -> Repetition:
        tok = self._expect(TokenType.REPEAT, "Expected '𒄀' or 'repeat'")
        target_tok = self._expect(TokenType.IDENTIFIER, "Expected loop variable identifier")

        self.in_repetition_range = True
        try:
            e1 = self._parse_expression()
        finally:
            self.in_repetition_range = False

        if self._match(TokenType.THROUGH):
            start_expr = e1
            end_expr = self._parse_expression()
        else:
            start_expr = None
            end_expr = e1

        self._expect(TokenType.COLON, "Expected ':' after repetition range")
        body = self._parse_block()

        return Repetition(
            target=target_tok.value,
            start=start_expr,
            end=end_expr,
            body=body,
            line=tok.line,
            col=tok.col,
        )

    def _parse_return(self) -> ReturnStatement:
        tok = self._expect(TokenType.RETURN, "Expected '𒄑' or 'return'")
        values: List[Expression] = []

        if not self._check(TokenType.NEWLINE) and not self._check(TokenType.DEDENT) and not self._check(TokenType.EOF):
            v1 = self._parse_expression()
            values.append(v1)
            while self._match(TokenType.COMMA):
                values.append(self._parse_expression())

        self._match(TokenType.NEWLINE)
        return ReturnStatement(values=values, line=tok.line, col=tok.col)

    def _parse_output(self) -> OutputStatement:
        tok = self._expect(TokenType.INSCRIBE, "Expected '𒁹𒀀', 'inscribe', or 'output'")
        val_expr = self._parse_expression()
        self._match(TokenType.NEWLINE)
        return OutputStatement(value=val_expr, line=tok.line, col=tok.col)

    # ==========================================================================
    # Expressions (Section 6 EBNF Grammar)
    # ==========================================================================

    def _parse_expression(self) -> Expression:
        return self._parse_comparison()

    def _parse_comparison(self) -> Expression:
        left = self._parse_sum()

        # Check for 'is' predicate: 'error is lesser than best.error', 'best is empty'
        if self._check(TokenType.IS) or self.current.raw in ("is", "me", "𒈨"):
            is_tok = self._advance()
            if self._check(TokenType.LESSER) or self.current.raw in ("lesser", "tur", "𒌉"):
                self._advance()
                if self._check(TokenType.THAN) or self.current.raw in ("than", "ta", "𒋫"):
                    self._advance()
                    right = self._parse_sum()
                    return CompareExpr(left=left, relation="lesser", right=right, line=is_tok.line, col=is_tok.col)
                return CompareExpr(left=left, relation="lesser", right=None, line=is_tok.line, col=is_tok.col)
            elif self._check(TokenType.GREATER) or self.current.raw in ("greater", "gal", "𒃲"):
                self._advance()
                if self._check(TokenType.THAN) or self.current.raw in ("than", "ta", "𒋫"):
                    self._advance()
                    right = self._parse_sum()
                    return CompareExpr(left=left, relation="greater", right=right, line=is_tok.line, col=is_tok.col)
                return CompareExpr(left=left, relation="greater", right=None, line=is_tok.line, col=is_tok.col)
            elif self._check(TokenType.EMPTY) or self.current.raw in ("empty", "none", "nu", "𒉡"):
                self._advance()
                return IsExpr(target=left, predicate="empty", line=is_tok.line, col=is_tok.col)

        while (
            self._check(TokenType.EQ)
            or self._check(TokenType.NEQ)
            or self._check(TokenType.LT)
            or self._check(TokenType.LTE)
            or self._check(TokenType.GT)
            or self._check(TokenType.GTE)
            or self._check(TokenType.LESSER)
            or self._check(TokenType.GREATER)
            or self._check(TokenType.EQUAL)
            or self.current.raw in ("𒌉", "𒃲", "𒊓")
        ):
            op_tok = self._advance()
            op_str = op_tok.raw
            if op_str in ("𒌉", "lesser"):
                op_str = "<"
            elif op_str in ("𒃲", "greater"):
                op_str = ">"
            elif op_str in ("𒊓", "equal"):
                op_str = "=="
            right = self._parse_sum()
            left = BinaryOp(
                left=left,
                op=op_str,
                right=right,
                line=op_tok.line,
                col=op_tok.col,
            )
        return left

    def _parse_sum(self) -> Expression:
        left = self._parse_product()
        while self._check(TokenType.PLUS) or self._check(TokenType.MINUS):
            op_tok = self._advance()
            right = self._parse_product()
            left = BinaryOp(
                left=left,
                op=op_tok.raw,
                right=right,
                line=op_tok.line,
                col=op_tok.col,
            )
        return left

    def _parse_product(self) -> Expression:
        left = self._parse_power()
        while self._check(TokenType.STAR) or self._check(TokenType.SLASH) or self._check(TokenType.MOD):
            op_tok = self._advance()
            right = self._parse_power()
            left = BinaryOp(
                left=left,
                op=op_tok.raw,
                right=right,
                line=op_tok.line,
                col=op_tok.col,
            )
        return left

    def _parse_power(self) -> Expression:
        left = self._parse_unary()
        if self._match(TokenType.POW):
            op_tok = self._peek(-1)
            right = self._parse_unary()
            return BinaryOp(
                left=left,
                op="**",
                right=right,
                line=op_tok.line,
                col=op_tok.col,
            )
        return left

    def _parse_unary(self) -> Expression:
        if self._check(TokenType.MINUS) or self._check(TokenType.NOT):
            op_tok = self._advance()
            operand = self._parse_unary()
            return UnaryOp(
                op=op_tok.raw,
                operand=operand,
                line=op_tok.line,
                col=op_tok.col,
            )
        return self._parse_primary()

    def _parse_primary(self) -> Expression:
        tok = self.current

        # Number literal with optional unit
        if self._check(TokenType.NUMBER):
            num_tok = self._advance()
            unit_str = None
            if self._check(TokenType.IDENTIFIER) and not self._is_op_token(self.current) and self.current.line == num_tok.line:
                unit_tok = self._advance()
                unit_str = unit_tok.value
            elif (
                not self.in_repetition_range
                and self._check(TokenType.THROUGH)
                and self.current.value == "𒌗"
                and self.current.line == num_tok.line
            ):
                self._advance()
                unit_str = "𒌗"

            return NumberLiteral(
                value=num_tok.value,
                unit=unit_str,
                line=num_tok.line,
                col=num_tok.col,
            )

        # String literal
        if self._check(TokenType.STRING):
            str_tok = self._advance()
            return StringLiteral(
                value=str_tok.value,
                line=str_tok.line,
                col=str_tok.col,
            )

        # Empty literal: empty / none / nu / 𒉡
        if self._check(TokenType.EMPTY) or tok.raw in ("empty", "none", "nu", "𒉡"):
            tok_empty = self._advance()
            return EmptyLiteral(value="empty", line=tok_empty.line, col=tok_empty.col)

        # Input expression: 𒀀𒁹("...") or input("...") or ask "..."
        if self._check(TokenType.ASK):
            return self._parse_input_expr()

        # Parenthesized expression: ( expr )
        if self._match(TokenType.LPAREN):
            expr = self._parse_expression()
            self._expect(TokenType.RPAREN, "Expected ')' after parenthesized expression")
            return expr

        # Identifier or Call or Field Access or Builtin Math Operation Call
        if self._check(TokenType.IDENTIFIER) or self.current.type in (
            TokenType.FLOOR,
            TokenType.CEIL,
            TokenType.NEAREST,
            TokenType.ABSOLUTE,
        ):
            ident_tok = self._advance()

            # Record field access: record.field
            if self._match(TokenType.DOT):
                field_tok = self._expect(TokenType.IDENTIFIER, "Expected field identifier after '.'")
                return FieldAccess(
                    record=Identifier(name=str(ident_tok.value), line=ident_tok.line, col=ident_tok.col),
                    field=field_tok.value,
                    line=ident_tok.line,
                    col=ident_tok.col,
                )

            # Record field access: field of record
            if self._check(TokenType.OF) or self.current.raw in ("of", "ša", "sha", "𒊭"):
                self._advance()
                rec_tok = self._expect(TokenType.IDENTIFIER, "Expected record identifier after 'of'")
                return FieldAccess(
                    record=Identifier(name=rec_tok.value, line=rec_tok.line, col=rec_tok.col),
                    field=str(ident_tok.value),
                    line=ident_tok.line,
                    col=ident_tok.col,
                )

            # Procedure call: id(args...)
            if self._match(TokenType.LPAREN):
                args: List[Expression] = []
                if not self._check(TokenType.RPAREN):
                    args.append(self._parse_expression())
                    while self._match(TokenType.COMMA):
                        args.append(self._parse_expression())
                self._expect(TokenType.RPAREN, "Expected ')' after procedure arguments")
                callee_name = str(ident_tok.raw) if ident_tok.type != TokenType.IDENTIFIER else ident_tok.value
                return CallExpr(
                    callee=callee_name,
                    arguments=args,
                    line=ident_tok.line,
                    col=ident_tok.col,
                )

            if ident_tok.type in (TokenType.FLOOR, TokenType.CEIL, TokenType.NEAREST, TokenType.ABSOLUTE):
                raise DubSarSyntaxError(
                    f"Unexpected token in expression: {ident_tok.type.name} ({ident_tok.raw!r})",
                    line=ident_tok.line,
                    col=ident_tok.col,
                    source_file=self.source_file,
                )

            return Identifier(
                name=ident_tok.value,
                line=ident_tok.line,
                col=ident_tok.col,
            )

        raise DubSarSyntaxError(
            f"Unexpected token in expression: {tok.type.name} ({tok.raw!r})",
            line=tok.line,
            col=tok.col,
            source_file=self.source_file,
        )

    def _parse_input_expr(self) -> InputExpr:
        tok = self._expect(TokenType.ASK, "Expected '𒀀𒁹', 'ask', or 'input'")
        if self._match(TokenType.LPAREN):
            prompt_tok = self._expect(TokenType.STRING, "Expected string prompt in input expression")
            self._expect(TokenType.RPAREN, "Expected ')' after input prompt")
        else:
            prompt_tok = self._expect(TokenType.STRING, "Expected string prompt after ask")
        return InputExpr(
            prompt=prompt_tok.value,
            line=tok.line,
            col=tok.col,
        )
