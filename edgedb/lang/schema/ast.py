##
# Copyright (c) 2016-present MagicStack Inc.
# All rights reserved.
#
# See LICENSE for details.
##


import typing

from edgedb.lang.common import enum as s_enum
from edgedb.lang.common import ast, parsing
from edgedb.lang.edgeql import ast as qlast


class Base(ast.AST):
    __ast_hidden__ = {'context'}
    context: parsing.ParserContext

    def _extra_repr(self):
        return ''

    def __repr__(self):
        ar = self._extra_repr()
        return '<{}.{} at {:#x}{}>'.format(self.__class__.ns,
                                           self.__class__.__name__,
                                           id(self),
                                           ar)


class Attribute(Base):
    name: qlast.ObjectRef
    value: qlast.Base


class Constraint(Base):
    args: typing.List[qlast.FuncArg]
    attributes: typing.List[Attribute]
    delegated: bool = False
    name: qlast.ObjectRef
    subject: typing.Optional[qlast.Expr]


class Policy(Base):
    __fields = ['event', 'action']  # TODO: type this


class Pointer(Base):
    name: qlast.ObjectRef

    # Computable links don't have a target
    target: typing.Optional[typing.List[qlast.TypeName]]

    attributes: typing.List[Attribute]
    constraints: typing.List[Constraint]
    policies: typing.List[Policy]

    required: bool = False

    # Expression of a computable link
    expr: qlast.Base = None


class Index(Base):
    name: qlast.ObjectRef
    expression: qlast.Base


class Property(Pointer):
    pass


class Link(Pointer):
    properties: typing.List[Property]


# # XXX: to be killed
# class LinkProperty(Property):
#     pass


class Declaration(Base):
    name: str
    extends: typing.List[qlast.TypeName]
    attributes: typing.List[Attribute]


class ActionDeclaration(Declaration):
    pass


class ScalarTypeDeclaration(Declaration):
    abstract: bool = False
    final: bool = False
    constraints: typing.List[Constraint]


class AttributeDeclaration(Declaration):
    type: typing.Optional[qlast.TypeName]


class ObjectTypeDeclaration(Declaration):
    abstract: bool = False
    final: bool = False
    links: typing.List[Link]
    properties: typing.List[Property]
    indexes: typing.List[Index]
    constraints: typing.List[Constraint]


class ConstraintDeclaration(Declaration):
    abstract: bool = False
    args: typing.List[qlast.Base]
    subject: typing.Optional[qlast.Expr]


class EventDeclaration(Declaration):
    pass


class ViewDeclaration(Declaration):
    pass


class Language(s_enum.StrEnum):
    SQL = 'SQL'
    EdgeQL = 'EDGEQL'


class FunctionCode(Base):
    language: Language
    code: qlast.Base
    from_name: str


class FunctionDeclaration(Declaration):
    args: list
    returning: qlast.TypeName
    aggregate: bool = False
    initial_value: qlast.Base
    code: FunctionCode
    set_returning: str = ''


class BasePointerDeclaration(Declaration):
    abstract: bool = False
    indexes: typing.List[Index]
    constraints: typing.List[Constraint]
    policies: typing.List[Policy]


class PropertyDeclaration(BasePointerDeclaration):
    pass


class LinkDeclaration(BasePointerDeclaration):
    properties: typing.List[Property]


class Import(Base):
    modules: list


class ImportModule(Base):
    module: str
    alias: str = None


class Schema(Base):
    # TODO: Remove union type
    declarations: typing.List[typing.Union[Declaration, Import]]
