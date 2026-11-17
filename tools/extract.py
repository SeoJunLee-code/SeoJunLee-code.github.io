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

# ---------------------------------------------------------------- four newer research projects (read 2026-11-15)
CR = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "/home/user/repos2/AI-Creativity-Research")
if (CR / "results/exp1_ideas.json").exists():
    import statistics as _st, collections as _co
    def _means(rows, key):
        g = _co.defaultdict(lambda: [[], [], []])
        for x in rows:
            o = _st.mean(v[0] for v in x["scores"].values()); q = _st.mean(v[1] for v in x["scores"].values()); g[x[key]][0].append(o); g[x[key]][1].append(q)
            if "retention" in x: g[x[key]][2].append(_st.mean(x["retention"].values()))
        return {k: {"originality": round(_st.mean(v[0]), 2), "quality": round(_st.mean(v[1]), 2), "n": len(v[0]),
                    **({"retention": round(_st.mean(v[2]), 2)} if v[2] else {})} for k, v in g.items()}
    exp1 = _means(json.load(open(CR / "results/exp1_ideas.json", encoding="utf-8")), "cond")
    exp2 = _means(json.load(open(CR / "results/exp2_developed.json", encoding="utf-8"))["developed"], "arm")
else:
    exp1 = exp2 = None
data["creativity"] = {
  "source": "AI-Creativity-Research/REPORT.md (read 2026-11-15); exp1/exp2 means recomputed from results/exp1_ideas.json and results/exp2_developed.json (mean of two LLM judges)",
  "exp1_recomputed": exp1, "exp2_recomputed": exp2,
  "exp1_report_extra": {  # REPORT.md table: yield (originality>=6 and quality>=6, of 20) and embedding diversity
     "iid": {"yield": 1.31, "diversity": 0.078}, "list": {"yield": 1.62, "diversity": 0.177}, "cot": {"yield": 3.25, "diversity": 0.180},
     "deny": {"yield": 4.12, "diversity": 0.172}, "box": {"yield": 3.56, "diversity": 0.170}, "stim": {"yield": 3.25, "diversity": 0.173},
     "doxa": {"yield": 3.94, "diversity": 0.160}},
  "ideas": 2240, "tasks": 8, "conditions": 7, "per_cell": 320, "proposals_exp2": 72,
  "h5": {"quality_diff": 1.42, "originality_diff": -1.60, "retention_from": 5.00, "retention_to": 1.88},
  "h6": {"originality_diff": 0.33, "originality_p": 0.05, "quality_diff": -0.08, "anchor_quality_ge_refine": 4, "of": 24},
  "h2": {"vs_cot": 0.55, "vs_deny": -0.01, "vs_box": -0.67, "vs_stim": -0.48},
  "exploratory_top10": {"doxa_slots": 31.3, "uniform_slots": 11.4},
}
data["forgetting"] = {
  "source": "AI-Forgetting-Review-Research/output/data-analysis/study_a/REPORT.md (read 2026-11-15)",
  "rho": 0.2, "h1": {"learnedneed": 70.5, "lru": 51.0, "diff": 19.45, "ci": [16.60, 22.40], "min_pp": 3},
  "h1b_vs_random": {"LRU": [6.5, 4.8, 8.2], "LFU": [-14.8, -16.9, -12.8], "Ebbinghaus": [3.7, 1.8, 5.7], "ACT-R": [-2.8, -4.8, -0.8]},
  "learnedneed_minus": {"Random": [26.0, 23.4, 28.6], "FIFO": [19.8, 16.9, 22.5], "LRU": [19.5, 16.6, 22.4], "LFU": [40.8, 38.5, 43.1],
                        "Ebbinghaus": [22.3, 19.8, 25.0], "ACT-R": [28.8, 26.7, 31.2], "GA-proxy": [3.9, 2.5, 5.4]},
  "selfcheck_fail": {"random_seed_sd_pp": 3.31, "margin_pp": 3.0, "se_pp": 1.48}, "result_rows": 2600, "conversations": 10, "bootstrap": 10000,
}
data["algorithm"] = {
  "source": "Algorithm-Innovation-Research/output/results.md and output/report.md (read 2026-11-15)",
  "n": 3984588, "seeds": 10, "n_large": 31876710, "seeds_large": 3,
  "h1": [[8.42, 0.695], [10.53, 0.487], [12.63, 0.350], [14.74, 0.256], [16.84, 0.192], [21.05, 0.117]],
  "h1b": [{"target": "1e-2", "bbf": 9.92, "epf": 8.91, "saving": 1.01}, {"target": "1e-3", "bbf": 15.56, "epf": 12.82, "saving": 2.74},
          {"target": "1e-4", "bbf_gt": 21.05, "epf": 17.19, "saving_ge": 3.86}],
  "h4a": {"epf": 83.9, "bbf": 30.0, "ratio": 2.80, "limit": 3.0}, "h4b": {"epf": 0.958, "cuckoo": 1.924, "limit": 1.05},
  "h4c": {"epf": 486.8, "cuckoo": 198.0, "ratio": 2.46, "limit": 2.0},
  "wallclock_negative_query": {"vs_blocked_bloom": 3.14, "vs_cuckoo": 1.70, "vs_prefix_style": 1.81},
  "novelty_gain_bits_per_key": 0.2, "phase2_result_file_bytes": 0,
}
data["responsibility"] = {
  "source": "AI-Responsibility-Research README.md, input/bibliography/{audit-log,claim-check}*, output/reports/2026-11-13-phase1-final-report.md (read 2026-11-15)",
  "sources": {"total": 201, "A": 61, "B": 106, "C": 34}, "registry": {"verified": 160, "not_found": 27, "mismatch": 10, "not_checked": 4}, "bibtex_entries": 166,
  "claim_check": {"total": 65, "supported": 43, "partly": 18, "not_supported": 3, "unreachable": 1},
  "red_team": {"attacks": 49, "succeeded": 37, "tests_after": 62, "tests_passed_after": 58, "design_limits": 4},
  "behaviour": {"verified_charter": "6/8", "verified_other": "0/8"}, "human_decisions": 4,
}
data["updates"] = {
  "source": "unmerged claude/* branches of the 4 research repositories, read 2026-11-17",
  "forgetting_d": {"file": "output/data-analysis/study_d/REPORT.md", "h5": {"ours": 54.5, "base": "LRU", "base_v": 44.8, "diff": 9.7, "ci": [4.4, 14.0]},
                   "h5b": {"ours": 54.9, "base": "FIFO", "base_v": 49.7, "diff": 5.1, "ci": [2.0, 8.3]}, "h6": {"diff": 13.0, "ci": [9.5, 16.6]}},
  "creativity_human": {"file": "results/human_eval/human_summary.md", "raters": 1, "items": 72,
                       "a": {"n": 56, "orig": 0.16, "orig_p": 0.241, "qual": 0.30, "qual_p": 0.025},
                       "b": {"n": 16, "orig": 0.56, "orig_p": 0.025, "qual": 0.23, "qual_p": 0.388},
                       "pair": {"n": 8, "orig": 1.50, "orig_p": 0.172, "qual": -2.00, "qual_p": 0.031}},
  "algorithm_p2": {"file": "output/speed-report.md", "targets": 6, "met": 1, "neg_target": 1.25, "pos_target": 1.5, "mispred_target": 0.2,
                   "neg_ratio_before": [1.54, 1.69, 1.70], "neg_ratio_new": [1.81, 1.81, 1.78], "pos_ratio_before": [2.45, 2.56, 2.56], "pos_ratio_new": [3.59, 3.38, 3.40],
                   "mispred_before": 0.98, "mispred_new": 0.49, "hinted_neg_ns": [34, 21.6], "hinted_pos_ns": [46.6, 24.6]},
  "responsibility_p2": {"file": "input/ideas/lineage-consequence-contrast-plan.md", "status": "draft, awaiting freeze", "delta": 0.20, "holm_family": 5, "seeds": 13},
}
data["anc"] = {
  "source": "AGI- repo, branch claude/magical-heisenberg-2wt86e, anc_research/HANDOFF.md and README.md (read 2026-11-17)",
  "mimo_whole_run_db": 3.24, "mimo_ci": [2.39, 4.09], "mimo_steady_db": -0.28,
  "measured_plants": 16, "measured_broadband_db": -0.08, "measured_tonal_db": 0.73, "mu": 0.4, "diverged": "160/160",
  "synthetic_envs": 8, "synthetic_trials": 48, "synthetic_mean_db": 5.72, "tests": 74,
}
data["aptsx"] = {
  "source": "AGI- repo, branch claude/nice-ramanujan-yts94b, APTS_X_Runtime_Risk/APTS_X_Runtime_Risk_Research_Report.md (read 2026-11-17)",
  "sample_rows": 1000, "unique_job_ids": 549, "repeated_id_extra_rows": 451, "seeds": 8,
  "coverage_after_shift": {"fixed_2x": 49.87, "rolling_conformal_90": 88.79, "aci_90": 89.83},
  "resets_per_seed": 0.625, "seeds_no_reset": 3, "zero_delay_from": 61.8, "zero_delay_to": 76.5, "tests": 35,
}
out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", out)
for c in conds: print(c["dataset"], c["model"], c["backfire"], c["ci"], c["n_nondegenerate"], "gap", c["gap"], c["gap_ci"], "cap", c["cap_share"])
print(pair_verdicts, n_pairs, n_pairs_excl_zero)
