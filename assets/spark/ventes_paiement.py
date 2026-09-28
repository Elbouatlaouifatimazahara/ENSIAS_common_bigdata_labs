# Lab préparatoire Spark — À vous de jouer
# Total des ventes par moyen de paiement, sur le cluster (YARN).
# Chaque ligne de purchases.txt : date \t heure \t magasin \t categorie \t montant \t paiement
#                                  [0]     [1]     [2]       [3]         [4]       [5]

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ventes-par-paiement").getOrCreate()
sc = spark.sparkContext
sc.setLogLevel("WARN")

ENTREE = "hdfs://hadoop-master:9000/user/root/input/purchases.txt"
SORTIE = "hdfs://hadoop-master:9000/user/root/output/ventes_paiement"

lignes = sc.textFile(ENTREE)
champs = lignes.map(lambda l: l.split("\t")).filter(lambda c: len(c) == 6)

# TODO 1 : produire des paires (moyen_de_paiement, montant) ; le montant doit être un float
paires = champs.map(lambda c: (None, 0.0))

# TODO 2 : additionner les montants par moyen de paiement
totaux = paires

# Affichage des 10 premiers totaux, du plus grand au plus petit
for paiement, total in totaux.takeOrdered(10, key=lambda kv: -kv[1]):
    print(paiement, round(total, 2))

# Écriture du résultat dans HDFS (écrase une éventuelle exécution précédente)
spark.createDataFrame(totaux, "paiement STRING, total DOUBLE").write.mode("overwrite").csv(SORTIE, sep="\t")

spark.stop()
