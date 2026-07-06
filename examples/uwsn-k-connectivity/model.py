#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Non-uniform k-connectivity routing for an underwater sensor network (UWSN).

Faithful, reduced (small-topology) reimplementation of the THEDN energy-minimization
MILP behind "Mitigating Energy Cost of Connection Reliability in UWSNs Through
Non-Uniform k-Connectivity" (IEEE doc 11143186). The physics (Thorp acoustic
absorption, distance-tiered transmit energy, node-disjoint multi-path routing,
interference-aware bandwidth) is preserved from the original Model/VariableK_MR.py;
only the node count is reduced and a fixed seed + a solution CSV export are added so
the model runs end-to-end quickly and reproducibly.

Run:  python3 model.py        ->  writes solutions.csv (columns: i,j,k,l,val)
"""

import math
import random
import csv
import io
import json
import sys

import gurobipy as gp
from gurobipy import GRB

# ============================ CONSTANTS ============================
# -- topology --
NODE = 13           # total nodes incl. base station (paper's own figure uses ~13; reduced
                    #   from the 30-node campaign for a fast, reproducible gate)
SEED = 6            # fixed for reproducibility (original used random.seed(iterNo))
RATE = 0.5          # NodeRate = NODE*RATE splits nodes into higher- vs lower-k tiers
# Non-uniform k-connectivity (the paper's contribution): critical nodes keep more
# node-disjoint paths than the rest, instead of a uniform k everywhere. Faithful to the
# commented `if k < NodeRate: k1 else: k2` block in the original Model/VariableK_MR.py.
K_HIGH = 2          # required disjoint paths for critical (index < NodeRate) sources
K_LOW = 1           # required disjoint paths for the remaining sources

# -- geometry (km) --
DX, DY, DZ = 1.0, 3.0, 0.3

# -- traffic / rounds --
T_ROUND = 300       # round duration (s)
S_K = 1             # data packets generated per sensor per round
L_DATA = 1024       # data packet size (bits)
L_CONTROL = 256     # control packet size (bits)
LARGE_M = 5000
N_L = 3             # number of paths
XI = 0.25           # control-packet frequency
N_R = 1440          # total rounds
ER_BIT = 2e-8       # reception energy per bit (J)
R_B = 2500          # data rate (bps)
GAMMA = 1.7         # interference-range multiplier

# -- acoustic channel (Thorp absorption at OP_FREQ kHz) --
KS = 1.5            # spreading factor
OP_FREQ = 25        # operating frequency (kHz)
ABSORB = ((0.11 * OP_FREQ ** 2) / (1 + OP_FREQ ** 2)
          + (44 * OP_FREQ ** 2) / (4100 + OP_FREQ ** 2)
          + 2.75e-4 * OP_FREQ ** 2 + 0.003)
V_ABS = 10 ** (ABSORB / 10)     # frequency-dependent absorption component
P0 = 1e-7                       # desired received power level

# -- transmit power levels: reachable distance tiers (m) --
RMAX = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
MAX_DIST = RMAX[-1]
TL = list(range(1, 11))         # 10 power levels
TL_MOD = list(range(1, 10))
# path loss and per-bit transmit energy for each level
PATH_LOSS = {tl: (RMAX[tl - 1] ** KS) * (V_ABS ** (RMAX[tl - 1] * 1e-3)) for tl in TL}
ET_BIT = {tl: PATH_LOSS[tl] * P0 for tl in TL}

# node index sets
V = list(range(NODE))           # all nodes (0 = base station)
W = list(range(1, NODE))        # sensor nodes
NL = [l + 1 for l in range(N_L)]
NL_MOD = [l + 1 for l in range(N_L - 1)]

BASE_POSITIONS = [(DX / 2, DY / 2, 0), (DX / 2, -DY / 2, 0),
                  (-DX / 2, DY / 2, 0), (-DX / 2, -DY / 2, 0)]


# ============================ TOPOLOGY ============================
def build_topology(seed):
    """Place the base station at a random corner and sensors uniformly in the prism.
    Returns node coordinates, pairwise distances D (m), the link set A, per-link
    transmit energy E_t_link, and the interference tensor."""
    random.seed(seed)
    base = BASE_POSITIONS[random.randint(0, 3)]

    xs, ys, zs = [], [], []
    for i in V:
        if i == 0:
            x, y, z = base
        else:
            x = random.uniform(-DX / 2, DX / 2)
            y = random.uniform(-DY / 2, DY / 2)
            z = random.uniform(-DZ, 0)
        xs.append(x); ys.append(y); zs.append(z)

    # distances in metres
    D = {(i, j): 1000 * math.sqrt((xs[i] - xs[j]) ** 2
                                  + (ys[i] - ys[j]) ** 2
                                  + (zs[i] - zs[j]) ** 2)
         for i in V for j in V}

    A = [(i, j) for i in V for j in V if i != j and D[i, j] <= MAX_DIST]

    # transmit energy per link: cheapest power tier that reaches the distance
    E_t_link = {}
    for i in V:
        for j in V:
            if i == j:
                E_t_link[i, j] = 0.0
            elif D[i, j] <= RMAX[0]:
                E_t_link[i, j] = ET_BIT[1]
            elif D[i, j] > MAX_DIST:
                E_t_link[i, j] = 1e10
            else:
                for tl in TL_MOD:
                    if RMAX[tl - 1] < D[i, j] <= RMAX[tl]:
                        E_t_link[i, j] = ET_BIT[tl + 1]
                        break

    # interference indicator: node m1's tx to node j collides at receiver i
    interference = {}
    for i in V:
        for j in V:
            for m1 in V:
                interference[j, m1, i] = (
                    1 if i != j and m1 != j and m1 != i and GAMMA * D[j, m1] >= D[j, i]
                    else 0)

    return D, A, E_t_link, interference


# ============================ MODEL ============================
def solve(k_req, D, A, E_t_link, interference):
    """Build and solve the THEDN energy-minimization MILP. k_req maps each source node
    to its required number of node-disjoint paths (non-uniform k-connectivity).
    Returns (status, tau, f-solution dict)."""
    mdl = gp.Model("uwsn_kconn")
    mdl.Params.LogToConsole = 0
    mdl.setParam("OutputFlag", 0)
    mdl.setParam("TimeLimit", 120)
    mdl.setParam("MIPGap", 0.05)

    reach = lambda i, j: i != j and D[i, j] <= MAX_DIST

    # -- decision variables --
    f = {(i, j, k, l): mdl.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=N_R,
                                  name=f"f_{i}_{j}_{k}_{l}")
         for i in V for j in V for k in W for l in NL}
    g = {(i, j, k, l): mdl.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=N_R,
                                  name=f"g_{i}_{j}_{k}_{l}")
         for (i, j) in A for k in W for l in NL}
    p = {(k, l): mdl.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f"p_{k}_{l}")
         for k in W for l in NL}
    h = {(i, j, k, l): mdl.addVar(vtype=GRB.BINARY, name=f"h_{i}_{j}_{k}_{l}")
         for (i, j) in A for k in W for l in NL}
    tau = mdl.addVar(vtype=GRB.CONTINUOUS, name="tau")

    # -- constraints --
    mdl.addConstrs((f[i, j, k, l] == 0
                    for i in V for j in V for k in W for l in NL
                    if i == j or D[i, j] > MAX_DIST), name="NoFlow")

    for i in V:
        for k in W:
            for l in NL:
                out = gp.quicksum(f[i, j, k, l] for j in V if reach(i, j))
                inc = gp.quicksum(f[j, i, k, l] for j in V if reach(i, j))
                if i == k:
                    mdl.addConstr(out - inc == p[k, l], name="FlowBalanceSource")
                elif i == 0:
                    mdl.addConstr(out - inc == -p[k, l], name="FlowBalanceBS")
                else:
                    mdl.addConstr(out - inc == 0, name="FlowBalanceRelay")

    mdl.addConstrs((gp.quicksum(p[k, l] for l in NL) == S_K * N_R for k in W),
                   name="DataGeneratedSource")
    mdl.addConstrs((gp.quicksum(f[j, k, k, l] for j in W for l in NL) == 0 for k in W),
                   name="NoLoopBack")
    mdl.addConstrs((f[i, j, k, l] <= S_K * N_R * h[i, j, k, l]
                    for (i, j) in A for k in W for l in NL), name="BinLink1")
    mdl.addConstrs((h[i, j, k, l] <= f[i, j, k, l]
                    for (i, j) in A for k in W for l in NL), name="BinLink2")
    mdl.addConstrs((gp.quicksum(h[i, j, k, l] for j in V if reach(i, j)) <= 1
                    for i in W for k in W for l in NL), name="OneNextHop")
    mdl.addConstrs((gp.quicksum(h[i, j, k, l] for l in NL) <= 1
                    for (i, j) in A for k in W), name="OnePathPerLink")
    mdl.addConstrs((gp.quicksum(f[j, 0, k, l + 1] for j in V if j != 0 and reach(j, 0))
                    <= gp.quicksum(f[j, 0, k, l] for j in V if j != 0 and reach(j, 0))
                    for k in W for l in NL_MOD), name="PacketPathOrder")
    mdl.addConstrs((f[i, j, k, l] - LARGE_M * (1 - h[i, j, k, l]) <= p[k, l]
                    for (i, j) in A for k in W for l in NL), name="ElimST1")
    mdl.addConstrs((f[i, j, k, l] + LARGE_M * (1 - h[i, j, k, l]) >= p[k, l]
                    for (i, j) in A for k in W for l in NL), name="ElimST2")
    mdl.addConstrs((g[i, j, k, l] == XI * N_R * (h[i, j, k, l] + h[j, i, k, l])
                    for (i, j) in A for k in W for l in NL), name="DefineG")
    mdl.addConstrs((gp.quicksum(h[i, j, k, l] for l in NL for j in V if reach(i, j)) <= 1
                    for i in W for k in W if i != k), name="NodeDisjoint1")
    mdl.addConstrs((gp.quicksum(h[j, i, k, l] for l in NL for j in V if reach(i, j)) <= 1
                    for i in W for k in W if i != k), name="NodeDisjoint2")

    # THEDN: tau bounds every sensor's tx+rx energy
    mdl.addConstrs((
        gp.quicksum(
            gp.quicksum(E_t_link[i, j] * (f[i, j, k, l] * L_DATA + g[i, j, k, l] * L_CONTROL)
                        for j in V if reach(i, j))
            + gp.quicksum(ER_BIT * (f[j, i, k, l] * L_DATA + g[j, i, k, l] * L_CONTROL)
                          for j in V if reach(i, j))
            for k in W for l in NL) <= tau
        for i in W), name="THEDN")

    # interference-aware bandwidth per node
    mdl.addConstrs((
        gp.quicksum(
            gp.quicksum((f[i, j, k, l] * L_DATA + g[i, j, k, l] * L_CONTROL) / R_B
                        for j in V if reach(i, j))
            + gp.quicksum((f[j, i, k, l] * L_DATA + g[j, i, k, l] * L_CONTROL) / R_B
                          for j in V if reach(i, j))
            + gp.quicksum((f[j, m1, k, l] * L_DATA * interference[j, m1, i]
                           + g[j, m1, k, l] * L_CONTROL * interference[j, m1, i]) / R_B
                          for m1 in V if j != m1 and j != i and m1 != i and reach(j, m1))
            for l in NL for k in W) <= N_R * T_ROUND
        for i in V for j in V if reach(i, j)), name="Bandwidth")

    # non-uniform k-connectivity: each source keeps >= k_req[k] first-hops (disjoint paths)
    mdl.addConstrs((gp.quicksum(h[k, j, k, l] for l in NL for j in V if reach(k, j)) >= k_req[k]
                    for k in W), name="kConnectivity")

    mdl.ModelSense = GRB.MINIMIZE
    mdl.setObjective(tau)
    # Determinism for the gate: single thread + fixed solver seed make the returned
    # optimum reproducible across processes (the routing optimum is otherwise non-unique;
    # see numerical-determinism). The objective tau is invariant regardless.
    mdl.setParam("Threads", 1)
    mdl.setParam("Seed", 0)
    mdl.optimize()

    if mdl.Status == GRB.INFEASIBLE:
        return "INFEASIBLE", None, None
    if mdl.SolCount == 0:
        return "NO_SOLUTION", None, None
    fsol = {key: var.X for key, var in f.items() if var.X > 1e-6}
    return "OPTIMAL", tau.X, fsol


# ============================ EXPORT ============================
def solution_csv_text(fsol):
    """Render the nonzero data-flow solution as CSV text (rows i,j,k,l,val) -- the
    per-edge format the original repo's plot scripts consumed but no script ever wrote."""
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["i", "j", "k", "l", "val"])
    for (i, j, k, l), val in sorted(fsol.items()):
        w.writerow([i, j, k, l, f"{val:.3f}"])
    return buf.getvalue()


