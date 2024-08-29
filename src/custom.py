from celery.utils import instantiate
from celery.worker.autoscale import Autoscaler


class ResourceAutoscaler(Autoscaler):
    def __init__(self, *args, **kwargs):
        super(ResourceAutoscaler, self).__init__(*args, **kwargs)

        resource_limits_setting = self.worker.app.conf.get("resource_limits", [])
        resource_limits = []
        for r in resource_limits_setting:
            i_class, i_args, i_kwargs = (
                r.get("class"),
                r.get("args", []),
                r.get("kwargs", {}),
            )
            print(
                "Adding resource limit %s with args=%s and kwargs=%s"
                % (i_class, i_args, i_kwargs)
            )
            resource_limits.append(instantiate(i_class, *i_args, **i_kwargs))
        self.resource_limits = resource_limits

    def _maybe_scale(self, req=None):
        proc_count = self.processes
        task_count = self.qty

        print(
            "Autoscale: %s processes and %s reserved tasks" % (proc_count, task_count)
        )
        # min_concurrency and max_concurrency 값이 변경되는지 확인 필요
        print(
            f"min_concurrency: {self.min_concurrency}, max_concurrency: {self.max_concurrency}"
        )

        # Get (min, max) target ranges that proc_count should fit inside
        proc_ranges = [
            (
                task_count,
                task_count,
            ),  # ideally we have same number of processes as pending tasks
            (self.min_concurrency, self.max_concurrency),
        ] + [r.get_range(proc_count, req) for r in self.resource_limits]

        # Scale down to the lowest max value ...
        max_procs = min(
            max_procs for min_procs, max_procs in proc_ranges if max_procs is not None
        )
        max_procs = max(max_procs, 1)  # don't scale below 1
        if proc_count > max_procs:
            print("Requesting scale down by %s" % (proc_count - max_procs))
            self.scale_down(proc_count - max_procs)
            return True

        # ... or scale up to the highest min value
        min_procs = max(
            min_procs for min_procs, max_procs in proc_ranges if min_procs is not None
        )
        if proc_count < min_procs:
            print("CHJ: Requesting scale up by %s" % (min_procs - proc_count))
            self.scale_up(min_procs - proc_count)
            return True
