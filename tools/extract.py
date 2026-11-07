#!/usr/bin/env python3
"""Extract every number shown on the site from source files into data/research.json.
Sources:  Nexus clone (H1, Paper 5 phase 1g-1i) read programmatically;
          Drive-verified constants (Phase 2b, Study 4) typed here with the file they come from
          and re-verified by hand on 2026-11-07 (see `verified` fields).
Run: python3 -I tools/extract.py /path/to/Nexus-.github.io
"""
import json, sys, pathlib

nx = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/repos/Nexus-.github.io")
out = pathlib.Path(__file__).resolve().parent.parent / "data" / "research.json"

def r3(x): return round(float(x), 3)

h1 = json.load(open(nx / "data/h1.json"))
conds = []
for c in h1["conditions"]:
    b, g = c["backfire"], c["gap"]
    conds.append({
        "dataset": c["dataset"], "model": c["model"],
        "backfire": r3(b["v"]), "ci": [r3(b["lo"]), r3(b["hi"])],
        "n_nondegenerate": b["n"], "n_problems": c["stats"]["n_problems"]["v"],
        "floor": r3(c["floor"]["v"]), "gap": r3(g["v"]), "gap_ci": [r3(g["lo"]), r3(g["hi"])],
        "cap_share": r3(c["stats"]["cap_share"]["v"]),
        "verdict": c["verdict_en"],
    })
pair_verdicts = sorted({p["verdict"] for p in h1["pairs"]})
n_pairs = len(h1["pairs"])
n_pairs_excl_zero = sum(1 for p in h1["pairs"] if p["stat"]["lo"] > 0 or p["stat"]["hi"] < 0)

def stat(o): return {"v": r3(o["v"]), "ci": [r3(o["ci"][0]), r3(o["ci"][1])]}
p1i = json.load(open(nx / "data_raw/analysis_phase1i.json"))["B"]
det, eps = p1i["run_confirm_det|d0|lf"], p1i["run_confirm_stochastic_eps0.1|d0|lf"]
p1h = json.load(open(nx / "data_raw/analysis_phase1h.json"))["B"]["run_multidepth_v2|d0|lf"]
p1g = json.load(open(nx / "data_raw/analysis_phase1g.json"))["B"]["run_multidepth_v2|d0|lf"]