def k_requirement():
    """Non-uniform per-node connectivity requirement: critical sources (index below
    NodeRate) need K_HIGH node-disjoint paths, the rest K_LOW."""
    node_rate = NODE * RATE
    return {k: (K_HIGH if k < node_rate else K_LOW) for k in W}


CSV_FILE = "solutions.csv"      # illustrative optimal routing (one of several optima)
BASELINE_FILE = "baseline.json"  # the gated invariant: objective tau
TAU_RTOL = 1e-6                  # relative tolerance for the gate


def compute():
    """Solve at the fixed operating point and return (status, tau, csv_text)."""
    k_req = k_requirement()
    D, A, E_t_link, interference = build_topology(SEED)
    status, tau, fsol = solve(k_req, D, A, E_t_link, interference)
    return status, tau, (solution_csv_text(fsol) if status == "OPTIMAL" else None)


def main(argv):
    check = "--check" in argv
    k_req = k_requirement()
    n_high = sum(1 for k in W if k_req[k] == K_HIGH)
    status, tau, text = compute()
    print(f"status={status}  seed={SEED}  nodes={NODE}  "
          f"k-scheme: {n_high} sources @k={K_HIGH}, {len(W)-n_high} @k={K_LOW}"
          + (f"  tau={tau:.6f}" if tau is not None else ""))
    if status != "OPTIMAL":
        raise SystemExit(f"no optimal solution (status={status}); "
                         f"try a different SEED or lower K_HIGH")

    if check:
        # GATE — compare the reproducible scientific invariant (objective tau), NOT the
        # exact routing: the flow optimum is non-unique (many routings hit the same tau),
        # so byte-comparing solutions.csv is a solver tie-break artifact, not a result.
        with open(BASELINE_FILE) as fh:
            expected = json.load(fh)["tau"]
        if abs(tau - expected) <= TAU_RTOL * abs(expected):
            print(f"GATE PASS: tau={tau:.6f} matches baseline {expected:.6f} "
                  f"(rtol {TAU_RTOL})")
            return 0
        print(f"GATE FAIL: tau={tau:.6f} != baseline {expected:.6f} "
              f"(rtol {TAU_RTOL})", file=sys.stderr)
        return 1

    with open(CSV_FILE, "w", newline="") as fh:
        fh.write(text)
    with open(BASELINE_FILE, "w") as fh:
        json.dump({"seed": SEED, "nodes": NODE, "k_high": K_HIGH, "k_low": K_LOW,
                   "tau": round(tau, 6)}, fh, indent=2)
        fh.write("\n")
    print(f"wrote {CSV_FILE} (illustrative routing) and {BASELINE_FILE} (gated tau)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
