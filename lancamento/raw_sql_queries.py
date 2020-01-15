from django.db import connection


def get_lancamentos(user=None):

    with connection.cursor() as cursor:
        sql = ('''
                 SELECT * FROM lancamento_lancamento l
                 WHERE (created_by_id = %s or %s is null)
               '''
        )

        cursor.execute(sql, [user, user])

        return dictfetchall(cursor)

def get_saldo(user=None):

    with connection.cursor() as cursor:
        sql = ('''
                   Select SUM(VALOR) SALDO
                   FROM
                   (
                   select SUM(l.valor)*-1  as valor from lancamento_lancamento l
                   where (l.created_by_id = %s or %s is null)
                   UNION
                   select SUM(r.valor)  as valor from lancamento_receita r
                   where (r.created_by_id = %s or %s is null)
                   )
               '''               
        )

        cursor.execute(sql, [user, user,
                             user, user])

        return dictfetchall(cursor)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


 