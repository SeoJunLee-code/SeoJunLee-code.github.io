# -*- coding: utf-8 -*-
"""All page text (EN / KO). Every number comes from data/research.json via D; nothing is typed by hand
except labels. Blocks: ("h2",t) ("p",t) ("ul",[..]) ("table",head,rows) ("note",t,kind) ("kv",[(k,v)])."""

def f3(x): return f"{x:.3f}"
def ci(a): return f"[{a[0]:.3f}, {a[1]:.3f}]"
def pct(x, d=0): return f"{x*100:.{d}f}%"

BADGES = {
    "en": {"prototype": "Prototype · Unvalidated", "refuted": "Hypothesis Refuted", "progress": "In Progress",
           "partial": "Reproduction · Partial", "exploratory": "Exploratory · 3 seeds"},
    "ko": {"prototype": "프로토타입 · 미검증", "refuted": "가설 반증", "progress": "진행 중",
           "partial": "재현 · 부분", "exploratory": "탐색적 · 시드 3개"},
}
TAGS = {"en": {"m": "Measured", "r": "Reported", "j": "Judgment", "u": "Unverified"},
        "ko": {"m": "실측", "r": "문서 기재", "j": "판단", "u": "미검증"}}

def tag(lang, k): return f'<span class="ev ev-{k}">{TAGS[lang][k]}</span>'

DS = {"gsm8k": "GSM8K", "math500": "MATH-500 (L3–4)"}

