
if [ $1 == "-f" ]
then
    touch $2
    setfacl -R -m u:umangmal:rwx $2 
    setfacl -R -m u:keshavb:rwx $2 
    setfacl -R -m u:ayushk:rwx $2 
    setfacl -R -m u:snehal:rwx $2
    setfacl -R -m u:harsh:rwx $2 
fi

if [ $1 == "-d" ]
then
    mkdir $2
    setfacl -R -m u:umangmal:rwx $2 
    setfacl -R -m u:keshavb:rwx $2 
    setfacl -R -m u:ayushk:rwx $2 
    setfacl -R -m u:snehal:rwx $2
    setfacl -R -m u:harsh:rwx $2 
fi

