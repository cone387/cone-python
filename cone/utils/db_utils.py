# -*- coding:utf-8 -*-

# author: Cone
# datetime: 2022/10/20 下午5:20
# software: PyCharm
import json
import logging
try:
    from pymysql.err import IntegrityError
except ImportError:
    raise ImportError("please install pymysql first")


logger = logging.getLogger(__name__)


def build_insert_cmd(table, data: dict, option='insert'):
    columns = []
    values = []
    for key, value in data.items():
        if value is None:
            continue
        if isinstance(value, (list, dict)):
            data[key] = json.dumps(value, ensure_ascii=False)
        columns.append('`%s`' % key)
        values.append(f'%({key})s')
    return '{} into {}({}) values({})'.format(option, table, ','.join(columns), ','.join(values))


def insert_item(conn, cursor, item, table, option='insert') -> int:
    cmd = build_insert_cmd(table, item, option)
    try:
        cursor.execute(cmd, item)
        conn.commit()
        return 1
    except IntegrityError:
        logger.debug("insert duplicate: %s" % item)
        return 2
    except Exception as e:
        logger.exception("insert failed: %s, cmd is %s" % (e, cmd))
        return 0


def delete(conn, table, default_where=None, **where):
    children = [default_where] if default_where else []
    for key, value in where.items():
        if value is None:
            continue
        if isinstance(value, (str, int, float)):
            if '`' in key:
                children.append(f"{key} = '{value}'")
            else:
                children.append(f"`{key}` = '{value}'")
        else:
            raise Exception("invalid where value-type: %s" % type(value))
    assert children, "where can't be empty"
    cmd = 'delete from %s where %s' % (table, ' and '.join(children))
    with conn.cursor() as cursor:
        try:
            r = cursor.execute(cmd)
        except Exception as e:
            logger.exception("delete failed: %s, cmd is %s" % (e, cmd))
            return 0
    conn.commit()
    conn.close()
    logger.debug("delete %s rows from %s where %s" % (r, table, ' and '.join(children)))
    return r


def batch_insert(conn, table, items, option='insert'):
    s, f, d = 0, 0, 0
    with conn.cursor() as cursor:
        for item in items:
            cmd = build_insert_cmd(table, item, option=option)
            try:
                cursor.execute(cmd, item)
                s += 1
            except IntegrityError:
                d += 1
            except Exception as e:
                logger.exception("insert failed: %s, cmd is %s" % (e, cmd))
                f += 1
    conn.commit()
    conn.close()
    return s, f, d
