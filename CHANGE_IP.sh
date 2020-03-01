ip_address=$0
gateway=$1
mask=$2

#
#
rm var
sudo grep -n -R "static ip_address=
    static routers=" ./dhcpcd.conf >> var

var2=$(sudo wc -l var)
echo $var2

IFS=' ' read -ra my_array <<< "$var2"

echo ${my_array[0]}

#Print the split string
for i in "${my_array[@]}"
do
    echo $i
done

flag_1=0
if [ ${my_array[0]} -ne 0 ]; then 

        input="var"
        while IFS= read -r line
        do
                echo $flag_1
                if [ $flag_1 -eq 0 ]; then 

                        IFS=':' read -ra my_array <<< "$line"
                        echo "${my_array[0]}d"
                        sudo sed "${my_array[0]}d" ./dhcpcd.conf > ./dhcpcd2.conf
                        flag_1=1
                else
                        IFS=':' read -ra my_array <<< "$line"
                        echo "${my_array[0]}d"
                        sudo sed "${my_array[0]}d" ./dhcpcd2.conf > ./dhcpcd.conf
                        flag_1=0
                fi
        done < "$input"

fi
