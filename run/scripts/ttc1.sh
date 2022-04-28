dir=`pwd`
compile_dir="${dir}/../../compile"
LD_LIBRARY_PATH="${compile_dir}/boost-1.70.0/lib:${compile_dir}/mvapich2/lib:${LD_LIBRARY_PATH}"
PATH="${compile_dir}/mvapich2/bin:${compile_dir}/ramBLe:${PATH}"
datadir="${dir}/data"
scratchdir="${dir}/../output/scratch"
outputdir="${dir}/../output"
#echo "${compile_dir}"
export MV2_IBA_HCA=mlx5_2
export MV2_USE_RoCE=1
export LD_LIBRARY_PATH
export PATH
export MV2_ENABLE_AFFINITY=0
ulimit -l unlimited

dataset=("C1","C2","C3")
algorithm=("gs","iamb","inter.iamb")
rambledir="${compile_dir}/ramBLe"
mpirun -h
mpirun -np 1 -env MV2_CPU_MAPPING 0 -env MV2_SHOW_CPU_BINDING 1 ramble -d -a gs -f ${rambledir}/test/coronary.csv -n 6 -m 1841 --warmup --hostnames -o coronary.dot 
