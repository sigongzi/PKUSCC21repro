dir=`pwd`
compile_dir="${dir}/../../compile"
LD_LIBRARY_PATH="${compile_dir}/boost-1.70.0/lib:${compile_dir}/mvapich2/lib:${LD_LIBRARY_PATH}"
PATH="${compile_dir}/mvapich2/bin:${compile_dir}/ramBLe:${PATH}"

#echo "${compile_dir}"
export MV2_IBA_HCA=mlx5_2
export MV2_USE_RoCE=1
export LD_LIBRARY_PATH
export PATH
export MV2_ENABLE_AFFINITY=0
ulimit -l unlimited

ramble -h
