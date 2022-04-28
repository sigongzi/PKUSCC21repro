for d in "C2" "C3"
do
    for a in "gs" "iamb" "inter.iamb"
    do
        ./test_single.sh 32 ${d} ${a} 0
    done
done
