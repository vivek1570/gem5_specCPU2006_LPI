import m5
from m5.objects import *

# Create the system
system = System()

# Set up the clock domain and voltage domain
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '3GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Set the memory mode to timing and define the memory range
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('4GB')]

# Create an out-of-order CPU
system.cpu = X86O3CPU()

# Configure CPU parameters
system.cpu.fetchWidth = 2
system.cpu.decodeWidth = 2
system.cpu.issueWidth = 2
system.cpu.commitWidth = 2
system.cpu.numIQEntries = 64
system.cpu.numROBEntries = 192
system.cpu.LQEntries = 32
system.cpu.SQEntries = 32

# Set up the branch predictor
# system.cpu.branchPred = Tage()
# system.cpu.branchPred.BTBEntries = 4096
# system.cpu.branchPred.RASSize = 32

# Create L1 instruction and data caches
# system.cpu.icache = L1ICache(size='32kB', assoc=4, hit_latency=3, mshrs=32, tgts_per_mshr=8)
# system.cpu.dcache = L1DCache(size='32kB', assoc=4, hit_latency=3, mshrs=32, tgts_per_mshr=8)

# Create the L2 cache
system.l2cache = L2Cache(size='256kB', assoc=16, hit_latency=9, mshrs=32, tgts_per_mshr=8)

# Configure L1 caches and connect them to the CPU
system.cpu.icache_port = system.cpu.icache.cpu_side
system.cpu.dcache_port = system.cpu.dcache.cpu_side

# Connect the caches to the memory bus
system.l2bus = L2XBar()
system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports
system.l2cache.cpu_side = system.l2bus.mem_side_ports

# Attach the L2 cache to the memory bus
system.membus = SystemXBar()
system.l2cache.mem_side = system.membus.cpu_side_ports

# Create a memory controller, configure it, and connect it to the memory bus
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Add a Best Offset Prefetcher (BOP) to the L2 cache
system.l2cache.prefetcher = BOP()

# Set up the interrupt controller
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# Set the system port to connect to the memory bus
system.system_port = system.membus.cpu_side_ports

# Set up the workload: a "Hello world" binary in SE mode (or replace with your program)
binary = 'tests/test-progs/hello/bin/x86/linux/hello'
system.workload = SEWorkload.init_compatible(binary)

# Create a process for the program to run
process = Process()
process.cmd = [binary]

# Set the CPU's workload and create execution threads
system.cpu.workload = process
system.cpu.createThreads()

# Create the root of the simulation and instantiate the system
root = Root(full_system=False, system=system)
m5.instantiate()

# Begin the simulation
print("Beginning simulation!")
exit_event = m5.simulate()

# Output the reason for the simulation exit and the simulation tick at exit
print('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))
