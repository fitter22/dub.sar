"""DUB.SAR 1.0 — Parser.

Implements Section 6 Grammar:
- Tablet structure: Problem section, Procedures, Result section
- Prescriptions: Declarations, Single/Tuple Assignments, Conditionals, Repetitions, Returns, Outputs
- Expressions with proper operator precedence, exact sexagesimal numbers, and first-class units
"""

from __future__ import annotations

from typing import List, Optional, Set

from dubsar.ast import (
    Assignment,
    BinaryOp,
    CallExpr,
    Conditional,
    Declaration,
    Expression,
    ExpressionStatement,
    Identifier,
    InputExpr,
    NumberLiteral,
    OutputStatement,
    ProblemSection,
    Procedure,
    Program,
    Repetition,
    ResultSection,
    ReturnStatement,
    Statement,
    StringLiteral,
    TupleExpr,
    UnaryOp,
)
from dubsar.errors import DubSarSyntaxError
from dubsar.tokens import Token, TokenType


class Parser:
    """Recursive descent parser for DUB.SAR 1.0."""

    def __init__(self, tokens: List[Token], source_file: Optional[str] = None) -> None:
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
        if self.pos < len(self.tokens) - 1:
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
        problem = self._parse_problem_section()
        self._skip_newlines()

        procedures: List[Procedure] = []
        while self._check(TokenType.PROCEDURE):
            proc = self._parse_procedure()
            procedures.append(proc)
            self._skip_newlines()

        result = self._parse_result_section()
        self._skip_newlines()

        return Program(
            problem=problem,
            procedures=procedures,
            result=result,
            line=node_line,
            col=node_col,
        )

    def _parse_problem_section(self) -> ProblemSection:
        tok = self._expect(TokenType.PROBLEM, "Expected tablet problem section ('𒂊𒁹' or 'PROBLEM')")
        self._match(TokenType.COLON)  # Optional colon
        body = self._parse_block()
        return ProblemSection(body=body, line=tok.line, col=tok.col)

    def _parse_result_section(self) -> ResultSection:
        tok = self._expect(TokenType.RESULT, "Expected tablet result section ('𒅗𒁹' or 'RESULT')")
        self._match(TokenType.COLON)  # Optional colon
        body = self._parse_block()
        return ResultSection(body=body, line=tok.line, col=tok.col)

    def _parse_procedure(self) -> Procedure:
        tok = self._expect(TokenType.PROCEDURE, "Expected procedure declaration ('𒁾𒊬' or 'procedure')")
        name_tok = self._expect(TokenType.IDENTIFIER, "Expected procedure name")
        self._expect(TokenType.LPAREN, "Expected '(' after procedure name")

        params: List[str] = []
        if not self._check(TokenType.RPAREN):
            p = self._expect(TokenType.IDENTIFIER, "Expected parameter identifier")
            params.append(p.value)
            while self._match(TokenType.COMMA):
                p = self._expect(TokenType.IDENTIFIER, "Expected parameter identifier")
                params.append(p.value)

        self._expect(TokenType.RPAREN, "Expected ')' after parameter list")
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

    def _parse_block(self) -> List[Statement]:
        self._expect(TokenType.NEWLINE, "Expected newline before indented block")
        self._skip_newlines()
        self._expect(TokenType.INDENT, "Expected indented block")

        statements: List[Statement] = []
        while not self._check(TokenType.DEDENT) and not self._check(TokenType.EOF):
            self._skip_newlines()
            if self._check(TokenType.DEDENT) or self._check(TokenType.EOF):
                break
            stmt = self._parse_statement()
            statements.append(stmt)
            self._skip_newlines()

        self._expect(TokenType.DEDENT, "Expected dedent at end of block")
        return statements

    def _parse_statement(self) -> Statement:
        tok = self.current

        # Conditional: 𒂊𒀀 / if
        if self._check(TokenType.IF):
            return self._parse_conditional()

        # Repetition: 𒄀 / repeat
        if self._check(TokenType.REPEAT):
            return self._parse_repetition()

        # Return: 𒄑 / return
        if self._check(TokenType.RETURN):
            return self._parse_return()

        # Output: 𒁹𒀀 / output
        if self._check(TokenType.OUTPUT):
            return self._parse_output()

        # Input statement
        if self._check(TokenType.INPUT):
            input_expr = self._parse_input_expr()
            self._match(TokenType.NEWLINE)
            return ExpressionStatement(expr=input_expr, line=input_expr.line, col=input_expr.col)

        # Lookahead for declaration (name : expr) or assignment (name := expr or tuple unpack)
        if self._check(TokenType.IDENTIFIER):
            next1 = self._peek(1)
            # Declaration: name : expr [unit]
            if next1.type == TokenType.COLON:
                return self._parse_declaration()

            # Single assignment: name := expr
            if next1.type == TokenType.ASSIGN:
                return self._parse_assignment()

            # Multiple assignment unpack: id1, id2, ... := expr
            if next1.type == TokenType.COMMA:
                # Check if this leads to :=
                is_tuple_assign = False
                j = 1
                while self._peek(j).type in (TokenType.IDENTIFIER, TokenType.COMMA):
                    if self._peek(j).type == TokenType.COMMA and self._peek(j + 1).type == TokenType.IDENTIFIER:
                        j += 2
                    else:
                        break
                if self._peek(j).type == TokenType.ASSIGN:
                    return self._parse_assignment()

        # General expression statement
        expr = self._parse_expression()
        self._match(TokenType.NEWLINE)
        return ExpressionStatement(expr=expr, line=expr.line, col=expr.col)

    def _parse_declaration(self) -> Declaration:
        name_tok = self._expect(TokenType.IDENTIFIER, "Expected identifier in declaration")
        self._expect(TokenType.COLON, "Expected ':' in declaration")
        val_expr = self._parse_expression()

        # Optional unit directly following expression on same line
        unit_str = None
        if self._check(TokenType.IDENTIFIER) and self.current.line == name_tok.line:
            unit_tok = self._advance()
            unit_str = unit_tok.value
        elif self._check(TokenType.RANGE_SEP) and self.current.value == "𒌗":
            # 𒌗 used as unit month
            self._advance()
            unit_str = "𒌗"

        self._match(TokenType.NEWLINE)
        return Declaration(
            name=name_tok.value,
            value=val_expr,
            unit=unit_str,
            line=name_tok.line,
            col=name_tok.col,
        )

    def _parse_assignment(self) -> Assignment:
        line, col = self.current.line, self.current.col
        targets: List[str] = []

        first = self._expect(TokenType.IDENTIFIER, "Expected identifier in assignment target")
        targets.append(first.value)

        while self._match(TokenType.COMMA):
            nxt = self._expect(TokenType.IDENTIFIER, "Expected identifier in assignment target list")
            targets.append(nxt.value)

        self._expect(TokenType.ASSIGN, "Expected ':=' in assignment")

        # Parse RHS
        first_expr = self._parse_expression()
        if len(targets) > 1 and self._match(TokenType.COMMA):
            # Comma-separated expression list on RHS
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
        tok = self._expect(TokenType.IF, "Expected '𒂊𒀀' or 'if'")
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

        # Range: single-bound (gi cycle 1000) or explicit-range (gi cycle 1 iti 1000)
        self.in_repetition_range = True
        try:
            e1 = self._parse_expression()
        finally:
            self.in_repetition_range = False

        if self._match(TokenType.RANGE_SEP):
            # Explicit range: start iti end
            start_expr = e1
            end_expr = self._parse_expression()
        else:
            # Single-bound: 1..end
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
        tok = self._expect(TokenType.OUTPUT, "Expected '𒁹𒀀' or 'output'")
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
        while self._check(TokenType.EQ) or self._check(TokenType.NEQ) or \
              self._check(TokenType.LT) or self._check(TokenType.LTE) or \
              self._check(TokenType.GT) or self._check(TokenType.GTE):
            op_tok = self._advance()
            right = self._parse_sum()
            left = BinaryOp(
                left=left,
                op=op_tok.raw,
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
            right = self._parse_unary()  # right-associative
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
            # Check if followed by unit identifier on the same line
            if self._check(TokenType.IDENTIFIER) and self.current.line == num_tok.line:
                unit_tok = self._advance()
                unit_str = unit_tok.value
            elif (
                not self.in_repetition_range
                and self._check(TokenType.RANGE_SEP)
                and self.current.value == "𒌗"
                and self.current.line == num_tok.line
            ):
                # 𒌗 used as unit month
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

        # Input expression: 𒀀𒁹("...") or input("...")
        if self._check(TokenType.INPUT):
            return self._parse_input_expr()

        # Parenthesized expression: ( expr )
        if self._match(TokenType.LPAREN):
            expr = self._parse_expression()
            self._expect(TokenType.RPAREN, "Expected ')' after parenthesized expression")
            return expr

        # Identifier or Call: identifier ( args? )
        if self._check(TokenType.IDENTIFIER):
            ident_tok = self._advance()
            if self._match(TokenType.LPAREN):
                # Function call
                args: List[Expression] = []
                if not self._check(TokenType.RPAREN):
                    args.append(self._parse_expression())
                    while self._match(TokenType.COMMA):
                        args.append(self._parse_expression())
                self._expect(TokenType.RPAREN, "Expected ')' after procedure arguments")
                return CallExpr(
                    callee=ident_tok.value,
                    arguments=args,
                    line=ident_tok.line,
                    col=ident_tok.col,
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
        tok = self._expect(TokenType.INPUT, "Expected '𒀀𒁹' or 'input'")
        self._expect(TokenType.LPAREN, "Expected '(' after input keyword")
        prompt_tok = self._expect(TokenType.STRING, "Expected string prompt in input expression")
        self._expect(TokenType.RPAREN, "Expected ')' after input prompt")
        return InputExpr(
            prompt=prompt_tok.value,
            line=tok.line,
            col=tok.col,
        )
