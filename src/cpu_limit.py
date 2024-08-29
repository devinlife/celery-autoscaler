import psutil as psutil


class CPULimit:
    def __init__(self, min_load=0.0, max_load=1.0):
        # cpu_percent returns usage since last call, so initialize here
        psutil.cpu_percent()

        self.min_load = min_load
        self.max_load = max_load
        print(f"CPU limit: min_load={min_load}, max_load={max_load}")

    def get_range(self, proc_count, req):
        cur_load = self._get_load()
        print(f"CPU limit: current load={cur_load}, proc_count={proc_count}")
        if cur_load > self.max_load:
            print(
                "CPU limit: load average %s exceeds maximum %s. Requesting scale down."
                % (cur_load, self.max_load)
            )
            return (None, proc_count - 1)
        if cur_load < self.min_load:
            print(
                "CPU limit: load average %s below minimum %s. Requesting scale up."
                % (cur_load, self.min_load)
            )
            return (proc_count + 1, None)
        return (None, None)

    def _get_load(self):
        return psutil.cpu_percent() / 100
