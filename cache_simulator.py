# Bruno da Silva 
# EGRE 426 FALL 2023
# Lab 5 


# DEMO: 
# python cache_simulator.py --block-size 256 --num-blocks 256 --associativity 1 --policy LRU --hit-time 1 --miss-time 1 --input-file addresses.txt

#####################################################################################################################################################

import argparse

# Class for Cache 
class Cache:
    def __init__(self, block_size, num_blocks, associativity, policy, hit_time, miss_time):
        self.block_size = block_size
        self.num_blocks = num_blocks
        self.associativity = associativity
        self.policy = policy
        self.hit_time = hit_time
        self.miss_time = miss_time
        self.cache = {}
        self.hits = 0
        self.misses = 0

    def access_memory(self, address):
        block_address = address // self.block_size

        # Word-level access
        set_index = block_address % (self.num_blocks // self.associativity)

        if set_index in self.cache:         # Check if the block is in the set
            
            if block_address in self.cache[set_index]:    # Hit
                
                self.hits += 1
                if self.policy == "LRU":
                    # Move the block to the most recently used position
                    self.cache[set_index].remove(block_address)
                    self.cache[set_index].append(block_address)
                return self.hit_time
            else:
                # Block not in set = miss
                self.misses += 1
        else:
            # Set not in cache = miss
            self.misses += 1
            self.cache[set_index] = []

        # Cache has free space or needs eviction
        if len(self.cache[set_index]) < self.associativity:
            # Add block to the set
            self.cache[set_index].append(block_address)
        else:
            # Eviction based on policy (LRU)
            if self.policy == "LRU":
                self.cache[set_index].pop(0)
                self.cache[set_index].append(block_address)

        # Return total access time (hit time + miss time)
        return self.hit_time + self.miss_time

    def print_results(self, num_reads):
        cache_size_bytes = self.num_blocks * self.block_size
        cache_size_bits = cache_size_bytes * 8  # Calculate bits as well as bytes

        print("Cache size: {} bytes ({} bits)".format(cache_size_bytes, cache_size_bits))
        print("Reads:", num_reads)
        print("Hits:", self.hits)
        print("Misses:", self.misses)
        print("Hit Rate: {:.2%}".format(self.hits / (self.hits + self.misses)))
        print("Miss Rate: {:.2%}".format(self.misses / (self.hits + self.misses)))
        print("Total Access Time: {} cycles".format(num_reads * self.hit_time + self.misses * self.miss_time))

def simulate_cache(block_size, num_blocks, associativity, policy, hit_time, miss_time, addresses):
    cache = Cache(block_size, num_blocks, associativity, policy, hit_time, miss_time)

    total_access_time = 0
    for address in addresses:
        total_access_time += cache.access_memory(address)

    cache.print_results(len(addresses))

def main():
    parser = argparse.ArgumentParser(description="Cache Simulator")
    parser.add_argument("--block-size", type=int, default=16, help="Block size in bytes")
    parser.add_argument("--num-blocks", type=int, default=16, help="Number of blocks in the cache")
    parser.add_argument("--associativity", type=int, default=1, help="Associativity of the cache")
    parser.add_argument("--policy", choices=["random", "LRU"], default="random", help="Replacement policy")
    parser.add_argument("--hit-time", type=int, default=1, help="Hit time in cycles")
    parser.add_argument("--miss-time", type=int, default=1, help="Miss time in cycles")
    parser.add_argument("--input-file", type=str, required=True, help="File containing memory addresses")

    args = parser.parse_args()

    with open(args.input_file, "r") as file:     # Read from input file 
        addresses = [int(line.strip(), 16) for line in file]

        # Command line options arguements
    simulate_cache(args.block_size, args.num_blocks, args.associativity, args.policy, args.hit_time, args.miss_time, addresses)

if __name__ == "__main__":
    main()
