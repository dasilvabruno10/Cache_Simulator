# Bruno da Silva 
# EGRE 426 FALL 2023
# Lab 5 Test


# DEMO: python cache_test.py

######################################################################################################################

class DirectMappedCache:
    def __init__(self, cache_size):
        self.cache_size = cache_size
        self.cache = {}
        self.hits = 0
        self.misses = 0

    def access_memory(self, address):
        index = address % self.cache_size
        if index in self.cache and self.cache[index] == address:
            self.hits += 1
        else:
            self.misses += 1
            self.cache[index] = address

    def print_results(self):
        print("Direct Mapped Test")
        print("Hits:", self.hits)
        print("Misses:", self.misses)
        print("Contents in the cache at the end (address:content):")
        for index, content in self.cache.items():
            print(f"{index}:{content}")


class SetAssociativeCache:
    def __init__(self, num_sets, cache_size):
        self.num_sets = num_sets
        self.cache_size = cache_size
        self.cache = {i: {} for i in range(num_sets)}
        self.hits = 0
        self.misses = 0

    def access_memory(self, address):
        set_index = address % self.num_sets
        if address in self.cache[set_index]:
            self.hits += 1
        else:
            self.misses += 1
            if len(self.cache[set_index]) < self.cache_size:
                self.cache[set_index][address] = len(self.cache[set_index])
            else:
                # LRU replacement policy
                lru_key = min(self.cache[set_index], key=self.cache[set_index].get)
                del self.cache[set_index][lru_key]
                self.cache[set_index][address] = len(self.cache[set_index])

    def print_results(self):
        print("Two-Way Associative Test")
        print("Hits:", self.hits)
        print("Misses:", self.misses)
        print("Contents in the cache at the end (address:content):")
        for set_index, contents in self.cache.items():
            for address, content in contents.items():
                print(f"{address}:{content}")
            

# Example for direct-mapped cache
direct_mapped_cache = DirectMappedCache(16)
memory_accesses = [0, 3, 11, 16, 21, 11, 16, 48, 16]
for address in memory_accesses:
    direct_mapped_cache.access_memory(address)

direct_mapped_cache.print_results()

print("\n")

# Example for two-way set-associative cache
set_associative_cache = SetAssociativeCache(8, 2)
for address in memory_accesses:
    set_associative_cache.access_memory(address)

set_associative_cache.print_results()