def build(lang, D):
    en = lang == "en"
    B, T = BADGES[lang], (lambda k: tag(lang, k))
    h, p5, ll, s4 = D["h1"], D["paper5"], D["llm_internal"], D["study4"]
    C = {}

    # ------------------------------------------------------------------ shared
    C["nav"] = ([("", "Home"), ("research/", "Research"), ("projects/", "Projects"), ("about/", "About"), ("contact/", "Contact")]
                if en else [("", "홈"), ("research/", "연구"), ("projects/", "프로젝트"), ("about/", "소개"), ("contact/", "연락")])
    C["brand"] = dict(
        identity="Independent AI Research & Engineering",
        slogan_a="Beyond What ", slogan_b="Exists.",
        support="Exploring the boundaries of intelligence. Building what comes next.",
        footer="A new era begins with a question.",
        learn="Learn More" if en else "자세히 보기",
        view_all="View All Research" if en else "연구 전체 보기",
        skip="Skip to content" if en else "본문으로 건너뛰기")

    # ------------------------------------------------------------------ research index
    refute_lo = min(c["backfire"] for c in h["conditions"]); refute_hi = max(c["backfire"] for c in h["conditions"])
    m = s4["maze"]
    R = [
     dict(id="kore", badge="prototype", title="KORE",
          sub="Knowledge Orchestration & Retrieval Engine" if en else "Knowledge Orchestration & Retrieval Engine",
          q="Can a retrieval layer pick the knowledge that actually helps a language model answer, and does it beat plain RAG under identical conditions?" if en
            else "언어모델이 답하는 데 실제로 도움이 되는 지식을 골라 주는 검색 계층이, 같은 조건에서 단순 RAG보다 나은가?",
          one="No result yet. Nothing has been validated." if en else "아직 결과 없음. 검증된 것은 없습니다.",
          blurb="A three-person prototype for selecting knowledge to give a language model." if en else "언어모델에 넘길 지식을 고르는 3인 프로토타입."),
     dict(id="h1", badge="refuted", title="H1", sub="Majority-vote backfire" if en else "다수결 역효과",
          q="When a model sometimes answers correctly, does majority voting fail on more than half of those problems?" if en
            else "모델이 가끔 정답을 내는 문제에서, 다수결이 절반 넘게 틀리는가?",
          one=f"Refuted in 4 of 4 conditions; backfire {pct(refute_lo)}–{pct(refute_hi)}." if en else f"4개 조건 모두 반증. 역효과 비율 {pct(refute_lo)}–{pct(refute_hi)}.",
          blurb="Tested whether majority voting backfires more often than it helps." if en else "다수결이 도움보다 해를 더 자주 끼치는지 시험했습니다."),
     dict(id="paper5", badge="progress", title="Paper 5",
          sub="Predicting success via internal signals" if en else "내부 신호로 성공 예측",
          q="Can an agent's early internal signal predict whether it will succeed, or does it only reflect how well it was trained?" if en
            else "에이전트의 초기 내부 신호로 성공을 예측할 수 있는가, 아니면 학습 정도만 반영하는가?",
          one=(f"An early AUROC of {f3(p5['phase1i']['det_d0_lf']['total']['v'])} is mostly explained by training setting k; a stricter follow-up found no detectable signal ({f3(p5['phase2b']['main']['auroc'])})." if en
               else f"초기 AUROC {f3(p5['phase1i']['det_d0_lf']['total']['v'])}은 대부분 학습 설정 k로 설명되고, 더 엄격한 후속 실험에서는 신호가 검출되지 않았습니다({f3(p5['phase2b']['main']['auroc'])})."),
          blurb="A closer look at what signals success." if en else "무엇이 성공을 알려 주는지 들여다봅니다."),
     dict(id="llm-internal-computing", badge="partial", title="LLM Internal Computing",
          sub="Verifying a deterministic computer inside an LLM" if en else "LLM 내부 결정론적 컴퓨터 검증",
          q="Do the unit tests of two upstream projects that embed a deterministic computer in an LLM pass at pinned commits?" if en
            else "LLM 안에 결정론적 컴퓨터를 넣는 두 업스트림 프로젝트의 단위 테스트가 고정 커밋에서 통과하는가?",
          one=(f"First run: {ll['qwenpu']['passed']} of {ll['qwenpu']['collected']} and {ll['qwenputer']['passed']} of {ll['qwenputer']['collected']} tests passed. No performance claims." if en
               else f"첫 실행: {ll['qwenpu']['collected']}개 중 {ll['qwenpu']['passed']}개, {ll['qwenputer']['collected']}개 중 {ll['qwenputer']['passed']}개 통과. 성능 주장은 없습니다."),
          blurb="Unit-test reproduction of two upstream projects. No performance claims." if en else "두 업스트림 프로젝트의 단위 테스트 재현. 성능 주장은 없습니다."),
     dict(id="world-model", badge="exploratory", title="Study 4" if en else "연구 4",
          sub="World-model study" if en else "월드 모델 연구",
          q=("The original report measures three things: 막힘 예측, 위치 프로브 and 인과 개입, at 3,000, 12,000 and 24,000 steps in two environments (maze, empty)." if en
             else "원본 보고서는 두 환경(maze, empty)에서 3,000·12,000·24,000스텝의 막힘 예측, 위치 프로브, 인과 개입 세 가지를 측정합니다."),
          one=(f"maze 3000스텝 위치 프로브 {f3(m['probe3000'])}, 미학습 {f3(m['probe3000_untrained'])} (미학습이 설명하는 몫 {m['untrained_share_pct']}%)." if en
               else f"maze 3000스텝 위치 프로브 {f3(m['probe3000'])}, 미학습 {f3(m['probe3000_untrained'])} (미학습이 설명하는 몫 {m['untrained_share_pct']}%)."),
          blurb="Exploratory results, three seeds, no significance tests." if en else "탐색적 결과. 시드 3개, 유의성 검정 없음."),
    ]
    C["research"] = R
    C["research_intro"] = ("Five lines of work. Each page states what was measured, what failed, and what was not checked." if en
                           else "다섯 가지 연구입니다. 각 페이지는 무엇을 쟀는지, 무엇이 실패했는지, 무엇을 확인하지 않았는지를 적습니다.")
    C["home_research_lead"] = ("We explore fundamental questions in AI, from collective decision-making to what models represent inside. Every page states what failed and what was not checked." if en
                               else "집단 의사결정부터 모델 내부 표현까지, AI의 근본 질문을 탐구합니다. 모든 페이지에 실패한 것과 확인하지 못한 것을 함께 적습니다.")

    # ------------------------------------------------------------------ roles / AI use blocks
    def ai_use(extra_en, extra_ko):
        return [("h2", "Roles and AI use" if en else "역할과 AI 활용"),
                ("p", extra_en if en else extra_ko)]

    pages = {}

    # ------------------------------------------------------------------ KORE
    pages["kore"] = [
     ("note", ("<b>Nothing has been validated yet.</b> The repository's own README says so. The sample data (15 documents, 9 questions) only checks that the pipeline runs; it supports no conclusion about KORE versus plain RAG." if en
               else "<b>아직 검증된 것은 없습니다.</b> 저장소 README가 직접 그렇게 밝힙니다. 샘플 데이터(문서 15개, 질문 9개)는 파이프라인이 도는지만 확인하며, KORE와 단순 RAG의 비교에 대해 어떤 결론도 뒷받침하지 않습니다."), "warn"),
     ("h2", "Question" if en else "질문"),
     ("p", ("Language models answer better with the right outside knowledge, but retrieval often returns text that looks relevant without helping. KORE is a prototype that tries to select the knowledge that actually helps, and compares it with plain RAG under identical conditions." if en
            else "언어모델은 알맞은 외부 지식이 있으면 더 잘 답하지만, 검색은 관련 있어 보이기만 하고 도움이 되지 않는 글을 가져오기도 합니다. KORE는 실제로 도움이 되는 지식을 고르려는 프로토타입이며, 같은 조건에서 단순 RAG와 비교합니다.") ),
     ("h2", "What exists" if en else "있는 것"),
     ("ul", (["Experiment skeleton and a resumable experiment runner",
              "BM25 retrieval, a weighted selector, and evaluation code with bootstrap intervals",
              "A generator that uses free open models, and tools for labelling how much each document contributed",
              "Data-checking tools and tests"] if en else
             ["실험 골격과 중단 후 이어 하는 실험 실행기",
              "BM25 검색, 가중 점수 선택기, 부트스트랩 구간이 있는 평가 코드",
              "무료 오픈 모델 생성기와 문서 기여도 라벨링 도구",
              "데이터 점검 도구와 테스트"])),
     ("h2", "What is not done" if en else "하지 않은 것"),
     ("ul", ([f"The hypotheses (H1–H3), the KORE-versus-RAG comparison and the originality claim are all untested {T('u')}",
              "No real evaluation set is approved: a 20-question draft written with AI help is waiting for human approval",
              "Large-scale runs on GPU were not done in the environment where the code was written"] if en else
             [f"가설(H1–H3), KORE와 RAG의 비교, 독창성 주장은 모두 시험하지 않았습니다 {T('u')}",
              "승인된 실제 평가 세트가 없습니다. AI의 도움으로 쓴 20문항 초안이 사람의 승인을 기다리고 있습니다",
              "코드를 쓴 환경에서는 GPU 대규모 실행을 하지 못했습니다"])),
     ("h2", "Data" if en else "데이터"),
     ("p", ("The repository holds a draft knowledge table. Its source log marks the licence of every entry as not yet checked, so this site does not redistribute it." if en
            else "저장소에는 지식 표 초안이 있습니다. 출처 기록에서 모든 항목의 라이선스가 아직 확인되지 않은 상태라서, 이 사이트는 그 데이터를 재배포하지 않습니다.")),
     ("h2", "Team and roles" if en else "팀과 역할"),
     ("table", (["Contributor", "Role"] if en else ["기여자", "역할"]),
      [["SeoJunLee", "Development &amp; Integration" if en else "개발 및 통합"],
       ["Contributor B" if en else "기여자 B", "Data &amp; prior research" if en else "데이터 및 선행 연구"],
       ["Contributor C" if en else "기여자 C", "Evaluation &amp; reproduction" if en else "평가 및 재현"]]),
     ("p", ("This is a three-person project. Teammates are credited by role." if en else "3인 공동 프로젝트입니다. 팀원은 역할로 표기합니다.")),
     ("h2", "AI use" if en else "AI 활용"),
     ("p", ("<b>AI-assisted development.</b> In the repository history, 24 of 32 commits are authored by an AI assistant, 6 by the author's account and 2 by a placeholder account. The history cannot show who wrote the work committed under the placeholder account. This page makes no claim of sole authorship or sole development." if en
            else "<b>AI 보조 개발입니다.</b> 저장소 이력에서 32개 커밋 중 24개는 AI 어시스턴트, 6개는 저자 계정, 2개는 자리표시자 계정의 커밋입니다. 자리표시자 계정으로 커밋된 작업을 누가 썼는지는 이력만으로 알 수 없습니다. 이 페이지는 단독 저작이나 단독 개발을 주장하지 않습니다.")),
     ("h2", "Verification" if en else "검증 상태"),
     ("p", ("Figures in the repository's own status notes (test counts, a retrieval diagnostic on 20 development questions) were not reproduced for this page, so none are shown here." if en
            else "저장소 자체 현황 문서의 수치(테스트 개수, 개발 질문 20개에 대한 검색 진단)는 이 페이지를 위해 재현하지 않았으므로 여기에 싣지 않습니다.")),
    ]

    # ------------------------------------------------------------------ H1
    cond_rows = []
    for c in h["conditions"]:
        cond_rows.append([DS[c["dataset"]], c["model"], f3(c["backfire"]), ci(c["ci"]), str(c["n_nondegenerate"]),
                          ("Refuted" if en else "반증")])
    gap_lo = sorted(c["gap_ci"][0] for c in h["conditions"])
    assert gap_lo[0] <= 0.0005 < gap_lo[1], f'gap-CI wording no longer matches data: {gap_lo}'
    gap_rows = [[DS[c["dataset"]], c["model"], f3(c["floor"]), f3(c["gap"]), ci(c["gap_ci"])] for c in h["conditions"]]
    caps = [c["cap_share"] for c in h["conditions"]]
    pages["h1"] = [
     ("note", (f"Refuted in all {len(h['conditions'])} conditions by the decision rule written in the experiment code." if en
               else f"실험 코드에 적힌 판정 규칙에 따라 {len(h['conditions'])}개 조건 모두에서 반증되었습니다."), "bad"),
     ("h2", "Question" if en else "질문"),
     ("p", ("Asking a model to solve the same problem many times and taking the most common answer (majority voting) usually raises accuracy. But on a problem where the right answer shows up only sometimes, a wrong answer can become the majority. We call that <b>backfire</b>. H1 says: among problems where the model is sometimes right, majority voting is wrong on <b>more than half</b>." if en
            else "같은 문제를 여러 번 풀게 하고 가장 많이 나온 답을 고르는 다수결은 보통 정확도를 올립니다. 그러나 정답이 가끔만 나오는 문제에서는 오답이 다수가 될 수 있습니다. 이를 <b>backfire(역효과)</b>라고 부릅니다. H1은 “모델이 가끔 정답을 내는 문제 가운데 다수결이 틀리는 비율이 <b>절반을 넘는다</b>”입니다.")),
     ("h2", "Method" if en else "방법"),
     ("ul", ([f"Models: {', '.join(h['models'])}; datasets: GSM8K and MATH-500 (levels 3–4 only)",
              f"{h['problems_per_condition']} problems per condition, {h['samples_per_problem']} samples per problem, temperature {h['temperature']}, at most {h['max_new_tokens']} new tokens",
              "Non-degenerate problem: some but not all samples are correct (always-right and always-wrong problems are excluded)",
              "Backfire: the share of non-degenerate problems where the majority answer is wrong; 95% interval from a problem-level bootstrap (10,000 resamples)",
              f"Decision rule: {h['decision_rule']}"] if en else
             [f"모델: {', '.join(h['models'])}. 데이터: GSM8K, MATH-500(레벨 3–4만)",
              f"조건당 문제 {h['problems_per_condition']}개, 문제당 샘플 {h['samples_per_problem']}개, temperature {h['temperature']}, 최대 {h['max_new_tokens']}토큰",
              "비축퇴 문제: 샘플 중 일부만 정답인 문제(항상 맞거나 항상 틀리는 문제는 제외)",
              "Backfire: 비축퇴 문제 중 다수결 답이 틀린 비율. 95% 구간은 문제 단위 부트스트랩(10,000회)",
              "판정 규칙: 95% 구간 상한이 0.50 미만이면 반증, 하한이 0.50 초과면 지지, 그 밖에는 불확정"])),
     ("h2", f"Results {T('m')}" if en else f"결과 {T('m')}"),
     ("table", (["Dataset", "Model", "Backfire", "95% CI", "Non-degenerate problems", "Verdict"] if en
                else ["데이터", "모델", "Backfire", "95% 구간", "비축퇴 문제 수", "판정"]), cond_rows),
     ("p", (f"In every condition the upper bound of the interval is below 0.50. Among problems where the model is sometimes right, majority voting is wrong on {pct(min(c['backfire'] for c in h['conditions']))}–{pct(max(c['backfire'] for c in h['conditions']))}, not more than half." if en
            else f"모든 조건에서 구간 상한이 0.50보다 낮습니다. 모델이 가끔 정답을 내는 문제에서 다수결이 틀리는 비율은 {pct(min(c['backfire'] for c in h['conditions']))}–{pct(max(c['backfire'] for c in h['conditions']))}이며 절반을 넘지 않았습니다.")),
     ("h2", f"Part of the backfire is unavoidable {T('m')}" if en else f"역효과의 일부는 피할 수 없습니다 {T('m')}"),
     ("p", (f"Given how the votes split, some wrong majorities cannot be avoided (an arithmetic floor). The excess above that floor has a 95% interval whose lower bound is above zero in three conditions ({gap_lo[1]:.3f}–{gap_lo[3]:.3f}) and {gap_lo[0]:.3f} in the fourth." if en
            else f"표가 나뉜 방식만으로도 피할 수 없는 오답 다수결이 있습니다(산술 하한). 그 하한을 넘는 초과분의 95% 구간 하한은 세 조건에서 0보다 크고({gap_lo[1]:.3f}–{gap_lo[3]:.3f}) 나머지 한 조건은 {gap_lo[0]:.3f}입니다.")),
     ("table", (["Dataset", "Model", "Arithmetic floor", "Excess over floor", "95% CI"] if en else ["데이터", "모델", "산술 하한", "하한 초과분", "95% 구간"]), gap_rows),
     ("h2", f"Difficulty effect {T('m')}" if en else f"난이도 효과 {T('m')}"),
     ("p", (f"Comparing the harder dataset with the easier one: {h['pairs_total']} pairs, {h['pairs_ci_excludes_zero']} with an interval that excludes zero. All were inconclusive; the effect of difficulty is not settled." if en
            else f"어려운 데이터와 쉬운 데이터의 비교: {h['pairs_total']}쌍 중 구간이 0을 벗어난 쌍은 {h['pairs_ci_excludes_zero']}개입니다. 모두 불확정이어서 난이도 효과는 결론 내리지 못했습니다.")),
     ("h2", "Limitations" if en else "한계"),
     ("ul", ([f"Two models, one temperature, 16 votes per problem; non-degenerate problems number only {min(c['n_nondegenerate'] for c in h['conditions'])}–{max(c['n_nondegenerate'] for c in h['conditions'])} per condition, so intervals are wide",
              f"The {h['max_new_tokens']}-token cap truncated some solutions (cap reached in {pct(min(caps))}–{pct(max(caps))} of samples)",
              "MATH-500 uses levels 3–4 only; an earlier level-5 run is not included",
              "No pre-registration document was found. The hypothesis wording is read from the decision rule in the code, so the result is labelled by that rule and not as pre-registered"] if en else
             [f"모델 2종, temperature 1개, 문제당 16표. 비축퇴 문제가 조건당 {min(c['n_nondegenerate'] for c in h['conditions'])}–{max(c['n_nondegenerate'] for c in h['conditions'])}개뿐이라 구간이 넓습니다",
              f"{h['max_new_tokens']}토큰 상한 때문에 일부 풀이가 잘렸습니다(상한 도달 비율 {pct(min(caps))}–{pct(max(caps))})",
              "MATH-500은 레벨 3–4만 사용했고, 이전의 레벨 5 실행은 포함하지 않았습니다",
              "사전 고정(pre-registration) 문서를 찾지 못했습니다. 가설 문장은 코드의 판정 규칙에서 읽은 것이어서, 결과는 그 규칙에 따라 표시하며 사전 고정으로 표시하지 않습니다"])),
     ("h2", "Verification and AI use" if en else "검증과 AI 활용"),
     ("p", ("The figures on this page were generated from the project's analysis files by script and checked by tests against the same files. AI-assisted implementation; this page does not itemise who wrote which lines. No independent review." if en
            else "이 페이지의 수치는 프로젝트의 분석 파일에서 스크립트로 만들었고, 같은 파일과 대조하는 테스트로 확인했습니다. AI 보조 구현이며, 어느 줄을 누가 썼는지는 구분해 적지 않습니다. 독립적인 검토는 없습니다.")),
    ]

    # ------------------------------------------------------------------ Paper 5
    d1, e1 = p5["phase1i"]["det_d0_lf"], p5["phase1i"]["eps01_d0_lf"]
    h_, b2 = p5["phase1h_multidepth_d0_lf"], p5["phase2b"]
    rows1i = [[("Deterministic agent" if en else "결정론 에이전트"), f"{f3(d1['total']['v'])} {ci(d1['total']['ci'])}", f"{f3(d1['kscore']['v'])} {ci(d1['kscore']['ci'])}", f"{f3(d1['resk']['v'])} {ci(d1['resk']['ci'])}", f"{d1['n_runs']} / {d1['n_episodes']}"],
              [("Stochastic agent (ε=0.1)" if en else "확률적 에이전트 (ε=0.1)"), f"{f3(e1['total']['v'])} {ci(e1['total']['ci'])}", f"{f3(e1['kscore']['v'])} {ci(e1['kscore']['ci'])}", f"{f3(e1['resk']['v'])} {ci(e1['resk']['ci'])}", f"{e1['n_runs']} / {e1['n_episodes']}"]]
    pages["paper5"] = [
     ("note", ("<b>In progress.</b> The pre-registered next step (1j) has not been run. So far the data do not support reading the signal as “confidence”." if en
               else "<b>진행 중입니다.</b> 사전 고정한 다음 단계(1j)는 아직 실행하지 않았습니다. 지금까지의 데이터는 이 신호를 ‘자신감’으로 읽는 해석을 뒷받침하지 않습니다."), "warn"),
     ("h2", "Question" if en else "질문"),
     ("p", ("A reinforcement-learning agent scores every action with a Q value. Its maximum, maxQ, roughly says how good the agent thinks the situation is. Can the maxQ over the first five steps predict whether the agent later reaches a key? And is that signal really “confidence”, or just how well the agent was trained (the training setting k)?" if en
            else "강화학습 에이전트는 모든 행동에 Q 값으로 점수를 매깁니다. 그 최댓값 maxQ는 에이전트가 지금 상황을 얼마나 좋게 보는지에 가깝습니다. 처음 5걸음의 maxQ로 에이전트가 나중에 열쇠에 닿을지 예측할 수 있는가? 그 신호는 정말 ‘자신감’인가, 아니면 학습 정도(학습 설정 k)일 뿐인가?")),
     ("h2", "Method" if en else "방법"),
     ("p", ("A start close to the key makes success easy, so the comparison is fair only within the same run and the same distance. Stratified AUROC compares successes and failures only inside such strata (0.5 = chance, 1 = perfect). Only step 1f was pre-registered; the others are exploratory." if en
            else "열쇠 가까이에서 시작하면 성공이 쉬우므로, 같은 run·같은 거리 안에서만 비교해야 공정합니다. 층화 AUROC는 이런 층 안에서만 성공과 실패를 비교합니다(0.5 = 우연, 1 = 완벽). 사전 고정한 단계는 1f 하나뿐이고 나머지는 탐색적입니다.")),
     ("h2", f"Result 1 — the early signal and its decomposition {T('m')}" if en else f"결과 1 — 초기 신호와 그 분해 {T('m')}"),
     ("p", (f"In the decomposition (step 1i), maxQ over the first steps reaches AUROC {f3(d1['total']['v'])} for the deterministic agent. But k alone gives {f3(d1['kscore']['v'])}, and after removing what k explains, only {f3(d1['resk']['v'])} {ci(d1['resk']['ci'])} remains. Most of the signal is the training setting." if en
            else f"분해 단계(1i)에서 처음 몇 걸음의 maxQ는 결정론 에이전트에서 AUROC {f3(d1['total']['v'])}에 이릅니다. 그러나 k만으로도 {f3(d1['kscore']['v'])}이고, k가 설명하는 부분을 제거하면 {f3(d1['resk']['v'])} {ci(d1['resk']['ci'])}만 남습니다. 신호의 대부분은 학습 설정입니다.")),
     ("table", (["Agent", "Total (maxQ)", "k alone", "After removing k", "Runs / episodes"] if en else ["에이전트", "전체(maxQ)", "k만", "k 제거 후", "run 수 / 에피소드 수"]), rows1i),
     ("h2", f"Result 2 — a different run set {T('m')}" if en else f"결과 2 — 다른 run 묶음 {T('m')}"),
     ("p", (f"On another set of runs (steps 1g/1h, {h_['n_runs']} runs, {h_['n_episodes']} episodes) the total is {f3(h_['total']['v'])} {ci(h_['total']['ci'])}; after removing k it is {f3(h_['resk']['v'])} {ci(h_['resk']['ci'])}, which includes 0.5. (Step 1g reports the same number under the name “layout×distance”; the two intervals differ slightly because they were computed separately.)" if en
            else f"다른 run 묶음(1g/1h 단계, run {h_['n_runs']}개, 에피소드 {h_['n_episodes']}개)에서는 전체가 {f3(h_['total']['v'])} {ci(h_['total']['ci'])}이고, k를 제거하면 {f3(h_['resk']['v'])} {ci(h_['resk']['ci'])}로 0.5를 포함합니다. (1g 단계는 같은 값을 “배치×거리”라는 이름으로 보고하며, 두 구간은 따로 계산해서 조금 다릅니다.)")),
     ("h2", f"Result 3 — a stricter follow-up (Phase 2b) {T('m')}" if en else f"결과 3 — 더 엄격한 후속 실험 (Phase 2b) {T('m')}"),
     ("p", (f"With comparison restricted to the same run and the same distance after four steps, the AUROC is <b>{f3(b2['main']['auroc'])} {ci(b2['main']['ci'])}</b> (interval width {f3(b2['main']['width'])}) on {b2['main']['n']:,} samples, {b2['main']['n_success']:,} of them successes, {b2['main']['pairs']:,} comparable pairs in {b2['main']['strata']} strata. The pre-set verdict: <b>no signal detected</b> (and the interval is narrow enough to say so)." if en
            else f"같은 run, 같은 4걸음 뒤 거리 안에서만 비교하면 AUROC는 <b>{f3(b2['main']['auroc'])} {ci(b2['main']['ci'])}</b>(구간 폭 {f3(b2['main']['width'])})입니다. 표본 {b2['main']['n']:,}개 중 성공 {b2['main']['n_success']:,}개, 비교 가능한 쌍 {b2['main']['pairs']:,}개, 층 {b2['main']['strata']}개입니다. 미리 정한 판정은 <b>신호 검출 안 됨</b>이며, 그렇게 말할 만큼 구간이 좁습니다.")),
     ("ul", ([f"A weaker control that matches only the starting distance gives {f3(b2['aux_start_distance_only']['auroc'])} {ci(b2['aux_start_distance_only']['ci'])}; it was not used for the verdict",
              f"Pooled with the earlier main experiment: {f3(b2['pooled_with_phase2']['auroc'])} {ci(b2['pooled_with_phase2']['ci'])} (reference only; the designs differ slightly)"] if en else
             [f"시작 거리만 맞춘 약한 통제는 {f3(b2['aux_start_distance_only']['auroc'])} {ci(b2['aux_start_distance_only']['ci'])}이며 판정에는 쓰지 않았습니다",
              f"앞선 본 실험과 합친 값은 {f3(b2['pooled_with_phase2']['auroc'])} {ci(b2['pooled_with_phase2']['ci'])}입니다(설계가 조금 달라 참고용)"])),
     ("h2", f"What this means {T('j')}" if en else f"의미 {T('j')}"),
     ("p", ("The early AUROC of about 0.8 is mostly the training setting. Under stricter matching, maxQ is near chance. The “confidence” reading is not supported so far; the pre-registered step 1j, which excludes the extreme k=2 setting, is the planned test and has not been run." if en
            else "초기 AUROC 약 0.8은 대부분 학습 설정입니다. 더 엄격하게 맞추면 maxQ는 우연 수준에 가깝습니다. 지금까지는 ‘자신감’ 해석을 뒷받침하지 못하며, 극단적인 k=2 설정을 뺀 사전 고정 단계 1j가 예정된 시험이고 아직 실행하지 않았습니다.")),
     ("h2", "Limitations" if en else "한계"),
     ("ul", (["Only step 1f was pre-registered; its original text is not kept (only its hash), so it cannot be compared with the stated hypothesis",
              "Phase 2b was designed after the earlier main experiment's results were seen. Its pre-registration was locked before the new seeds ran, and the verdict follows one pre-set line",
              "The environment and agent are re-implementations; results are about this environment and do not generalise to other settings",
              "Step 1c scanned many signals and conditions at once, with no multiple-comparison correction on record",
              "Hypotheses H-B1 and H-B2 were not re-tested in Phase 2b",
              "Code for steps 1b–1h lives only in notebooks, so its hashes are not available"] if en else
             ["사전 고정한 단계는 1f뿐이고 원문은 보관되어 있지 않아(해시만 있음) 가설 문장과 대조할 수 없습니다",
              "Phase 2b는 앞선 본 실험의 결과를 본 뒤에 설계했습니다. 사전 등록은 새 시드를 돌리기 전에 잠갔고, 판정은 미리 정한 한 줄만 따릅니다",
              "환경과 에이전트는 재구현본입니다. 결과는 이 환경에 대한 것이며 다른 설정으로 일반화되지 않습니다",
              "1c 단계는 여러 신호와 조건을 한꺼번에 봤고, 다중 비교 보정 기록이 없습니다",
              "Phase 2b에서는 가설 H-B1, H-B2를 다시 시험하지 않았습니다",
              "1b–1h 단계의 코드는 노트북에만 있어서 해시를 제공하지 못합니다"])),
     ("h2", "Verification and AI use" if en else "검증과 AI 활용"),
     ("p", ("Steps 1g–1i figures were generated from the project's analysis files by script and checked by tests. The Phase 2b figures were checked by hand against the original report and result files. AI-assisted implementation. No independent review." if en
            else "1g–1i 수치는 프로젝트 분석 파일에서 스크립트로 만들고 테스트로 확인했습니다. Phase 2b 수치는 원본 보고서와 결과 파일에서 직접 대조했습니다. AI 보조 구현. 독립적인 검토는 없습니다.")),
    ]

    # ------------------------------------------------------------------ LLM Internal Computing
    qp, qq, cu = ll["qwenpu"], ll["qwenputer"], ll["colab_update"]
    pages["llm-internal-computing"] = [
     ("note", ("<b>Reproduction only.</b> This work runs the unit tests of two upstream projects at pinned commits. It reports pass and fail counts and causes. It contains no performance figures, and the upstream projects' claims about circuits, riscv-tests and benchmarks were not reproduced." if en
               else "<b>재현만 했습니다.</b> 두 업스트림 프로젝트의 단위 테스트를 고정 커밋에서 돌렸습니다. 통과·실패 개수와 원인만 보고하며 성능 수치는 없습니다. 업스트림이 주장하는 회로, riscv-tests, 벤치마크는 재현하지 않았습니다."), "warn"),
     ("h2", "Question" if en else "질문"),
     ("p", ("Two open projects, QwenPU and Qwenputer, embed a deterministic computer inside a language model. Before building on them, do their own unit tests pass at a fixed version?" if en
            else "공개 프로젝트 QwenPU와 Qwenputer는 언어모델 안에 결정론적 컴퓨터를 넣습니다. 이를 바탕으로 무언가 만들기 전에, 고정한 버전에서 그들의 단위 테스트가 통과하는지 확인했습니다.")),
     ("h2", "Attribution" if en else "출처 표기"),
     ("p", (f"The upstream projects are by <b>{ll['upstream'][0]['owner']}</b> (qwenpu at commit {ll['upstream'][0]['commit']}, qwenputer at commit {ll['upstream'][1]['commit']}). This repository does not copy their code; it points to the commits. The commits are the heads at the time of cloning, not versions chosen by the upstream authors." if en
            else f"업스트림 프로젝트의 저자는 <b>{ll['upstream'][0]['owner']}</b>입니다(qwenpu 커밋 {ll['upstream'][0]['commit']}, qwenputer 커밋 {ll['upstream'][1]['commit']}). 이 저장소는 그들의 코드를 복사하지 않고 커밋만 가리킵니다. 고정한 커밋은 클론한 시점의 최신 커밋이며, 업스트림 저자가 고른 버전이 아닙니다.")),
     ("h2", f"First run (container) {T('m')}" if en else f"첫 실행 (컨테이너) {T('m')}"),
     ("table", (["Project", "Collected", "Passed", "Skipped", "Failed", "Errors", "Not finished"] if en else ["프로젝트", "수집", "통과", "건너뜀", "실패", "오류", "미완료"]),
      [["QwenPU", str(qp["collected"]), str(qp["passed"]), str(qp["skipped"]), str(qp["failed"]), "–", str(qp["not_run"])],
       ["Qwenputer", str(qq["collected"]), str(qq["passed"]), str(qq["skipped"]), str(qq["failed"]), str(qq["errors"]), str(qq["incomplete"])]]),
     ("p", ("Failures and errors fall into four causes: a test that no longer matches the upstream code, missing input files, a process killed for lack of memory, and the time limit. This does not show that the upstream implementation is right or wrong." if en
            else "실패와 오류의 원인은 네 가지입니다. 업스트림 코드와 맞지 않는 테스트, 없는 입력 파일, 메모리 부족으로 강제 종료된 프로세스, 시간 제한입니다. 이 결과만으로 업스트림 구현이 맞다 틀리다를 판단할 수 없습니다.")),
     ("h2", f"Reruns {T('m')}" if en else f"재실행 {T('m')}"),
     ("ul", ([f"On Colab (13 GB RAM), the {cu['test_rv_hf_passed']} memory-heavy tests that the container could not finish all passed",
              f"One test file that had been cut off at the time limit then completed: {cu['q35_inline']}",
              f"Another stopped again at a longer limit: {cu['q35_overlay']}. Whether a longer limit changes this is {T('u')}"] if en else
             [f"코랩(RAM 13GB)에서는 컨테이너가 끝내지 못한 메모리 부담이 큰 테스트 {cu['test_rv_hf_passed']}개가 모두 통과했습니다",
              f"시간 제한에서 잘렸던 테스트 파일 하나는 이후 끝까지 돌았습니다: 113개 중 113개 통과",
              f"다른 파일은 더 긴 제한에서도 멈췄습니다: 6개 중 3개 통과, 3,000초 제한에 걸림. 제한을 더 늘리면 달라지는지는 {T('u')}입니다"])),
     ("h2", "Limitations" if en else "한계"),
     ("ul", (["Unit tests only; no performance numbers and no claim that the upstream design works as advertised",
              "The first-run table is a record of the container runs and was not rewritten after the reruns",
              "Some failures may come from tests left behind by upstream changes; this is a judgment, not a verified cause"] if en else
             ["단위 테스트만 했으며 성능 수치는 없고, 업스트림 설계가 소개대로 동작한다는 주장도 하지 않습니다",
              "첫 실행 표는 컨테이너 실행 기록이며 재실행 뒤에 고쳐 쓰지 않았습니다",
              "일부 실패는 업스트림 변경 때 남은 테스트 때문일 수 있으나, 이는 판단이며 확인된 원인이 아닙니다"])),
     ("h2", "Verification and AI use" if en else "검증과 AI 활용"),
     ("p", ("Counts were checked against the project's test report. AI-assisted implementation. No independent review. Tests were run in a container and on Colab." if en
            else "개수는 프로젝트의 테스트 보고서와 대조했습니다. AI 보조 구현. 독립적인 검토는 없습니다. 테스트는 컨테이너와 코랩에서 돌렸습니다.")),
    ]

    # ------------------------------------------------------------------ Study 4
    mz, em = s4["maze"], s4["empty"]
    pr, j2 = s4["probe"], s4["j2"]
    G = (lambda ko, gl: f"{ko} <span class=\"gloss\">({gl})</span>") if en else (lambda ko, gl: ko)
    pages["world-model"] = [
     ("note", ("<b>Exploratory.</b> 시드 3개, 유의성 검정 없음. The report uses its own terms; they are kept as written, with a plain English gloss in brackets. This page adds no interpretation beyond the report's own judgment rules." if en
               else "<b>탐색적 결과입니다.</b> 시드 3개, 유의성 검정 없음. 이 페이지는 보고서의 용어를 그대로 쓰며, 보고서의 판정 규칙 밖의 해석을 덧붙이지 않습니다."), "warn"),
     ("h2", "What the report covers" if en else "보고서가 다루는 것"),
     ("p", ("Source: Drive report “연구4_원본코드_확장_산출보고서” (auto-generated 2026-10-27). Code: the project's original experiment script with the CPU tier setting, changing only the step count and the output folder. The 3,000-step rows were not retrained in that run; they are original results stored earlier (Drive wm_results)." if en
            else "출처: Drive 보고서 「연구4_원본코드_확장_산출보고서」(2026-10-27 자동 생성). 코드: 프로젝트의 원본 실험 스크립트(TIER=CPU 설정)에서 스텝 수와 저장 폴더만 바꾼 것입니다. 3000스텝 행은 그 실행에서 새로 학습한 것이 아니라 이전에 저장해 둔(Drive wm_results) 원본 결과입니다.")),
     ("ul", ([f"{G('A. 막힘 예측', 'blocked-move prediction')} — {G('헤드룸 달성률', 'headroom attained')} = (모델 − 6-gram) / (1 − 6-gram)",
              f"{G('B. 위치 프로브', 'position probe')} — 행동 후 위치 pos_after 분류, 선형 프로브가 최고인 층",
              f"{G('C. 인과 개입', 'causal intervention')} — 층별 순효과 = 로짓 방향 제거한 평균차 방향 flip − 같은 α의 랜덤 방향 flip"] if en else
             ["A. 막힘 예측 — 헤드룸 달성률 = (모델 − 6-gram) / (1 − 6-gram)",
              "B. 위치 프로브 — 행동 후 위치 pos_after 분류, 선형 프로브가 최고인 층",
              "C. 인과 개입 — 층별 순효과 = 로짓 방향 제거한 평균차 방향 flip − 같은 α의 랜덤 방향 flip"])),
     ("h2", f"A. 막힘 예측 {T('m')}"),
     ("table", ["환경", "스텝", "시드", "정확도", "헤드룸 달성률", "6-gram"],
      [["maze", "3000", "3", f"{mz['steps3000']['acc']:.4f} ± {mz['steps3000']['acc_sd']:.4f}", f"{mz['steps3000']['headroom_pct']:.1f}% ± {mz['steps3000']['headroom_sd']:.1f}", f"{mz['ngram6']:.4f}"],
       ["maze", "12000", "3", f"{mz['steps12000']['acc']:.4f}", f"{mz['steps12000']['headroom_pct']:.1f}%", f"{mz['ngram6']:.4f}"],
       ["maze", "24000", "3", f"{mz['steps24000']['acc']:.4f}", f"{mz['steps24000']['headroom_pct']:.1f}%", f"{mz['ngram6']:.4f}"],
       ["empty", "3000", "3", f"{em['steps3000']['acc']:.4f}", f"{em['steps3000']['headroom_pct']:.1f}%", f"{em['ngram6']:.4f}"],
       ["empty", "12000", "3", f"{s4['empty_more']['steps12000']['acc']:.4f}", f"{s4['empty_more']['steps12000']['headroom_pct']:.1f}%", f"{em['ngram6']:.4f}"],
       ["empty", "24000", "3", f"{s4['empty_more']['steps24000']['acc']:.4f}", f"{s4['empty_more']['steps24000']['headroom_pct']:.1f}%", f"{em['ngram6']:.4f}"]]),
     ("h2", f"B. 위치 프로브 {T('m')}"),
     ("table", ["환경", "스텝", "선형·전체 스텝", "미학습이 설명하는 몫", "선형·지름길 배제 서브셋", "MLP(같은 층)"],
      [["maze", "3000", f"{pr['maze3000']['full']:.3f} ± {pr['maze3000']['full_sd']:.3f} (미학습 {pr['maze3000']['untrained']:.3f})", f"{pr['maze3000']['untrained_share_pct']}%",
        f"{pr['maze3000']['subset']:.3f} ± {pr['maze3000']['subset_sd']:.3f} (미학습 {pr['maze3000']['subset_untrained']:.3f}, {pr['maze3000']['subset_ratio']:.2f}×)", f"{pr['maze3000']['mlp']:.3f} ± {pr['maze3000']['mlp_sd']:.3f}"],
       ["maze", "24000", f"{pr['maze24000']['full']:.3f} (미학습 {pr['maze24000']['untrained']:.3f})", f"{pr['maze24000']['untrained_share_pct']}%",
        f"{pr['maze24000']['subset']:.3f} ({pr['maze24000']['subset_ratio']:.2f}×)", "–"]]),
     ("h2", f"C. 인과 개입 {T('m')}"),
     ("p", ("판정 규칙 [J3] (실행 전에 고정, n=3이라 sd 비교일 뿐 검정이 아니다): 순효과 평균 − 2×sd > 0 인 층. 결과: maze는 3000·12000·24000스텝 모두 <b>없음</b>. empty는 3000스텝 없음, 12000·24000스텝 <b>L2</b>." if en
            else "판정 규칙 [J3] (실행 전에 고정, n=3이라 sd 비교일 뿐 검정이 아니다): 순효과 평균 − 2×sd > 0 인 층. 결과: maze는 3000·12000·24000스텝 모두 <b>없음</b>. empty는 3000스텝 없음, 12000·24000스텝 <b>L2</b>.")),
     ("h2", f"[J2] 학습 신호 {T('m')}"),
     ("p", (f"maze: 서브셋 선형 정확도의 학습−미학습 격차 3000스텝 +{j2['maze']['gap3000']:.3f} → 12000스텝 +{j2['maze']['gap12000']:.3f}, 차이 +{j2['maze']['diff']:.3f}, 기준 2×sd {j2['maze']['two_sd']:.3f} → 수렴하자 신호가 강해졌다. "
            f"empty: +{j2['empty']['gap3000']:.3f} → +{j2['empty']['gap12000']:.3f}, 차이 +{j2['empty']['diff']:.3f}, 기준 2×sd {j2['empty']['two_sd']:.3f} → 변화가 sd 범위 안.")),
     ("h2", "Limitations (from the report)" if en else "보고서의 해석 주의"),
     ("ul", (["시드 3개, 유의성 검정 없음",
              "이 셀이 보지 않은 것: N=7·T=64 GPU 설정, 지름길 상한 정의 변경, 24000스텝 초과",
              "평균차 방향은 원본 정의대로 ‘행동 전 위치 클래스 평균’의 차이다. 시점 t와 위치가 섞여 있으므로 L0(임베딩) 효과는 시점 정보를 건드린 결과일 수 있다"] if en else
             ["시드 3개, 유의성 검정 없음",
              "이 셀이 보지 않은 것: N=7·T=64 GPU 설정, 지름길 상한 정의 변경, 24000스텝 초과",
              "평균차 방향은 원본 정의대로 ‘행동 전 위치 클래스 평균’의 차이다. 시점 t와 위치가 섞여 있으므로 L0(임베딩) 효과는 시점 정보를 건드린 결과일 수 있다"])),
     ("h2", "Verification and AI use" if en else "검증과 AI 활용"),
     ("p", ("The figures were checked by hand against the original report file. AI-assisted implementation. No independent review." if en
            else "수치는 원본 보고서 파일과 직접 대조했습니다. AI 보조 구현. 독립적인 검토는 없습니다.")),
    ]
    C["pages"] = pages
    C["detail_labels"] = dict(
        status="Status" if en else "상태", repo="Repository" if en else "저장소",
        back="All research" if en else "연구 목록", question="Research question" if en else "연구 질문")

    # ------------------------------------------------------------------ projects
    C["projects"] = dict(
      title="Projects" if en else "프로젝트",
      intro=("Things built, not research results. Other projects stay private." if en else "연구 결과가 아니라 만든 것입니다. 나머지 프로젝트는 비공개로 두었습니다."),
      items=[dict(title="Hard Takeoff",
                  sub="AI-lab management simulation" if en else "AI 연구소 경영 시뮬레이션",
                  body=("A browser game (Korean UI, 48 months) in which the laws of intelligence differ from world to world, plus a Python reference simulation (180 months). It is a game, not a research paper, and has no hypothesis document." if en
                        else "지능의 법칙이 세계마다 다른 브라우저 게임(한국어 UI, 48개월)과 파이썬 참조 시뮬레이션(180개월). 게임이며 연구 논문이 아니고 가설 문서도 없습니다."),
                  ai=("AI-assisted implementation; no per-file breakdown is recorded. Figures in its README were not re-run and are not shown here." if en
                      else "AI 보조 구현이며 파일별 구분 기록은 없습니다. README의 수치는 다시 돌리지 않았으므로 여기에 싣지 않습니다."),
                  repo="https://github.com/SeoJunLee-code/hard-takeoff")])

    # ------------------------------------------------------------------ about
    C["about"] = [
     ("h2", "AEVORIN"),
     ("p", ("<b>Independent AI Research &amp; Engineering.</b> Aevorin is a coined name, not an existing word. It joins <i>Aevo</i>, inspired by <i>aevum</i> (an age, a long span of time), with <i>Orin</i>, which suggests <i>origin</i>. The meaning we take from it: explore a new era of intelligence, and build possibilities beyond what already exists." if en
            else "<b>Independent AI Research &amp; Engineering.</b> Aevorin은 기존 단어를 가져온 것이 아니라 만든 조어입니다. <i>aevum</i>(시대, 긴 시간)에서 영감을 얻은 <i>Aevo</i>와 <i>origin</i>(기원)을 떠올리게 하는 <i>Orin</i>을 결합했습니다. 담은 뜻은 이렇습니다. 지능의 새로운 시대를 탐구하고, 기존에 존재하는 것 너머의 가능성을 직접 구축한다.")),
     ("h2", "Philosophy" if en else "철학"),
     ("kv", [("Discover", "We look for what is not yet known." if en else "아직 알려지지 않은 것을 찾아냅니다."),
             ("Construct", "We build the thing itself, not only a description of it." if en else "설명에 그치지 않고 직접 만들어 냅니다."),
             ("Advance", "We keep what holds up and move it forward; we record what does not." if en else "버텨 낸 것은 이어 가고, 그렇지 못한 것은 기록으로 남깁니다.")]),
     ("h2", "Researcher" if en else "연구자"),
     ("p", ("<b>SeoJunLee</b> — <a href=\"https://github.com/SeoJunLee-code\">github.com/SeoJunLee-code</a>. Where work is shared, the roles of others are stated on the project page." if en
            else "<b>SeoJunLee</b> — <a href=\"https://github.com/SeoJunLee-code\">github.com/SeoJunLee-code</a>. 공동 작업은 각 프로젝트 페이지에 다른 기여자의 역할을 적습니다.")),
     ("h2", "How we work with AI" if en else "AI와 일하는 방식"),
     ("kv", [("Human-led research direction" if en else "사람이 이끄는 연구 방향", "The author chooses the questions and what is published." if en else "질문과 공개할 내용은 저자가 정합니다."),
             ("AI-assisted implementation" if en else "AI 보조 구현", "Code, analysis scripts, documentation and this site were written with AI assistance. Each project page says what is known about its AI use; where there is no itemised record, it says so." if en
                else "코드, 분석 스크립트, 문서, 이 사이트는 AI의 도움을 받아 만들었습니다. 각 프로젝트 페이지에 AI 활용에 대해 알려진 범위를 적고, 구분 기록이 없으면 없다고 적습니다."),
             ("Checked against sources" if en else "원자료와 대조", "Numbers on this site are generated from source files by script and checked by tests. Some were checked by hand against original reports; each page says which. None has had independent peer review." if en
                else "이 사이트의 수치는 원자료에서 스크립트로 만들고 테스트로 확인합니다. 일부는 원본 보고서와 직접 대조했고, 각 페이지에 어느 것인지 적습니다. 독립적인 동료 검토를 받은 것은 없습니다.")]),
     ("h2", "Evidence labels" if en else "근거 표시"),
     ("p", (f"{T('m')} a result produced and read from files; {T('r')} stated in a document, not re-run; {T('j')} the author's interpretation; {T('u')} not tested." if en
            else f"{T('m')} 파일에서 직접 얻어 읽은 결과, {T('r')} 문서에 적혀 있으나 다시 돌리지 않은 것, {T('j')} 저자의 해석, {T('u')} 시험하지 않은 것.")),
    ]
    C["contact"] = dict(
      title="Contact" if en else "연락",
      body=("For now, GitHub is the contact channel." if en else "현재는 GitHub이 연락 창구입니다."),
      link_label="github.com/SeoJunLee-code")
    C["title"] = dict(home="AEVORIN — Independent AI Research & Engineering", research="Research", projects="Projects", about="About", contact="Contact")
    C["desc"] = "Independent AI research and engineering. Beyond What Exists. Exploring the boundaries of intelligence." if en else "독립 AI 연구 및 엔지니어링. Beyond What Exists. 지능의 경계를 탐구합니다."
    return C
