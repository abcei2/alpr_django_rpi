#!/bin/bash
ip_address=$1
gateway=$2
mask=$3

file="/home/santi/ECUADOR/LPR/rpi/alpr_django_rpi/dhcpcd.conf"
#
#
rm var
sudo grep -n -R "interface eth0" $file >> var

var2=$(sudo wc -l var)
echo $var2

IFS=' ' read -ra my_array <<< "$var2"

echo ${my_array[0]}

#Print the split string
for i in "${my_array[@]}"
do
    echo $i
done

number_1=1
flag_1=0
line_to_drop=-1
counter_lines=0

if [ ${my_array[0]} -ne 0 ]; then 

    input="var"
    while IFS= read -r line;
    do
        IFS=':' read -ra my_array <<< "$line"

        line_to_drop=${my_array[0]} 
        echo $line_to_drop
    done < "$input"
    
    while [ $counter_lines  -lt 4 ];do
        var1=${line_to_drop}d
        sed -e $var1 $file > ./dhcp.back
        sudo mv ./dhcp.back $file
        let counter_lines=counter_lines+1
    done 

    echo "interface eth0" >> $file
    echo "static ip_address=$ip_address/$mask" >> $file
    echo "static routers=$gateway" >> $file
    echo "static domain_name_servers= $gateway 8.8.8.8 8.8.0.0 fd51:42f8:caae:d92e::1" >> $file

fi
