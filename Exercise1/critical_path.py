from collections import defaultdict, deque


class Activity:
    def __init__(self, id, duration, dependencies=None):
        self.id = id
        self.duration = duration
        self.dependencies = dependencies or []
        self.earliest_start = 0
        self.earliest_finish = 0
        self.latest_start = 0
        self.latest_finish = 0
        self.slack = 0


class CriticalPathAnalyzer:
    def __init__(self, activities):
        # Preserve insertion order for deterministic results
        self.activities = {a.id: a for a in activities}
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build adjacency list of successors."""
        graph = defaultdict(list)
        for act in self.activities.values():
            for dep in act.dependencies:
                graph[dep].append(act.id)
        return graph

    def _topological_sort(self):
        """Kahn's algorithm for topological ordering of activities."""
        indegree = {a: 0 for a in self.activities}
        for act in self.activities.values():
            for _ in act.dependencies:
                indegree[act.id] += 1

        queue = deque([a for a, deg in indegree.items() if deg == 0])
        topo_order = []

        while queue:
            node = queue.popleft()
            topo_order.append(node)
            for succ in self.graph[node]:
                indegree[succ] -= 1
                if indegree[succ] == 0:
                    queue.append(succ)
        return topo_order

    def compute_early_times(self):
        """Forward pass: compute ES and EF for all activities."""
        topo_order = self._topological_sort()
        for node in topo_order:
            act = self.activities[node]
            if act.dependencies:
                act.earliest_start = max(
                    self.activities[d].earliest_finish for d in act.dependencies
                )
            act.earliest_finish = act.earliest_start + act.duration

    def compute_late_times(self):
        """Backward pass: compute LS, LF and Slack for all activities."""
        topo_order = self._topological_sort()[::-1]
        # Project duration is max EF
        max_ef = max(self.activities[a].earliest_finish for a in self.activities)
        for node in topo_order:
            act = self.activities[node]
            if self.graph[node]:
                act.latest_finish = min(
                    self.activities[s].latest_start for s in self.graph[node]
                )
            else:
                act.latest_finish = max_ef
            act.latest_start = act.latest_finish - act.duration
            act.slack = act.latest_start - act.earliest_start

    def get_critical_path(self):
        """Return the list of activities with zero slack (critical activities).

        Note: This returns them in insertion/topological order which matches
        the single-path cases and keeps results deterministic.
        """
        self.compute_early_times()
        self.compute_late_times()
        return [a.id for a in self.activities.values() if a.slack == 0]

    def project_duration(self) -> int:
        """Return the total project duration (maximum earliest finish)."""
        # Ensure times are computed
        if all(a.earliest_finish == 0 for a in self.activities.values()):
            self.compute_early_times()
        return max(a.earliest_finish for a in self.activities.values())
