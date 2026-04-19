# --- KEEP YOUR IMPORTS ---
from world import World
from coordination import Coordinator
from pathfinding import astar
from visualization import Visualizer
import random
import time

# GLOBAL CONTROL
control_mode = "FAST"


EPI_COUNT = 3
MAX_STEPS = 200

vis = None

def move_obstacles(w):
    new_obs = set()
    protected = set()

    protected.add(w.target_position)

    for t in w.tasks:
        protected.add(t.start)
        protected.add(t.end)
        if hasattr(t, "current_location"):
            protected.add(t.current_location)

    for pos in w.agent_positions.values():
        protected.add(pos)

    for (x, y) in w.obstacles:
        dx, dy = random.choice([(0,0),(1,0),(-1,0),(0,1),(0,-1)])
        nx, ny = x + dx, y + dy

        if (
            0 <= nx < w.grid_size and
            0 <= ny < w.grid_size and
            (nx, ny) not in protected
        ):
            new_obs.add((nx, ny))
        else:
            new_obs.add((x, y))

    w.obstacles = list(new_obs)


def get_dynamic_obstacles(w, current_aid):
    obs = set(w.obstacles)
    for aid, pos in w.agent_positions.items():
        if aid != current_aid:
            obs.add(pos)
    return obs


for episode in range(EPI_COUNT):

    w = World()

    if vis is None:
        vis = Visualizer(w)
    else:
        vis.world = w

    coord = Coordinator(w)
    coord.assign_initial_tasks()

    w.last_positions = {}

    for aid in w.agent_positions:
        if aid not in w.agent_roles:
            w.agent_roles[aid] = "IDLE"

    metrics = {
        "steps": 0,
        "waits": 0,
        "collisions": 0,
        "task_completed": False,
        "completion_pct": 0
    }

    print(f"\n===== EPISODE {episode+1} =====")

    for step in range(MAX_STEPS):

        move_obstacles(w)

        #  READ CONTROL FROM FILE (ADDED)
        try:
            with open("control.txt", "r") as f:
                control_mode = f.read().strip()
        except:
            control_mode = "FAST"

        if step == 10:
            print("SIMULATED FAILURE: Agent 1 slowed")
            w.agent_roles[1] = "RECOVERING"

        for aid in w.agent_roles:
            if w.agent_roles[aid] == "RECOVERING":
                if step > 10 and (step - 10) % 6 == 0:
                    print(f"RECOVER: Agent {aid}")
                    w.agent_roles[aid] = "IDLE"

        if all(t.completed for t in w.tasks):
            print("MISSION COMPLETE")

            for aid in w.agent_roles:
                if w.agent_roles[aid] != "RECOVERING":
                    w.agent_roles[aid] = "DONE"

            metrics["completion_pct"] = 100

            vis.animate_high_fidelity(
                w,
                w.agent_positions,
                w.agent_positions,
                {},
                metrics,
                metrics["completion_pct"]
            )

            time.sleep(2)
            metrics["task_completed"] = True
            break

        metrics["steps"] += 1

        old_positions = dict(w.agent_positions)
        intended = {}
        paths = {}

        for aid in w.get_active_agents():

            curr = w.agent_positions[aid]
            task = coord.get_agent_current_task(aid)

            if not task:
                remaining = [t for t in w.tasks if not t.completed]

                if remaining:
                    def dist(t):
                        return abs(curr[0] - t.start[0]) + abs(curr[1] - t.start[1])

                    new_task = min(remaining, key=dist)
                    coord.agent_task_map[aid] = [new_task]
                    w.agent_roles[aid] = new_task.name
                    task = new_task
                else:
                    intended[aid] = curr
                    continue

            goal = task.start if not task.picked else task.end

            dyn_obs = get_dynamic_obstacles(w, aid)
            if goal in dyn_obs:
                dyn_obs.remove(goal)

            path = astar(curr, goal, w.grid_size, dyn_obs)

            if len(path) <= 1:
                neighbors = [
                    (curr[0]+1, curr[1]),
                    (curr[0]-1, curr[1]),
                    (curr[0], curr[1]+1),
                    (curr[0], curr[1]-1)
                ]

                valid_moves = [
                    (nx, ny) for nx, ny in neighbors
                    if 0 <= nx < w.grid_size and
                       0 <= ny < w.grid_size and
                       (nx, ny) not in dyn_obs
                ]

                next_pos = random.choice(valid_moves) if valid_moves else curr
            else:
                next_pos = path[1]

            #  FINAL OVERRIDE (UNCHANGED LOGIC)
            if control_mode == "SLOW":
                next_pos = curr

            if next_pos == curr:
                metrics["waits"] += 1

            intended[aid] = next_pos
            paths[aid] = path

        safe, collisions = coord.resolve_collisions(intended)
        metrics["collisions"] += collisions

        for aid, pos in safe.items():
            task = coord.get_agent_current_task(aid)

            if not task:
                continue

            if pos == task.start and not task.picked:
                task.picked = True

            if pos == task.end and task.picked:
                task.completed = True
                coord.agent_task_map[aid] = []

        w.update_positions(safe)

        total = len(w.tasks)
        done = sum(1 for t in w.tasks if t.completed)
        metrics["completion_pct"] = int((done / total) * 100)

        with open("agent_positions.txt", "w") as f:
            f.write(str(w.agent_positions))

        vis.animate_high_fidelity(
            w,
            old_positions,
            w.agent_positions,
            paths,
            metrics,
            metrics["completion_pct"]
        )

        time.sleep(0.05)

print("\n===== DONE =====")

while True:
    vis.update()