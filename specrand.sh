#!/bin/bash
./build/X86/gem5.opt -d stats/specrand configs/deprecated/example/se.py \
--cpu-type=DerivO3CPU --sys-clock=3GHz \
--caches --l1i_size=32kB --l1d_size=32kB \
--l2cache --l2_size=256kB --l2-hwp-type=BOPPrefetcher \
--mem-size=4GB --mem-type=DDR3_1600_8x8 \
-F 100000 -s 200000 -W 50000000 -I 50000000 \
-c /home/kpvivek/ca_gem5/benchspec/CPU2006/999.specrand/exe/specrand_base.gcc43-64bit \
-o /home/kpvivek/ca_gem5/benchspec/CPU2006/999.specrand/data/ref/input/control
 