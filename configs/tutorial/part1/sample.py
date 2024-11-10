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

# Configure CPU parameters according to the baseline configuration
system.cpu.fetchWidth = 2
system.cpu.decodeWidth = 2
system.cpu.issueWidth = 2
system.cpu.commitWidth = 2
system.cpu.numIQEntries = 64
system.cpu.numROBEntries = 192
system.cpu.LQEntries = 32
system.cpu.SQEntries = 32

# Set up the branch predictor as TAGE
system.cpu.branchPred = Tage()
system.cpu.branchPred.BTBEntries = 4096
system.cpu.branchPred.RASSize = 32

# Configure L1 instruction and data caches
system.cpu.icache = L1ICache(size='32kB', assoc=4, hit_latency=3, mshrs=32, tgts_per_mshr=8)
system.cpu.dcache = L1DCache(size='32kB', assoc=4, hit_latency=3, mshrs=32, tgts_per_mshr=8)

# Create the L2 (last-level cache, LLC) with an option to set LRU or LIP_i replacement policy
class CustomL2Cache(L2Cache):
    def __init__(self, replacement_policy="LRU", lip_i_position=None):
        super(CustomL2Cache, self).__init__()
        self.size = '256kB'
        self.assoc = 16
        self.hit_latency = 9
        self.mshrs = 32
        self.tgts_per_mshr = 8
        self.prefetcher = BOP()
        
        # Set replacement policy to either LRU or LIP_i based on input
        if replacement_policy == "LIP_i" and lip_i_position is not None:
            self.replacement_policy = LIP_iReplacementPolicy(position=lip_i_position)
        else:
            self.replacement_policy = LRUReplacementPolicy()

# Initialize L2 cache with LRU as the default policy
# Set 'lip_i_position' to your assigned value if testing LIP_i
lip_i_position = (sum_of_roll_numbers) % 15  # Replace with calculated value
system.l2cache = CustomL2Cache(replacement_policy="LIP_i", lip_i_position=lip_i_position)

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

# Set up the interrupt controller
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# Set the system port to connect to the memory bus
system.system_port = system.membus.cpu_side_ports

# Set up the workload: select one of the binaries from the list (e.g., 'astar')
binary = 'path_to_application_binary'  # Replace with the actual binary path for your workload
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

# Warm-up phase for 50M instructions
print("Starting warm-up phase (50M instructions)...")
m5.simulate(50_000_000)

# Detailed simulation phase for 50M instructions
print("Starting detailed simulation (50M instructions)...")
exit_event = m5.simulate(50_000_000)

# Output the reason for the simulation exit and the simulation tick at exit
print('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))
