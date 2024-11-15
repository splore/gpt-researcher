import logging
from typing import List, Union
from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta


logger = logging.getLogger(__name__)


async def create_rows(psql_sess: AsyncSession, table: DeclarativeMeta, rows: List[dict],
                      returning: List[str] = None) -> Union[List, None]:
    """
    This async function insert rows into any psql table.

    Args:
        psql_sess (AsyncSession): the psql db connection session.
        table (DeclarativeMeta): the psql table ORM for insertion mapping.
        rows (list[dict]): list of data rows to insert, where keys are the mapped column names.
        returning (list[str]): list of columns to return upon insertion.

    Returns:
        list|None: list of fields to return corresponding to inserted rows if required.

    """
    result = None
    if returning:
        returning = [getattr(table, col) for col in returning]
        statement = insert(table).returning(*returning)
        resp = await psql_sess.execute(statement, rows)
        result = list(resp.all())
    else:
        statement = insert(table)
        _ = await psql_sess.execute(statement, rows)
    await psql_sess.commit()
    return result


async def update_row_by_id(psql_sess: AsyncSession, table: DeclarativeMeta, row: dict, row_id: str, returning: List[str] = None):
    """
        This async function updates any psql table row by id.

        Args:
            psql_sess (AsyncSession): the psql db connection session.
            table (DeclarativeMeta): the psql table ORM for insertion mapping.
            row (dict): data row to update, where keys are the mapped column names.
            row_id (str): row id to update
            returning (list[str]): list of columns to return upon insertion.

        Returns:
            list|None: list of fields to return corresponding to inserted rows if required.
    """

    result = None
    if returning:
        returning = [getattr(table, col) for col in returning]
        statement = update(table).returning(*returning).values(row).where(table.id == row_id)
        resp = await psql_sess.execute(statement)
        result = list(resp.all())
    else:
        statement = update(table).values(row).where(table.id == row_id)
        _ = await psql_sess.execute(statement)
    await psql_sess.commit()
    return result
