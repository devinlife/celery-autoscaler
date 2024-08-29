import psutil


class MemoryLimit:
    def __init__(self, min_memory=0.0, max_memory=1.0):
        self.min_memory = min_memory
        self.max_memory = max_memory

    def get_range(self, proc_count, req):
        used_mem = self._get_used_mem()
        print(f"used_mem: {used_mem}")
        if used_mem > self.max_memory:
            print(
                "Memory limit: used memory %s exceeds maximum %s. Requesting scale down."
                % (used_mem, self.max_memory)
            )
            return (None, proc_count - 1)
        if used_mem < self.min_memory:
            print(
                "Memory limit: used memory %s below minimum %s. Requesting scale up."
                % (used_mem, self.min_memory)
            )
            return (proc_count + 1, None)
        print("Memory limit: None, None")
        return (None, None)

    def _get_used_mem(self):
        return psutil.virtual_memory().percent / 100
