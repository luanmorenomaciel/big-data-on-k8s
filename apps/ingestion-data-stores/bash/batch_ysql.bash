cd "/Users/luanmorenomaciel/BitBucket/big-data-on-k8s/apps/ingestion-data-stores"

for i in {1..100}
do
   python3.9 cli.py 'ysql'
done
