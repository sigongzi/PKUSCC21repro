dir=`pwd`
compiledir="${dir}/../../compile"
LD_LIBRARY_PATH="${compiledir}/boost-1.70.0/lib:${compiledir}/mvapich2/lib:${LD_LIBRARY_PATH}"
PATH="${compiledir}/mvapich2/bin:${compiledir}/ramBLe:${compiledir}/ramBLe/common/scripts:${PATH}"
datadir="${dir}/data"
scratchdir="${dir}/../output/scratch"
outputdir="${dir}/../output/weak"
echo "${compiledir}"
export MV2_IBA_HCA=mlx5_2
export MV2_USE_RoCE=1
export LD_LIBRARY_PATH
export PATH
export MV2_ENABLE_AFFINITY=1
ulimit -l unlimited


core_number=$1
dataset=$2
algorithm=$3
st=$4
n=$5
dataset_file="${datadir}/${dataset}_discretized.tsv"
prefix="${dataset}_${algorithm}_p${core_number}_weak"
output_file="${outputdir}/${prefix}.csv"
if [ -f ${dataset_file} ];then
    s=$st
    i=1

    while(( $i<$core_number))
    do
        s="${s}:`expr $st + $i`"
        i=`expr $i + 1`
    done
    echo $s
    ramble_weak_experiments.py --basedir ${compiledir}/ramBLe --scratch ${scratchdir} -g "-o ${scratchdir}/${prefix}.dot" --weak $n --mpi-arguments "-env MV2_CPU_MAPPING ${s}" -p ${core_number} -r 1 -a ${algorithm} -d ${dataset_file} -s $'\t' -c -v -i  --results ${output_file} > ${outputdir}/${prefix}.save 
else
    echo "${dataset_file} not found!"
fi
