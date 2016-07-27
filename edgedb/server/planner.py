##
# Copyright (c) 2016 MagicStack Inc.
# All rights reserved.
#
# See LICENSE for details.
##


from edgedb.lang import edgeql
from edgedb.lang.edgeql import ast as qlast
from edgedb.lang.schema import ddl as s_ddl


def plan_statement(stmt, backend):
    if isinstance(stmt, qlast.DDLNode):
        return s_ddl.delta_from_ddl(stmt)

    else:
        ir = edgeql.compile_ast_to_ir(stmt, schema=backend.schema)
        query = backend.compile(ir, output_format='json')

        return query