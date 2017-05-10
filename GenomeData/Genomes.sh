filename="SampleReferences.csv"
refquery=`cat Queries/RefQuery.txt`
altquery=`cat Queries/AltQuery.txt`
samplerefquery=`cat Queries/SampleRefQuery.txt`
samplequery=`cat Queries/SampleQuery.txt`
chromosome="17"
directory="chr17"

mkdir "$directory"

samplerefquery="${samplerefquery/chromosome/$chromosome}"
echo "$samplerefquery"
#bq --format=csv query --use_legacy_sql=false "$samplerefquery" > "$directory"/"$filename"

refquery="${refquery/chromosome/$chromosome}"
echo "$refquery"
#bq --format=csv query --use_legacy_sql=false "$refquery" > "$directory"/Reference.csv 

altquery="${altquery/chromosome/$chromosome}"
echo "$altquery"
#bq --format=csv query --use_legacy_sql=false "$altquery" > "$directory"/Alternate.csv

while read line
do
SampleReference="$line"
q="${samplequery/SampleReference/$SampleReference}"
q="${q/chromosome/$chromosome}"
echo "$q"
echo "SampleGenotype_"$SampleReference".csv"
#bq --format=csv query --use_legacy_sql=false "$q" >"$directory"/SampleGenotype_"$SampleReference".csv
done < "$directory"/"$filename"
