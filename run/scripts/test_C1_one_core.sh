dir=`pwd`
compile_dir="${dir}/../../compile"
LD_LIBRARY_PATH="${compile_dir}/boost-1.70.0/lib:${compile_dir}/mvapich2/lib:${LD_LIBRARY_PATH}"
PATH="${compile_dir}/mvapich2/bin:${PATH}"

#echo "${compile_dir}"
export MV2_IBA_HCA=mlx5_2
export MV2_USE_RoCE=1
export LD_LIBRARY_PATH
export PATH
export MV2_ENABLE_AFFINITY=0
ulimit -l unlimited
${compile_dir}/ramBLe/common/scripts/ramble_experiments.py --basedir "${compile_dir}/ramBLe" --scratch "${dir}/../output/scratch" -p 1 -r 1 -a gs -d "${dir}/data/C1_discretized.tsv" -s $'\t' -c -v -i  --results "${dir}/../output/C1_gs_p1_strong_tmp.csv"
#${compile_dir}/ramBLe/common/scripts/ramble_experiments.py --basedir "${compile_dir}/ramBLe" --scratch "${dir}/../output/scratch" -p 1 -r 1 -a iamb -d "${dir}/data/C1_discretized.tsv" -s $'\t' -c -v -i --hostfile "${dir}/hostfile" --results "${dir}/../output/C1_iamb_p1_strong.csv" > "${dir}/../output/iamb.log" &
#${compile_dir}/ramBLe/common/scripts/ramble_experiments.py --basedir "${compile_dir}/ramBLe" --scratch "${dir}/../output/scratch" -p 1 -r 1 -a inter.iamb -d "${dir}/data/C1_discretized.tsv" -s $'\t' -c -v -i --hostfile "${dir}/hostfile" --results "${dir}/../output/C1_inter.iamb_p1_strong.csv" > "${dir}/../output/inter-iamb.log" &

