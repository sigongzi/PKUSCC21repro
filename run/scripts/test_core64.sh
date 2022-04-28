for d in "C1"
do
    for a in "gs" "iamb" "inter.iamb"
    do
        ./test_multiple.sh 2 32 ${d} ${a} 0 ./hostfile
    done
done
