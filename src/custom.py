from celery.worker.autoscale import Autoscaler


class ResourceAutoscaler(Autoscaler):
    def _maybe_scale(self, req=None):
        procs = self.processes
        cur = min(self.qty, self.max_concurrency)
        if cur > procs:
            self.scale_up(cur - procs)
            return True
        cur = max(self.qty, self.min_concurrency)
        if cur < procs:
            self.scale_down(procs - cur)
            return True

    def maybe_scale(self, req=None):
        print("CHJ: maybe_scale")
        if self._maybe_scale(req):
            self.pool.maintain_pool()
