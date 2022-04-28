for a in "gs" "iamb" "inter.iamb"
do
    ./test_weak_multiple.sh 2 32 C2 ${a} 0 20000 ./hostfile
done
