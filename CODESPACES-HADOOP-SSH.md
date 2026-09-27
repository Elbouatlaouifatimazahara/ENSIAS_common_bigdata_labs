# Corriger l'erreur SSH entre conteneurs Hadoop sous Codespaces

## Le problème

`start-all.sh` échoue sur les slaves :

```
hadoop-slave1: ssh: connect to host hadoop-slave1 port 22: Connection timed out
```

SSH tourne bien sur les slaves. C'est le pare-feu du Codespace qui bloque le trafic entre conteneurs : dans `iptables-legacy`, la chaîne `FORWARD` est en `DROP` et n'autorise que `docker0`, pas le réseau créé par docker-compose.

Les avertissements `HADOOP_*_OPTS` sont normaux, ignorez-les.

## La correction

Dans le terminal du Codespace, pas dans un conteneur :

```bash
sudo iptables-legacy -P FORWARD ACCEPT
sudo iptables-legacy -I FORWARD -s 172.18.0.0/16 -d 172.18.0.0/16 -j ACCEPT
```

Si vos conteneurs ne sont pas en `172.18.x.x`, adaptez le sous-réseau. Pour le connaître : `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' cluster-master`.

## Relancer et vérifier

```bash
docker exec -it cluster-master bash

$HADOOP_HOME/sbin/stop-all.sh
$HADOOP_HOME/sbin/start-all.sh

hdfs dfsadmin -report | grep -i "live datanodes"
```

Vous devez obtenir `Live datanodes (2)`. Les interfaces web sont dans l'onglet **Ports** du Codespace : 9870 pour HDFS, 8088 pour YARN.

## À chaque redémarrage du Codespace

Les règles iptables sont perdues quand le Codespace s'arrête. Le plus simple : relancez les deux commandes de la section « La correction » après chaque `docker compose up -d`. C'est tout ce qui est nécessaire.

Pour éviter de les retaper, créez une fois pour toutes un fichier `fix-network.sh` à la racine de votre dépôt :

```bash
cat > fix-network.sh << 'EOF'
#!/bin/bash
sudo iptables-legacy -P FORWARD ACCEPT
sudo iptables-legacy -I FORWARD -s 172.18.0.0/16 -d 172.18.0.0/16 -j ACCEPT
echo "Reseau Docker debloque"
EOF

chmod +x fix-network.sh
```

Ensuite, après chaque redémarrage, une seule commande suffit :

```bash
./fix-network.sh
```
