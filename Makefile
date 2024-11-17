# Variables for common configurations
GEM5_EXEC = ./build/X86/gem5.opt
SCRIPT = configs/deprecated/example/se.py
CPU_TYPE = DerivO3CPU
SYS_CLOCK = 3GHz
L1I_SIZE = 32kB
L1D_SIZE = 32kB
L2_SIZE = 256kB
L2_HWP_TYPE = BOPPrefetcher
MEM_SIZE = 4GB
MEM_TYPE = DDR3_1600_8x8

# Directories for outputs
ASTAR_STATS_DIR = stats/astar
MILC_STATS_DIR = stats/milc
SPECRAND_STATS_DIR=stats/specrand


# Commands for benchmarks
ASTAR_CMD = -c /home/kpvivek/ca_gem5/benchspec/CPU2006/473.astar/exe/astar_base.gcc43-64bit \
            -o /home/kpvivek/ca_gem5/benchspec/CPU2006/473.astar/data/ref/input/BigLakes2048.cfg

MILC_CMD = -c /home/kpvivek/ca_gem5/benchspec/CPU2006/433.milc/exe/milc_base.gcc43-64bit \
           -o /home/kpvivek/ca_gem5/benchspec/CPU2006/433.milc/data/ref/input/su3imp.in

SPECRAND_CMD = -c /home/kpvivek/ca_gem5/benchspec/CPU2006/999.specrand/exe/specrand_base.gcc43-64bit \
							 -o /home/kpvivek/ca_gem5/benchspec/CPU2006/999.specrand/data/ref/input/control

HMMER_CMD = -c /home/kpvivek/ca_gem5/benchspec/CPU2006/456.hmmer/exe/hmmer_base.gcc43-64bit \
						-o /home/kpvivek/ca_gem5/benchspec/CPU2006/456.hmmer/data/ref/input/nph3.hmm

BZIP_CMD = -c /home/kpvivek/ca_gem5/benchspec/CPU2006/401.bzip2/exe/bzip2_base.gcc43-64bit \
					 -o /home/kpvivek/ca_gem5/benchspec/CPU2006/401.bzip2/data/ref/input/input.source

LBM_CMD = -c /home/kpvivek/ca_gem5/benchspec/CPU2006/470.lbm/exe/lbm_base.gcc43-64bit \
					-o /home/kpvivek/ca_gem5/benchspec/CPU2006/470.lbm/data/ref/input/100_100_130_ldc.of


# Execution limits
ASTAR_LIMITS = -F 100000 -s 200000 -W 700000 -I 700000
MILC_LIMITS = -F 100000 -s 200000 -W 1000000 -I 1000000
SPECRAND_LIMITS= -F 100000 -s 200000 -W 50000000 -I 50000000
HMMER_LIMITS= -F 100000 -s 200000 -W 50000000 -I 50000000
BZIP_LIMITS=-F 100000 -s 200000 -W 50000000 -I 50000000
LBM_LIMITS=-F 100000 -s 200000 -W 50000000 -I 50000000

.PHONY: all astar milc clean

# Default target
all: astar milc

# Astar target
astar:
	$(GEM5_EXEC) -d $(ASTAR_STATS_DIR) $(SCRIPT) \
	--cpu-type=$(CPU_TYPE) --sys-clock=$(SYS_CLOCK) \
	--caches --l1i_size=$(L1I_SIZE) --l1d_size=$(L1D_SIZE) \
	--l2cache --l2_size=$(L2_SIZE) --l2-hwp-type=$(L2_HWP_TYPE) \
	--mem-size=$(MEM_SIZE) --mem-type=$(MEM_TYPE) \
	$(ASTAR_LIMITS) $(ASTAR_CMD)

# Milc target
milc:
	$(GEM5_EXEC) -d $(MILC_STATS_DIR) $(SCRIPT) \
	--cpu-type=$(CPU_TYPE) --sys-clock=$(SYS_CLOCK) \
	--caches --l1i_size=$(L1I_SIZE) --l1d_size=$(L1D_SIZE) \
	--l2cache --l2_size=$(L2_SIZE) --l2-hwp-type=$(L2_HWP_TYPE) \
	--mem-size=$(MEM_SIZE) --mem-type=$(MEM_TYPE) \
	$(MILC_LIMITS) $(MILC_CMD)

specrand:
	$(GEM5_EXEC) -d stats/specrand $(SCRIPT) \
	--cpu-type=$(CPU_TYPE) --sys-clock=$(SYS_CLOCK) \
	--caches --l1i_size=$(L1I_SIZE) --l1d_size=$(L1D_SIZE) \
	--l2cache --l2_size=$(L2_SIZE) --l2-hwp-type=$(L2_HWP_TYPE) \
	--mem-size=$(MEM_SIZE) --mem-type=$(MEM_TYPE) \
	$(SPECRAND_LIMITS) $(SPECRAND_CMD)

# Hmmer target
hmmer:
	$(GEM5_EXEC) -d stats/hmmer $(SCRIPT) \
	--cpu-type=$(CPU_TYPE) --sys-clock=$(SYS_CLOCK) \
	--caches --l1i_size=$(L1I_SIZE) --l1d_size=$(L1D_SIZE) \
	--l2cache --l2_size=$(L2_SIZE) --l2-hwp-type=$(L2_HWP_TYPE) \
	--mem-size=$(MEM_SIZE) --mem-type=$(MEM_TYPE) \
	$(HMMER_LIMITS) $(HMMER_CMD)

bzip:
	$(GEM5_EXEC) -d stats/bzip $(SCRIPT) \
	--cpu-type=$(CPU_TYPE) --sys-clock=$(SYS_CLOCK) \
	--caches --l1i_size=$(L1I_SIZE) --l1d_size=$(L1D_SIZE) \
	--l2cache --l2_size=$(L2_SIZE) --l2-hwp-type=$(L2_HWP_TYPE) \
	--mem-size=$(MEM_SIZE) --mem-type=$(MEM_TYPE) \
	$(BZIP_LIMITS) $(BZIP_CMD)
	
lbm:
	$(GEM5_EXEC) -d stats/lbm $(SCRIPT) \
	--cpu-type=$(CPU_TYPE) --sys-clock=$(SYS_CLOCK) \
	--caches --l1i_size=$(L1I_SIZE) --l1d_size=$(L1D_SIZE) \
	--l2cache --l2_size=$(L2_SIZE) --l2-hwp-type=$(L2_HWP_TYPE) \
	--mem-size=$(MEM_SIZE) --mem-type=$(MEM_TYPE) \
	$(LBM_LIMITS) $(LBM_CMD)

# Clean target
clean:
	rm -rf stats/astar stats/milc stats/specrand stats/hmmer stats/lbm stats/bzip