data = {
 "generated_from": "Nexus-.github.io data/h1.json + data_raw/analysis_phase1{g,h,i}.json (read programmatically)",
 "h1": {
   "samples_per_problem": 16, "problems_per_condition": 120, "temperature": 0.7, "max_new_tokens": 1024,
   "models": ["Qwen2.5-1.5B-Instruct", "Qwen2.5-3B-Instruct"],
   "decision_rule": "refuted if the backfire 95% CI upper bound < 0.50; supported if the lower bound > 0.50; otherwise inconclusive",
   "conditions": conds,
   "pairs_total": n_pairs, "pairs_ci_excludes_zero": n_pairs_excl_zero, "pair_verdicts": pair_verdicts,
 },
 "paper5": {
   "phase1i": {
     "det_d0_lf": {"total": stat(det["total"]), "kscore": stat(det["kscore"]), "resk": stat(det["resk"]),
                   "n_episodes": det["n_ep"], "n_success": det["n_pos"], "n_runs": det["n_run"]},
     "eps01_d0_lf": {"total": stat(eps["total"]), "kscore": stat(eps["kscore"]), "resk": stat(eps["resk"]),
                     "n_episodes": eps["n_ep"], "n_success": eps["n_pos"], "n_runs": eps["n_run"]},
   },
   "phase1h_multidepth_d0_lf": {"total": stat(p1h["total"]), "kscore": stat(p1h["kscore"]), "resk": stat(p1h["resk"]),
                                "n_episodes": p1h["n_ep"], "n_runs": p1h["n_run"]},
   "phase1g_lxd_same_value_as_1h_total": {"v": r3(p1g["lxd"]["v"]), "ci": [r3(p1g["lxd"]["ci"][0]), r3(p1g["lxd"]["ci"][1])]},
   # Verified by hand against Drive originals report_phase2b.md / analysis_phase2b.json / stage_decision.json (2026-11-07)
   "phase2b": {
     "verified": "Drive: report_phase2b.md, analysis_phase2b.json, stage_decision.json (opened 2026-11-07)",
     "main": {"auroc": 0.548, "ci": [0.486, 0.605], "width": 0.120, "n": 3478, "n_success": 2639, "pairs": 8931, "strata": 116,
              "verdict": "not detected (precise)"},
     "aux_start_distance_only": {"auroc": 0.794, "ci": [0.756, 0.831], "pairs": 20157},
     "pooled_with_phase2": {"auroc": 0.544, "ci": [0.476, 0.598], "n": 4099},
     "seeds": 30, "stage2_run": False,
   },
   "phase1j": {"status": "pre-registered, not run (no result file)"},
 },
 "llm_internal": {
   "verified": "results/upstream-tests-2026-11-03.md in llm-internal-computing (read 2026-11-07)",
   "qwenpu": {"collected": 282, "passed": 246, "skipped": 22, "failed": 11, "not_run": 3},
   "qwenputer": {"collected": 562, "passed": 479, "skipped": 49, "failed": 11, "errors": 15, "incomplete": 8},
   "colab_update": {"test_rv_hf_passed": 6, "q35_inline": "113 of 113 passed", "q35_overlay": "3 of 6 passed, stopped by a 3000 s limit"},
   "upstream": [{"name": "qwenpu", "owner": "divagr18", "commit": "5af1fc0"}, {"name": "qwenputer", "owner": "divagr18", "commit": "bec1a0c"}],
 },
 "study4": {
   "verified": "Drive: 연구4_원본코드_확장_산출보고서.md (opened 2026-11-07)",
   "seeds": 3,
   "maze": {"steps3000": {"acc": 0.8468, "acc_sd": 0.0044, "headroom_pct": 25.7, "headroom_sd": 2.0},
            "steps12000": {"acc": 0.9745, "headroom_pct": 87.6}, "steps24000": {"acc": 1.0, "headroom_pct": 100.0},
            "ngram6": 0.7947, "probe3000": 0.286, "probe3000_untrained": 0.238, "untrained_share_pct": 83},
   "empty": {"steps3000": {"acc": 0.9922, "headroom_pct": 92.1}, "ngram6": 0.9014},
   "empty_more": {"steps12000": {"acc": 0.9994, "headroom_pct": 99.4}, "steps24000": {"acc": 0.9999, "headroom_pct": 99.9}},
   "probe": {"maze3000": {"full": 0.286, "full_sd": 0.006, "untrained": 0.238, "untrained_share_pct": 83,
                           "subset": 0.198, "subset_sd": 0.016, "subset_untrained": 0.114, "subset_ratio": 1.75, "mlp": 0.420, "mlp_sd": 0.031},
             "maze24000": {"full": 0.466, "untrained": 0.238, "untrained_share_pct": 51, "subset": 0.401, "subset_ratio": 3.52}},
   "j2": {"maze": {"gap3000": 0.085, "gap12000": 0.196, "diff": 0.111, "two_sd": 0.042},
          "empty": {"gap3000": 0.019, "gap12000": 0.028, "diff": 0.010, "two_sd": 0.013}},
   "causal_layers_positive_after_2sd": "none for maze; empty at 12000 and 24000 steps: layer L2 only",
 },
}
out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", out)
for c in conds: print(c["dataset"], c["model"], c["backfire"], c["ci"], c["n_nondegenerate"], "gap", c["gap"], c["gap_ci"], "cap", c["cap_share"])
print(pair_verdicts, n_pairs, n_pairs_excl_zero)
