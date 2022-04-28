for d in "C1" "C2" "C3"
do
    for a in "gs" "iamb" "inter.iamb"
    do
        ./test_multiple.sh 4 32 ${d} ${a} 0 ./hostfile4
    done
done
