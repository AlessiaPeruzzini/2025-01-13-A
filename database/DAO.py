from database.DB_connect import DBConnect
from model.arco import Arco
from model.classification import Classification
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def getAllLocalizzazione():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select c.GeneID,
       c.Localization,
       g.Essential
from classification c, genes g
where c.GeneID = g.GeneID 

"""
            cursor.execute(query)

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(loca):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select c.GeneID,
       c.Localization,
       g.Essential
from classification c, genes g
where c.GeneID = g.GeneID and c.localization = %s"""
            cursor.execute(query, (loca,))

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges(loca, _idMapC):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select 
    i.GeneID1 as gen1,
    i.GeneID2 as gen2,
    sum(distinct g.Chromosome) as peso
from interactions i, classification c1, classification c2, genes g 
where i.GeneID1 = c1.GeneID
and i.GeneID2 = c2.GeneID
and g.GeneID in (i.GeneID1, i.GeneID2)
and c1.Localization = %s
and c2.Localization = %s
group by i.GeneID1, i.GeneID2"""
            cursor.execute(query, (loca,loca))

            for row in cursor:

                if row["gen1"] in _idMapC and row["gen2"] in _idMapC:
                    result.append(Arco(_idMapC[row["gen1"]], _idMapC[row["gen2"]], row["peso"]))

            cursor.close()
            cnx.close()
            return result
