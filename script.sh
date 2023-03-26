#!/bin/sh

cours_content=$(curl https://www.boursorama.com/cours/1rPMC/)
historic_content=$(curl https://www.boursorama.com/cours/historique/1rPMC)
# echo $(echo $cours_content | grep -oP 'LVMH.*span.*c-instrument c-instrument--last.*?\K[\d\.]+')
transactions_table=$(echo $cours_content | grep -oP 'c-block.*Dernières transactions.*?c-table c-table--generic.*?>\K.*?(?=</table>)')
table_header=$(echo $transactions_table | grep -oP 'h3.*?c-table__title.*?>\K.*?(?=</h3>)')
table_header=$(echo $(echo "$historic_table_header") | sed 's/ /;/g')
table_rows=$(echo $transactions_table | grep -oP '<td.*?>\K.*?(?=</td>)')
columns=$(echo "$table_header" | grep -o ";" | wc -l)
columns=$((columns+1))
# echo $(echo $table_header | sed 's/ /;/g') > data.csv
x=0
row=""
for i in $table_rows; do
    if [ "$row" = "" ]; then
        row="$i"
    else
        row="$row;$i"
    fi
    x=$((x+1))
    if [ $x -eq $columns ]; then
        # echo "$row" >> data.csv
        row=""
        x=0
    fi
done

historic_table_content=$(echo $historic_content | grep -oP '<table class="c-table".*?>.*Date.*?(?=</table>)')
historic_table_header=$(echo $historic_table_content | grep -oP 'th class="c-table__cell.*?>\K.*?(?=</th>)' | sed 's/ //g')
historic_table_header=$(echo $(echo "$historic_table_header") | sed 's/ /;/g')
historic_table_rows=$(echo $historic_table_content | grep -oP '<td class="c-table__cell.*?>\K.*?(?=</td>)')
echo "$historic_table_header"
echo "$historic_table_header"> data.csv
columns=$(echo "$historic_table_header" | grep -o ";" | wc -l)
columns=$((columns+1))
for i in $historic_table_rows; do
    if [ "$row" = "" ]; then
        row="$i"
    else
        row="$row;$i"
    fi
    x=$((x+1))
    if [ $x -eq $columns ]; then
        echo "$row" >> data.csv
        row=""
        x=0
    fi
done
