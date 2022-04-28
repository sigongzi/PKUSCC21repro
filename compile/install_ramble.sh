#!/bin/bash -x
boost_link="https://boostorg.jfrog.io/artifactory/main/release/1.70.0/source/boost_1_70_0.tar.bz2"

mvapich2_link="https://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.3.3.tar.gz"

ramBLe_link="https://github.com/asrivast28/ramBLe.git"

dir=`pwd`

function build_boost() {
    cd ${dir} 
    if [ -d "./boost-1.70.0" ]; then
        return
    fi
    if [ ! -f "./boost_1_70_0.tar.bz2" ]; then
        wget "${boost_link}"
    fi
    tar -xf ./boost_1_70_0.tar.bz2
    cd boost_1_70_0
    pwd
    ./bootstrap.sh
    ./b2
    echo "${dir}/boost-1.70.0"
    ./b2 install --prefix="${dir}/boost-1.70.0" 
    rm -rf ./boost_1_70_0
}

function build_mvapich2() {
    cd ${dir}
    if [ -d "./mvapich2" ]; then
        return
    fi
    if [ ! -f "./mvapich2-2.3.3.tar.gz" ]; then
        wget "${mvapich2_link}" --no-check-certificate
    fi
    tar -xvf ./mvapich2-2.3.3.tar.gz
    cd mvapich2-2.3.3
    pwd
    ./configure --prefix="${dir}/mvapich2"
    make -j4
    make install
    rm -rf "./mvapich2-2.3.3"
}

function build_ramBLe() {
    cd ${dir}
    if [ -d "./ramBLe" ]; then
        rm -rf "./ramBLe"
    fi
    git clone --recurse-submodules "${ramBLe_link}"
    export PATH="${dir}/mvapich2/bin:$PATH"
    cd ramBLe
    scons TIMER=1 TEST=0 LOCALLIBS="${dir}/mvapich2/lib ${dir}/boost-1.70.0/lib" LOCALINCLUDES="${dir}/mvapich2/include ${dir}/boost-1.70.0/include"
}

build_boost
build_mvapich2
build_ramBLe

