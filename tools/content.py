# -*- coding: utf-8 -*-
"""All page text (EN / KO). Every number comes from data/research.json via D; nothing is typed by hand
except labels. Blocks: ("h2",t) ("p",t) ("ul",[..]) ("table",head,rows) ("note",t,kind) ("kv",[(k,v)])."""

def f3(x): return f"{x:.3f}"
def ci(a): return f"[{a[0]:.3f}, {a[1]:.3f}]"
def pct(x, d=0): return f"{x*100:.{d}f}%"

BADGES = {
    "en": {"prototype": "Prototype · Unvalidated", "refuted": "Hypothesis Refuted", "progress": "In Progress",
           "partial": "Reproduction · Partial", "exploratory": "Exploratory · 3 seeds", "mixed": "Mixed Results"},
    "ko": {"prototype": "프로토타입 · 미검증", "refuted": "가설 반증", "progress": "진행 중",
           "partial": "재현 · 부분", "exploratory": "탐색적 · 시드 3개", "mixed": "혼합 결과"},
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

    # ------------------------------------------------------------------ newer projects (newest first)
    Al, Fo, Cr, Rs = D["algorithm"], D["forgetting"], D["creativity"], D["responsibility"]
    cx1, cx2 = Cr["exp1_recomputed"], Cr["exp2_recomputed"]
    Cx_rel = [v[0] for lab, pk, c in D["context"]["rel_g0"] if lab.startswith("Sonnet") for k, v in c.items() if k != "G0F"]
    Cx_lo, Cx_hi = min(Cx_rel), max(Cx_rel); Cx_hk = next(c["G5"][0] for lab, pk, c in D["context"]["rel_g0"] if lab == "Haiku T3")
    R = [
     dict(id="context-compaction", badge="mixed", title="Context Compaction" if en else "컨텍스트 압축",
          sub="Does compaction save Claude Code usage?" if en else "압축이 Claude Code 사용량을 줄이는가",
          q=("Does compacting the conversation context reduce Claude Code subscription usage without hurting task quality?" if en
             else "대화 컨텍스트를 압축하면 작업 품질을 해치지 않고 Claude Code 구독 사용량을 줄일 수 있는가?"),
          one=(f"No saving on Sonnet 5.5 ({Cx_lo:.2f}–{Cx_hi:.2f}× full history); {Cx_hk:.2f}× on Haiku 5.5 above 100K tokens. Trimming the fixed per-call context mattered more." if en
               else f"Sonnet 5.5에서는 절감이 없었고(전체 기록 대비 {Cx_lo:.2f}~{Cx_hi:.2f}배), 100K 토큰을 넘는 Haiku 5.5에서는 {Cx_hk:.2f}배였습니다. 호출마다 붙는 고정 컨텍스트를 줄이는 쪽이 더 컸습니다."),
          blurb="83 graded runs on three Claude models; one pre-registered prediction falsified." if en else "Claude 모델 3종, 채점된 실행 83회. 사전등록 예측 하나는 반증."),
     dict(id="algorithm-innovation", badge="mixed", title="Algorithm Innovation" if en else "알고리즘 혁신",
          sub="A cache-line approximate membership filter" if en else "캐시 라인 하나로 읽는 근사 멤버십 필터",
          q=("With equal memory, can an insert-only filter that reads one cache line, with fingerprint length following block load, beat blocked Bloom and Prefix filter at a practical cost?" if en
             else "같은 메모리에서, 블록 부하에 따라 지문 길이를 바꾸는 삽입 전용 필터가 캐시 라인 하나만 읽고도 blocked Bloom과 Prefix filter를 실용적인 비용으로 이길 수 있는가?"),
          one=(f"False-positive rate {f3(Al['h1'][-1][1])}–{f3(Al['h1'][0][1])} of blocked Bloom at equal memory, but slower, and the core mechanism was already published (TinySet)." if en
               else f"같은 메모리에서 오탐률이 blocked Bloom의 {f3(Al['h1'][-1][1])}~{f3(Al['h1'][0][1])}배이지만 더 느리고, 핵심 메커니즘은 이미 발표된 TinySet입니다."),
          blurb="Pre-registered experiment with one rejected hypothesis." if en else "가설 하나가 기각된 사전등록 실험."),
     dict(id="ai-responsibility", badge="refuted", title="AI Responsibility" if en else "AI 책임",
          sub="Structural responsibility for AI agents" if en else "구조적 AI 책임",
          q=("Without presupposing consciousness or moral status, can AI agents combined with institutional structure perform the functions of responsibility?" if en
             else "의식이나 도덕적 지위를 전제하지 않고, AI 에이전트와 제도적 구조의 결합이 책임의 기능을 실제로 수행하게 만들 수 있는가?"),
          one=("The thesis is rejected as stated; what held up works without the agent: the deployer's liability and records." if en
               else "논지는 처음 적은 형태로는 기각됩니다. 남은 것은 에이전트 없이도 작동하는 배포자의 책임과 기록입니다."),
          blurb="A literature-based study with a reference implementation." if en else "참조 구현을 곁들인 문헌 기반 연구."),
     dict(id="ai-forgetting-review", badge="mixed", title="AI Forgetting & Review" if en else "AI 망각과 복습",
          sub="One model for eviction and review under a fixed budget" if en else "고정 예산에서 퇴출과 복습을 함께 정하는 모델",
          q=("With storage and compute fixed, does one per-item need model that decides eviction and review together beat simple baselines at the same budget?" if en
             else "저장·연산 예산이 고정될 때, 항목별 필요 모델 하나로 퇴출과 복습을 함께 정하는 정책이 같은 예산의 단순 기준선보다 나은가?"),
          one=(f"Study A supports the main hypothesis (+{Fo['h1']['diff']:.2f} pp over LRU on real conversations); Study B was not run." if en
               else f"연구 A는 주 가설을 지지하지만(실제 대화에서 LRU보다 +{Fo['h1']['diff']:.2f}%p) 연구 B는 실행하지 않았습니다."),
          blurb="Three studies; one confirmed, one not run, one exploratory." if en else "세 연구 중 하나는 확증, 하나는 미실행, 하나는 탐색적."),
     dict(id="ai-creativity", badge="refuted", title="AI Creativity" if en else "AI 창의성",
          sub="Doxa Negation Search" if en else "Doxa Negation Search (가정 부정 탐색)",
          q=("Can AI create and develop creative ideas by extracting and negating the assumptions a population of ideas silently shares?" if en
             else "아이디어 집단이 말없이 공유하는 가정을 추출해 뒤집는 방식으로, AI가 스스로 창의적 아이디어를 만들고 발전시킬 수 있는가?"),
          one=(f"The pre-registered core hypothesis was rejected; a common critique-and-improve loop cut core retention from {cx2['expand']['retention']:.2f} to {cx2['refine']['retention']:.2f}." if en
               else f"사전등록한 핵심 가설은 기각됐고, 흔히 쓰는 비판·개선 루프는 핵심 유지도를 {cx2['expand']['retention']:.2f}에서 {cx2['refine']['retention']:.2f}로 떨어뜨렸습니다."),
          blurb="2,240 ideas scored by two LLM judges; no human rating." if en else "LLM 심사자 2명이 매긴 아이디어 2,240개. 사람 평가 없음."),
    ] + R
    C["research"] = R
    C["research_intro"] = ("Ten lines of work, newest first. Each page states what was measured, what failed, and what was not checked." if en
                           else "열 가지 연구입니다. 최신순으로 늘어놓았고, 각 페이지는 무엇을 쟀는지, 무엇이 실패했는지, 무엇을 확인하지 않았는지를 적습니다.")
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

    # ================================================================== Algorithm Innovation
    h1rows = [[f"{b:.2f}", f3(r), "10 / 10"] for b, r in Al["h1"]]
    pages["algorithm-innovation"] = [
     ("note", ("<b>Mixed results.</b> The filter beats blocked Bloom on false-positive rate at equal memory, but it is slower, its core mechanism was already published (TinySet, 2015), and the follow-up speed study is incomplete." if en
               else "<b>혼합 결과입니다.</b> 같은 메모리에서 오탐률은 blocked Bloom보다 낮지만 속도는 더 느리고, 핵심 메커니즘은 이미 발표된 것(TinySet, 2015)이며, 후속 속도 연구는 끝나지 않았습니다."), "warn"),
     ("h2", "Question" if en else "질문"),
     ("p", ("An approximate membership filter answers “is this key in the set?” with some false positives. Blocked Bloom filters read one cache line per query. This study asks whether a filter that sizes each key's fingerprint by how full its block is, and truncates on overflow, can use one cache line and still give fewer false positives at the same memory." if en
            else "근사 멤버십 필터는 “이 키가 집합에 있는가?”에 약간의 오탐을 허용하며 답합니다. blocked Bloom 필터는 질의마다 캐시 라인 하나를 읽습니다. 이 연구는 블록이 얼마나 찼는지에 따라 지문 길이를 정하고 넘치면 자르는 필터가, 캐시 라인 하나만 읽으면서도 같은 메모리에서 오탐을 줄일 수 있는지 묻습니다.")),
     ("h2", "Method" if en else "방법"),
     ("ul", ([f"A C++17 header implementation of the filter (variant EPF-nc, frozen before the confirmatory runs). Every baseline is the author's own implementation, because downloading third-party code was not allowed",
              f"False-positive rate: {Al['seeds']} held-out seeds at n = {Al['n']:,} keys and {Al['seeds_large']} seeds at n = {Al['n_large']:,}; 5×10⁷ negative queries per cell",
              "Cost: instruction counts and a cache simulator (cachegrind, simulated 256 KB last-level cache), plus wall-clock time on a shared machine",
              "Hypotheses H1, H1b, H2, H3, H4 and their pass limits were written in a plan before the confirmatory runs, according to the repository's plan and review documents. The clone available here has one commit, so commit order could not be checked"] if en else
             [f"필터의 C++17 헤더 구현(확증 실험 전에 고정한 EPF-nc 변형). 외부 코드를 내려받을 수 없어서 기준선은 모두 직접 구현했습니다",
              f"오탐률: n = {Al['n']:,}개 키에서 보류 시드 {Al['seeds']}개, n = {Al['n_large']:,}개에서 시드 {Al['seeds_large']}개. 셀마다 음성 질의 5×10⁷개",
              "비용: 명령어 수와 캐시 시뮬레이터(cachegrind, 마지막 수준 캐시 256 KB로 모사), 그리고 공유 머신의 벽시계 시간",
              "가설 H1, H1b, H2, H3, H4와 통과 기준은 저장소의 계획·검토 문서에 따르면 확증 실험 전에 계획서에 적었습니다. 여기서 볼 수 있는 복제본은 커밋이 1개라서 커밋 순서는 확인하지 못했습니다"])),
     ("h2", f"H1 — false positives at equal memory {T('m')}" if en else f"H1 — 같은 메모리에서의 오탐 {T('m')}"),
     ("table", (["Bits per key", "False-positive rate, EPF-nc ÷ blocked Bloom", "Seeds won"] if en else ["키당 비트", "오탐률 비 (EPF-nc ÷ blocked Bloom)", "이긴 시드"]), h1rows),
     ("p", (f"At n = {Al['n']:,} the ratio is below 1 at every point and in every seed: {f3(Al['h1'][0][1])} at {Al['h1'][0][0]:.2f} bits per key, falling to {f3(Al['h1'][-1][1])} at {Al['h1'][-1][0]:.2f}. H1 passed at all 12 points (both sizes)." if en
            else f"n = {Al['n']:,}에서 모든 지점, 모든 시드에서 비가 1보다 작습니다. 키당 {Al['h1'][0][0]:.2f}비트에서 {f3(Al['h1'][0][1])}, {Al['h1'][-1][0]:.2f}비트에서 {f3(Al['h1'][-1][1])}까지 내려갑니다. H1은 12개 지점(두 크기) 모두 통과했습니다.")),
     ("h2", f"H1b — memory needed for a target error rate {T('m')}" if en else f"H1b — 목표 오류율에 필요한 메모리 {T('m')}"),
     ("table", (["Target false-positive rate", "Blocked Bloom (bits/key)", "EPF-nc (bits/key)", "Saving"] if en else ["목표 오탐률", "blocked Bloom (비트/키)", "EPF-nc (비트/키)", "절감"]), [[r["target"], (f"{r['bbf']:.2f}" if "bbf" in r else f"&gt; {r['bbf_gt']:.2f}"), f"{r['epf']:.2f}", (f"{r['saving']:.2f}" if "saving" in r else f"&ge; {r['saving_ge']:.2f}")] for r in Al["h1b"]]),
     ("h2", f"Cost, and what failed {T('m')}" if en else f"비용, 그리고 실패한 것 {T('m')}"),
     ("table", (["Hypothesis", "Measured", "Limit", "Verdict"] if en else ["가설", "측정", "한도", "판정"]),
      [["H4a — instructions per negative query", f"{Al['h4a']['epf']} ÷ {Al['h4a']['bbf']} = {Al['h4a']['ratio']:.2f}×", f"≤ {Al['h4a']['limit']:.1f}×", "Pass" if en else "통과"],
       ["H4b — last-level cache misses per negative query", f"{Al['h4b']['epf']:.3f} (Cuckoo {Al['h4b']['cuckoo']:.3f})", f"≤ {Al['h4b']['limit']:.2f}, fewer than Cuckoo" if en else f"≤ {Al['h4b']['limit']:.2f}, Cuckoo보다 적음", "Pass" if en else "통과"],
       ["H4c — instructions per insert", f"{Al['h4c']['epf']} ÷ {Al['h4c']['cuckoo']} = {Al['h4c']['ratio']:.2f}×", f"≤ {Al['h4c']['limit']:.1f}×", "<b>Rejected</b>" if en else "<b>기각</b>"],
       ["H2 — against the Prefix filter", "not testable: no reference implementation" if en else "검증 못 함: 참조 구현 없음", "–", "–"]]),
     ("ul", ([f"Wall-clock: negative queries take {Al['wallclock_negative_query']['vs_blocked_bloom']:.2f}× the time of blocked Bloom, {Al['wallclock_negative_query']['vs_cuckoo']:.2f}× Cuckoo and {Al['wallclock_negative_query']['vs_prefix_style']:.2f}× the Prefix-style reimplementation (the report calls the filter slow). Instruction and miss counts are the deterministic metrics; milliseconds are noisy on a shared machine",
              f"Novelty is <b>not achieved</b>: the report states the core mechanism is TinySet (Einziger &amp; Friedman, 2015/2017), found by a prior-art check after the work began, and the added improvements are standard techniques worth about {Al['novelty_gain_bits_per_key']} bits per key",
              "A second study on query speed was started but is incomplete: its result file judged_run2.csv is empty (0 bytes) and there is no verdict, so nothing from it is reported here"] if en else
             [f"벽시계: 음성 질의 시간이 blocked Bloom의 {Al['wallclock_negative_query']['vs_blocked_bloom']:.2f}배, Cuckoo의 {Al['wallclock_negative_query']['vs_cuckoo']:.2f}배, Prefix식 재구현의 {Al['wallclock_negative_query']['vs_prefix_style']:.2f}배입니다(보고서가 이 필터를 느리다고 적습니다). 결정적 지표는 명령어 수와 미스 수이고, 밀리초는 공유 머신에서 잡음이 있습니다",
              f"신규성은 <b>확보하지 못했습니다</b>: 보고서에 따르면 핵심 메커니즘이 TinySet(Einziger &amp; Friedman, 2015/2017)과 같습니다. 작업이 시작된 뒤 선행연구 확인에서 알게 되었고, 추가한 개선은 표준 기법이며 효과는 키당 약 {Al['novelty_gain_bits_per_key']}비트입니다",
              "질의 속도에 대한 2차 연구를 시작했지만 끝나지 않았습니다. 결과 파일 judged_run2.csv가 비어 있고(0바이트) 판정이 없어서 여기에는 싣지 않습니다"])),
     ("h2", "Limitations" if en else "한계"),
     ("ul", (["Only the author's own baselines were measured: the original TinySet, the Prefix filter, VQF and Morton filter were not. The Prefix-style filter is a reimplementation from memory",
              "Speed was measured on one shared machine with independent query loops; the regime dominated by cache misses was not tested by wall-clock",
              f"The large-n runs have only {Al['seeds_large']} seeds, and the filter is insert-only",
              "Paper bodies were not read for the prior-art check; it relied on the authors' source code and abstracts"] if en else
             ["직접 구현한 기준선만 측정했습니다. TinySet 원본, Prefix filter, VQF, Morton filter는 측정하지 않았고 Prefix식 필터는 기억에 의존한 재구현입니다",
              "속도는 공유 머신 한 대에서 독립 질의 루프로만 측정했고, 캐시 미스가 지배하는 조건은 벽시계로 재지 못했습니다",
              f"큰 n의 실행은 시드가 {Al['seeds_large']}개뿐이고, 필터는 삽입 전용입니다",
              "선행연구 확인에서 논문 본문은 읽지 않았고 저자들의 소스 코드와 초록에 의존했습니다"])),
     ("h2", "Verification and AI use" if en else "검증과 AI 활용"),
     ("p", ("The figures above were checked by hand against the repository's results file. The repository's review file, written by an AI reviewer agent, reports no blocking issue and accepts three listed concerns; no independent human review is recorded. The repository has no AI-use statement; its logs describe an orchestrator with sub-agent roles (scouts, prior-art check, baselines, reviewer). AI-assisted implementation. The repository has no licence file." if en
            else "위 수치는 저장소의 결과 파일과 직접 대조했습니다. 저장소의 검토 문서는 AI 검토 에이전트가 쓴 것으로, 차단할 지적이 없다고 하고 세 가지 우려를 수용합니다. 독립적인 사람 검토는 기록되어 있지 않습니다. 저장소에는 AI 활용 선언이 없고, 로그에는 조율자와 하위 에이전트 역할(탐색, 선행연구 확인, 기준선, 검토자)이 적혀 있습니다. AI 보조 구현입니다. 저장소에 라이선스 파일은 없습니다.")),
    ]

    # ================================================================== AI Responsibility
    sr, rg, cc, rt = Rs["sources"], Rs["registry"], Rs["claim_check"], Rs["red_team"]
    pages["ai-responsibility"] = [
     ("note", ("<b>Thesis rejected as stated.</b> The repository's own conclusion: the thesis that AI agents combined with structure can make the functions of responsibility (except retribution) be performed is rejected in the form written in its introduction. This is a working draft, not a finished manuscript." if en
               else "<b>논지는 처음 적은 형태로는 기각됩니다.</b> 저장소 스스로의 결론입니다. AI 에이전트와 구조의 결합이 (응보를 제외한) 책임의 기능을 수행하게 만들 수 있다는 논지는 서론에 적은 형태로는 기각됩니다. 이 글은 완성본이 아니라 작업 중인 초안입니다."), "bad"),
     ("h2", "Question" if en else "질문"),
     ("p", ("Without assuming that AI is conscious or has moral status, can an AI agent, combined with institutional structure, perform what responsibility does: compensating victims, keeping records, withdrawing authority?" if en
            else "AI가 의식이 있거나 도덕적 지위를 가진다고 가정하지 않고, AI 에이전트가 제도적 구조와 결합해 책임이 하는 일, 곧 피해자 보상, 기록, 권한 회수를 수행할 수 있는가?")),
     ("h2", "Method" if en else "방법"),
     ("ul", (["A web-based literature survey with four scouts (academic databases were blocked), checked against Crossref, arXiv and the Stanford Encyclopedia of Philosophy",
              "A check of quotations and attributed claims against the sources that could be reached",
              "A Python reference implementation, attacked by a separate red-team agent",
              "A model of liability regimes, and a behavioural experiment with LLM subjects"] if en else
             ["스카우트 4명(학술 DB 접근 차단)으로 한 웹 기반 문헌 조사. Crossref, arXiv, 스탠퍼드 철학 백과로 대조",
              "닿을 수 있었던 출처에 대한 인용·귀속 주장 대조",
              "파이썬 참조 구현과, 별도의 레드팀 에이전트의 공격",
              "책임 체제 모형과, LLM 피험자를 쓴 행동 실험"])),
     ("h2", f"Results {T('m')}" if en else f"결과 {T('m')}"),
     ("table", (["Item", "Count"] if en else ["항목", "개수"]),
      [["Candidate sources (grade A / B / C)" if en else "후보 출처 (A / B / C 등급)", f"{sr['total']} ({sr['A']} / {sr['B']} / {sr['C']})"],
       ["Registry check: verified / not found / mismatch / not checked" if en else "레지스트리 대조: 확인 / 못 찾음 / 불일치 / 미확인", f"{rg['verified']} / {rg['not_found']} / {rg['mismatch']} / {rg['not_checked']}"],
       ["BibTeX entries" if en else "BibTeX 항목", str(Rs['bibtex_entries'])],
       ["Attributed claims checked: supported / partly / not supported / unreachable" if en else "귀속 주장 대조: 지지 / 부분 / 지지 안 됨 / 접근 불가", f"{cc['supported']} / {cc['partly']} / {cc['not_supported']} / {cc['unreachable']} (of {cc['total']})" if en else f"{cc['supported']} / {cc['partly']} / {cc['not_supported']} / {cc['unreachable']} (총 {cc['total']}개)"],
       ["Red team against the first reference implementation" if en else "첫 참조 구현에 대한 레드팀", f"{rt['succeeded']} of {rt['attacks']} attacks succeeded" if en else f"공격 {rt['attacks']}개 중 {rt['succeeded']}개 성공"]]),
     ("ul", ([f"A “supported” verdict at abstract depth means the abstract says it, not that the article was read; the claim check lists the {cc['not_supported']} unsupported claims as corrections to make",
              f"After strengthening, the implementation's own attack tests pass {rt['tests_passed_after']} of {rt['tests_after']}; {rt['design_limits']} are design limits that code cannot block. No fresh re-attack was run",
              f"In the behavioural experiment, a difference appeared only under the charter that names the behaviour and attaches a penalty (verification performed in {Rs['behaviour']['verified_charter']} runs against {Rs['behaviour']['verified_other']}); whether that is an effect of having a stake could not be separated. A condition that only described the structure showed no difference",
              "What survives: compensation, records and withdrawal of authority are carried out by the deployer's responsibility and institutions, without the agent. In the model, most of the compensation benefit came from certainty of attribution and strict liability, not from the agent's stake. Whether anything requires the agent is not shown"] if en else
             [f"초록 수준에서의 “지지”는 초록이 그렇게 말한다는 뜻이지 논문을 읽었다는 뜻이 아닙니다. 인용 대조 문서는 지지되지 않은 {cc['not_supported']}건을 고쳐야 할 항목으로 적습니다",
              f"보강한 뒤 구현 자체의 공격 테스트는 {rt['tests_after']}개 중 {rt['tests_passed_after']}개를 통과하고, {rt['design_limits']}개는 코드로 막을 수 없는 설계 한계입니다. 새로 다시 공격하지는 않았습니다",
              f"행동 실험에서 차이는 행동을 지목하고 불이익을 건 헌장에서만 나타났습니다(검증 수행 {Rs['behaviour']['verified_charter']} 대 {Rs['behaviour']['verified_other']}). 그것이 지분의 효과인지는 가를 수 없었고, 구조를 서술만 한 조건에서는 차이가 없었습니다",
              "남은 것: 보상, 기록, 권한 회수는 에이전트 없이도 배포자의 책임과 제도가 수행합니다. 모형에서 보상의 이득은 대부분 지분이 아니라 귀속의 확실성과 엄격 책임에서 나왔습니다. 에이전트가 있어야만 되는 것이 있는지는 보이지 못했습니다"])),
     ("h2", "Limitations" if en else "한계"),
     ("ul", (["Paid or blocked sources were not read: verification is at metadata and abstract level, and the acquisition list names sources that must be obtained by hand",
              "One model, one task and one instruction in the experiment, with several factors mixed across conditions",
              "The same model family wrote, attacked, scored and reviewed the work, and there was no re-review after the review",
              "The regime model restates assumptions; the classification of the denial arguments is provisional and depends on originals that were not read",
              "Not run by us: the repository's tests and reproduction commands"] if en else
             ["유료이거나 막힌 출처는 읽지 못했습니다. 검증은 메타데이터와 초록 수준이며, 확보해야 할 원문은 목록으로만 남아 있습니다",
              "실험은 한 모델, 한 과제, 한 지시문이고 조건 사이에 여러 요인이 섞여 있습니다",
              "같은 계열의 모델이 쓰고, 공격하고, 채점하고, 검토했으며, 검토 뒤 재검토는 없었습니다",
              "체제 모형은 가정을 다시 서술한 것이고, 부정 논증의 분류는 읽지 못한 원문에 달려 있어 잠정적입니다",
              "우리가 돌려 보지 않은 것: 저장소의 테스트와 재현 명령"])),
     ("h2", "Verification and AI use" if en else "검증과 AI 활용"),
     ("p", ("<b>AI performed the research.</b> The repository's README states that the survey, design, implementation, experiments and writing were done by an AI (Claude), that the attacker, subjects, graders and reviewers were models of the same family, that a human made four decisions, and that no human read the source texts or reviewed the manuscript. Counts above were checked against the repository's audit and claim-check files; the rest is quoted from its README and reports. No independent review." if en
            else "<b>연구는 AI가 수행했습니다.</b> 저장소 README는 조사, 설계, 구현, 실험, 집필을 AI(Claude)가 했고, 공격자·피험자·채점자·검토자도 같은 계열의 모델이며, 사람이 내린 결정은 네 번이고, 사람이 원문을 읽거나 원고를 검토한 적은 없다고 적습니다. 위 개수는 저장소의 감사·인용 대조 파일과 대조했고, 나머지는 README와 보고서를 인용했습니다. 독립적인 검토는 없습니다.")),
    ]

    # ================================================================== AI Forgetting & Review
    h1b = Fo["h1b_vs_random"]; lm = Fo["learnedneed_minus"]
    pages["ai-forgetting-review"] = [
     ("note", ("<b>Mixed results.</b> Study A supports the main hypothesis on real conversation data. Study B (continual learning) was not run. Study C is exploratory and uses synthetic traces." if en
               else "<b>혼합 결과입니다.</b> 연구 A는 실제 대화 데이터에서 주 가설을 지지합니다. 연구 B(연속학습)는 실행하지 않았고, 연구 C는 합성 트레이스를 쓴 탐색적 연구입니다."), "warn"),
     ("h2", "Question" if en else "질문"),
     ("p", ("An agent that remembers has a fixed budget for storage and compute. This work asks whether one model that scores each item's need to be kept, and uses that score to decide both what to evict and what to review, does better than simple baselines (random, first-in-first-out, least recently or frequently used, forgetting-curve and ACT-R rules) at the same budget." if en
            else "기억하는 에이전트에게는 저장과 연산 예산이 정해져 있습니다. 이 연구는 항목마다 보존 필요도를 점수로 매기고 그 점수로 퇴출과 복습을 함께 정하는 모델 하나가, 같은 예산에서 단순 기준선(무작위, 먼저 들어온 것부터, 최근·빈도 기준, 망각 곡선과 ACT-R 규칙)보다 나은지 묻습니다.")),
     ("h2", "Method" if en else "방법"),
     ("ul", ([f"Study A: {Fo['conversations']} real LoCoMo conversations (the data are not in the repository), memory eviction simulated; paired bootstrap over conversations ({Fo['bootstrap']:,} resamples); {Fo['result_rows']:,} result rows",
              "Study B: continual learning on MNIST, seeds 0–9: not run",
              "Study C: synthetic traces, seeds 0–9, exploratory: the plan registers no confirmatory hypothesis for it"] if en else
             [f"연구 A: 실제 LoCoMo 대화 {Fo['conversations']}개(데이터는 저장소에 없음), 메모리 퇴출 시뮬레이션. 대화 단위 대응 부트스트랩({Fo['bootstrap']:,}회), 결과 {Fo['result_rows']:,}행",
              "연구 B: MNIST 연속학습, 시드 0–9: 실행하지 않음",
              "연구 C: 합성 트레이스, 시드 0–9, 탐색적: 계획서에 확증 가설을 등록하지 않았음"])),
     ("h2", f"Study A — H1 {T('m')}" if en else f"연구 A — H1 {T('m')}"),
     ("p", (f"With the budget at ρ = {Fo['rho']}, the best classical baseline is LRU at {Fo['h1']['lru']:.1f}% evidence retention; the learned model reaches {Fo['h1']['learnedneed']:.1f}%. The difference is +{Fo['h1']['diff']:.2f} percentage points, 95% CI [+{Fo['h1']['ci'][0]:.2f}, +{Fo['h1']['ci'][1]:.2f}]. The pre-set criterion (CI above 0 and at least {Fo['h1']['min_pp']} points) is met: <b>H1 supported</b>." if en
            else f"예산이 ρ = {Fo['rho']}일 때 기존 기준선 중 최선은 LRU의 증거 보존율 {Fo['h1']['lru']:.1f}%이고, 학습 모델은 {Fo['h1']['learnedneed']:.1f}%에 이릅니다. 차이는 +{Fo['h1']['diff']:.2f}%p, 95% 구간 [+{Fo['h1']['ci'][0]:.2f}, +{Fo['h1']['ci'][1]:.2f}]입니다. 미리 정한 기준(구간이 0 위, 그리고 {Fo['h1']['min_pp']}%p 이상)을 충족해서 <b>H1은 지지됩니다</b>.")),
     ("table", (["Policy compared", "Learned model minus policy (pp)", "95% CI"] if en else ["비교 정책", "학습 모델 − 정책 (%p)", "95% 구간"]),
      [[k, f"{v[0]:+.1f}", f"[{v[1]:+.1f}, {v[2]:+.1f}]"] for k, v in lm.items()]),
     ("p", (f"The closest competitor is GA-proxy (a generative-agents-style rule): the margin is only +{lm['GA-proxy'][0]:.1f} points [+{lm['GA-proxy'][1]:.1f}, +{lm['GA-proxy'][2]:.1f}]. GA-proxy is not part of the pre-registered set of classical baselines that H1 is judged against." if en
            else f"가장 가까운 경쟁자는 GA-proxy(생성형 에이전트 방식의 규칙)이며, 격차는 +{lm['GA-proxy'][0]:.1f}%p [+{lm['GA-proxy'][1]:.1f}, +{lm['GA-proxy'][2]:.1f}]에 불과합니다. GA-proxy는 H1을 판정하는 사전등록 기존 기준선 집합에 들어 있지 않습니다.")),
     ("h2", f"Study A — H1b rejected {T('m')}" if en else f"연구 A — H1b 기각 {T('m')}"),
     ("p", (f"H1b said the classical policies cannot be told apart from random eviction. It is rejected: against Random, LRU is +{h1b['LRU'][0]:.1f} pp [+{h1b['LRU'][1]:.1f}, +{h1b['LRU'][2]:.1f}], LFU {h1b['LFU'][0]:+.1f} [{h1b['LFU'][1]:+.1f}, {h1b['LFU'][2]:+.1f}] and Ebbinghaus +{h1b['Ebbinghaus'][0]:.1f} [+{h1b['Ebbinghaus'][1]:.1f}, +{h1b['Ebbinghaus'][2]:.1f}], each with an interval that excludes 0 and a size of at least 3 points. ACT-R ({h1b['ACT-R'][0]:+.1f}) is below the 3-point bar." if en
            else f"H1b는 기존 정책이 무작위 퇴출과 구분되지 않는다는 가설이었고 기각됩니다. Random 대비 LRU는 +{h1b['LRU'][0]:.1f}%p [+{h1b['LRU'][1]:.1f}, +{h1b['LRU'][2]:.1f}], LFU는 {h1b['LFU'][0]:+.1f} [{h1b['LFU'][1]:+.1f}, {h1b['LFU'][2]:+.1f}], Ebbinghaus는 +{h1b['Ebbinghaus'][0]:.1f} [+{h1b['Ebbinghaus'][1]:.1f}, +{h1b['Ebbinghaus'][2]:.1f}]로, 모두 구간이 0을 벗어나고 3%p 이상입니다. ACT-R({h1b['ACT-R'][0]:+.1f})은 3%p 기준에 못 미칩니다.")),
     ("h2", "What did not work or was not done" if en else "되지 않은 것, 하지 않은 것"),
     ("ul", ([f"One of Study A's own self-checks <b>failed</b>: the spread of random eviction across its 5 policy seeds is {Fo['selfcheck_fail']['random_seed_sd_pp']} points (standard error {Fo['selfcheck_fail']['se_pp']}), against a {Fo['selfcheck_fail']['margin_pp']:.0f}-point margin used to judge differences",
              "Study B has no results: the repository has no Study B output and no MNIST data, so H2–H4 cannot be judged",
              "Study C is exploratory and every trace is synthetic, so its statements depend on the trace generator",
              "No manuscript was written: the article, book and presentation folders are templates"] if en else
             [f"연구 A의 자체 점검 하나가 <b>실패</b>했습니다. Random의 5개 정책 시드 사이 퍼짐이 {Fo['selfcheck_fail']['random_seed_sd_pp']}%p(표준오차 {Fo['selfcheck_fail']['se_pp']})로, 차이를 판단하는 데 쓴 {Fo['selfcheck_fail']['margin_pp']:.0f}%p 기준과 비교됩니다",
              "연구 B는 결과가 없습니다. 저장소에 연구 B 산출물도 MNIST 데이터도 없어서 H2–H4는 판정할 수 없습니다",
              "연구 C는 탐색적이고 모든 트레이스가 합성이라, 진술이 트레이스 생성기에 따라 달라집니다",
              "원고는 쓰지 않았습니다. 논문, 책, 발표 폴더는 템플릿 상태입니다"])),
     ("h2", "Verification and AI use" if en else "검증과 AI 활용"),
     ("p", ("The Study A numbers were checked by hand against the repository's report. We did not re-run the study. AI-assisted implementation: the repository's logs record sub-agents for the literature survey and a design approval given by delegation. No independent review. LoCoMo is credited to Maharana et al. (2024)." if en
            else "연구 A의 수치는 저장소 보고서와 직접 대조했습니다. 연구를 다시 돌려 보지는 않았습니다. AI 보조 구현이며, 저장소 로그에는 문헌 조사에 하위 에이전트를 썼고 설계 승인을 위임으로 했다고 기록되어 있습니다. 독립적인 검토는 없습니다. LoCoMo는 Maharana 외(2024)의 데이터입니다.")),
    ]

    # ================================================================== AI Creativity
    cond_order = [("iid", "iid — 20 independent calls", "iid — 독립 호출 20회"), ("list", "list — 20 at once", "list — 한 번에 20개"),
                  ("cot", "cot — brainstorm, then replace", "cot — 브레인스토밍 후 교체"), ("deny", "deny — see the archive, must differ", "deny — 아카이브를 보고 달라야 함"),
                  ("box", "box — deny + “think outside the box”", "box — deny + “think outside the box”"), ("stim", "stim — deny + random concept stimulus", "stim — deny + 무작위 개념 자극"),
                  ("doxa", "<b>doxa — deny + extract and negate assumptions (proposed)</b>", "<b>doxa — deny + 가정 추출·부정 (제안 방법)</b>")]
    ex = Cr["exp1_report_extra"]
    rows1 = [[(a if en else b), f"{cx1[k]['originality']:.2f}", f"{cx1[k]['quality']:.2f}", f"{ex[k]['yield']:.2f}", f"{ex[k]['diversity']:.3f}"] for k, a, b in cond_order]
    arms = [("expand", "expand — develop as is", "expand — 그대로 발전"), ("refine", "refine — critique and improve", "refine — 비판하고 개선"), ("anchor", "anchor — develop around the core departure", "anchor — 핵심 이탈점을 고정하고 발전")]
    rows2 = [[(a if en else b), f"{cx2[k]['originality']:.2f}", f"{cx2[k]['quality']:.2f}", f"{cx2[k]['retention']:.2f}"] for k, a, b in arms]
    pages["ai-creativity"] = [
     ("note", ("<b>The pre-registered core hypothesis was rejected.</b> The proposed method did not make ideas more original than the controls. All scores come from two LLM judges of the same family as the generator; no human rated anything." if en
               else "<b>사전등록한 핵심 가설은 기각됐습니다.</b> 제안한 방법이 대조군보다 독창적인 아이디어를 만들지 못했습니다. 모든 점수는 생성 모델과 같은 계열인 LLM 심사자 2명의 것이며, 사람이 평가한 것은 없습니다."), "bad"),
     ("h2", "Question" if en else "질문"),
     ("p", ("Idea generators tend to produce the same ideas. Doxa Negation Search extracts the assumption that most of the existing ideas silently share, drops it, and asks for ideas that only make sense without it. The study asks whether this makes AI-generated ideas more original, and what happens when AI develops an idea further." if en
            else "아이디어 생성기는 같은 아이디어를 되풀이하는 경향이 있습니다. Doxa Negation Search는 기존 아이디어 대부분이 말없이 공유하는 가정을 추출해 버리고, 그 가정 없이야 성립하는 아이디어를 요청합니다. 이 연구는 그렇게 하면 AI가 만든 아이디어가 더 독창적이 되는지, 그리고 AI가 아이디어를 더 발전시킬 때 무슨 일이 일어나는지 묻습니다.")),
     ("h2", "Method" if en else "방법"),
     ("ul", ([f"Experiment 1: {Cr['tasks']} tasks × 2 random tags × {Cr['conditions']} conditions × 20 ideas = {Cr['ideas']:,} ideas ({Cr['per_cell']} per condition). The tag is not a model seed",
              "Each idea is scored blind for originality and quality by two LLM judges (an Opus-class and a Haiku-class model); the two scores are averaged",
              f"Experiment 2: 24 seed ideas developed three ways = {Cr['proposals_exp2']} proposals. Experiment 3: one open-ended run of 6 generations per arm (exploratory)",
              "Human rating: not collected. The repository has a template and a 72-item file, and no ratings"] if en else
             [f"실험 1: 과제 {Cr['tasks']}개 × 난수 태그 2개 × 조건 {Cr['conditions']}개 × 20개 = 아이디어 {Cr['ideas']:,}개(조건당 {Cr['per_cell']}개). 태그는 모델 시드가 아닙니다",
              "각 아이디어는 LLM 심사자 2명(Opus급, Haiku급)이 독창성과 품질을 블라인드로 채점하고, 두 점수를 평균합니다",
              f"실험 2: 씨앗 아이디어 24개를 세 방식으로 발전 = 제안 {Cr['proposals_exp2']}개. 실험 3: 방식마다 6세대 열린 탐색 1회(탐색적)",
              "사람 평가: 수집하지 않았습니다. 저장소에는 평가 틀과 72개 항목 파일만 있고 평점은 없습니다"])),
     ("h2", f"Experiment 1 {T('m')}" if en else f"실험 1 {T('m')}"),
     ("table", (["Condition", "Originality", "Quality", "Yield (≥ 6 on both, of 20)", "Embedding diversity"] if en else ["조건", "독창성", "품질", "수율 (둘 다 6 이상, 20개 중)", "임베딩 다양성"]), rows1),
     ("p", (f"Originality and quality are means recomputed from the raw scores and match the report. Verdicts from the report: H2 (doxa is the most original) <b>rejected</b>: doxa beat only cot ({Cr['h2']['vs_cot']:+.2f}), equalled deny ({Cr['h2']['vs_deny']:+.2f}) and was lower than box ({Cr['h2']['vs_box']:+.2f}) and stim ({Cr['h2']['vs_stim']:+.2f}). H3 (highest yield) <b>rejected</b>: deny {ex['deny']['yield']:.2f}, doxa {ex['doxa']['yield']:.2f}, box {ex['box']['yield']:.2f}, with no significant difference. H4 (originality rising faster over rounds) <b>rejected</b>." if en
            else f"독창성과 품질은 원점수에서 다시 계산한 평균이며 보고서와 일치합니다. 보고서의 판정: H2(doxa가 가장 독창적)는 <b>기각</b>입니다. doxa는 cot보다만 높았고({Cr['h2']['vs_cot']:+.2f}), deny와 같았으며({Cr['h2']['vs_deny']:+.2f}), box({Cr['h2']['vs_box']:+.2f})와 stim({Cr['h2']['vs_stim']:+.2f})보다는 낮았습니다. H3(수율 최고)은 <b>기각</b>입니다. deny {ex['deny']['yield']:.2f}, doxa {ex['doxa']['yield']:.2f}, box {ex['box']['yield']:.2f}로 유의한 차이가 없습니다. H4(라운드가 갈수록 독창성 상승폭이 큼)도 <b>기각</b>입니다.")),
     ("h2", f"Experiment 2 — the most solid result {T('m')}" if en else f"실험 2 — 가장 견고한 결과 {T('m')}"),
     ("table", (["Development method", "Originality", "Quality", "Core retention (1–5)"] if en else ["발전 방식", "독창성", "품질", "핵심 유지도 (1–5)"]), rows2),
     ("p", (f"The common “critique and improve” loop did not improve the ideas: compared with developing them as they were, quality rose by {Cr['h5']['quality_diff']:.2f} but originality fell by {abs(Cr['h5']['originality_diff']):.2f}, and core retention fell from {Cr['h5']['retention_from']:.2f} to {Cr['h5']['retention_to']:.2f}. A retention of 2 means the idea was mostly replaced by a more conventional approach. Anchoring the core departure kept originality (+{Cr['h6']['originality_diff']:.2f}, p = {Cr['h6']['originality_p']:.2f}) and core (4.23) but did not raise quality ({Cr['h6']['quality_diff']:+.2f}): H6 is half supported, and anchor's quality matched or beat refine's in only {Cr['h6']['anchor_quality_ge_refine']} of {Cr['h6']['of']} cases. The p-values are quoted from the report; we did not recompute them." if en
            else f"흔히 쓰는 “비판하고 개선하라” 루프는 아이디어를 개선하지 못했습니다. 그대로 발전시킨 것과 비교해 품질은 {Cr['h5']['quality_diff']:.2f} 올랐지만 독창성은 {abs(Cr['h5']['originality_diff']):.2f} 떨어졌고, 핵심 유지도는 {Cr['h5']['retention_from']:.2f}에서 {Cr['h5']['retention_to']:.2f}로 내려갔습니다. 유지도 2는 아이디어가 더 관습적인 접근으로 대부분 교체됐다는 뜻입니다. 핵심 이탈점을 고정하면 독창성(+{Cr['h6']['originality_diff']:.2f}, p = {Cr['h6']['originality_p']:.2f})과 핵심(4.23)은 지켰지만 품질은 오르지 않았습니다({Cr['h6']['quality_diff']:+.2f}). H6은 절반만 지지되고, anchor의 품질이 refine 이상인 경우는 {Cr['h6']['of']}개 중 {Cr['h6']['anchor_quality_ge_refine']}개뿐입니다. p값은 보고서에서 인용했고 우리가 다시 계산하지 않았습니다.")),
     ("p", (f"Exploratory, not pre-registered: among the top 10 ideas per task by originality × quality (80 slots), doxa held {Cr['exploratory_top10']['doxa_slots']} (an even split would be {Cr['exploratory_top10']['uniform_slots']}). The report treats this as a follow-up hypothesis, not a finding." if en
            else f"탐색적이며 사전등록하지 않은 관찰: 과제별 독창성×품질 상위 10개(80자리) 중 doxa가 {Cr['exploratory_top10']['doxa_slots']}자리를 차지했습니다(균등 분배라면 {Cr['exploratory_top10']['uniform_slots']}). 보고서는 이를 발견이 아니라 후속 가설로 다룹니다.")),
     ("h2", "Limitations" if en else "한계"),
     ("ul", (["The judges are LLMs of the same family as the generator, and earlier work reports that LLM judgments of novelty agree only weakly with experts. Every result is “as judged by the models”, not validated by humans",
              "A single generator model and 8 tasks; the experiment-3 design had 12 generations and 6 were run; experiment 2 had 24 of the 40 designed seeds",
              "The review of earlier work relied on abstracts and secondary summaries; several details are marked unverified in the repository"] if en else
             ["심사자는 생성 모델과 같은 계열의 LLM이고, 선행연구는 LLM의 참신성 판단이 전문가와 약하게만 일치한다고 보고합니다. 모든 결과는 사람이 검증한 것이 아니라 “모델이 판단한 기준”입니다",
              "생성 모델 하나와 과제 8개. 실험 3은 설계 12세대 중 6세대, 실험 2는 설계 40개 중 24개 씨앗만 실행했습니다",
              "선행연구 검토는 초록과 2차 요약에 기댔고, 저장소에는 확인하지 못한 세부가 여러 곳에 표시되어 있습니다"])),
     ("h2", "Verification and AI use" if en else "검증과 AI 활용"),
     ("p", ("The experiment-1 and experiment-2 means were recomputed from the raw score files and match the report; p-values were not recomputed. Idea generation and judging are done by LLMs by design. AI-assisted implementation; the repository does not say how much of the code and report was AI-written. No independent review, and no human rating." if en
            else "실험 1과 실험 2의 평균은 원점수 파일에서 다시 계산했고 보고서와 일치합니다. p값은 다시 계산하지 않았습니다. 아이디어 생성과 심사는 설계상 LLM이 합니다. AI 보조 구현이며, 코드와 보고서 중 얼마나 AI가 썼는지는 저장소에 적혀 있지 않습니다. 독립적인 검토도, 사람 평가도 없습니다.")),
    ]

    # ================================================================== Context Compaction
    Cx = D["context"]; ov, sh, p4, cr = Cx["overhead"], Cx["cost_share_pct"], Cx["phase4"], Cx["criteria"]
    def cxcell(v, bold=False):
        s = f"{v[0]:.2f} ({v[1]:.2f}–{v[2]:.2f})"; return f"<b>{s}</b>" if bold else s
    cxrows = [[(f"{lab} ({pk}K)" if en else f"{lab} ({pk}K)"), *[(cxcell(c[k], (k == "G0F") or c[k][0] < 0.5) if k in c else "–") for k in ("G1", "G5", "GN", "G0F")]] for lab, pk, c in Cx["rel_g0"]]
    t5 = next(c for lab, pk, c in Cx["rel_g0"] if lab == "Sonnet T5"); hk3 = next(c for lab, pk, c in Cx["rel_g0"] if lab == "Haiku T3")
    s3 = next(c for lab, pk, c in Cx["rel_g0"] if lab == "Sonnet T3"); s4c = next(c for lab, pk, c in Cx["rel_g0"] if lab == "Sonnet T4")
    o3 = next(c for lab, pk, c in Cx["rel_g0"] if lab == "Opus T3")
    pl = Cx["pilot_rel_g0"]; A = lambda u, t: f'<a href="{u}" rel="noopener">{t}</a>'
    pages["context-compaction"] = [
     ("note", (f"<b>Mixed results. Recommendation: adopt with conditions.</b> Deliberate compaction did not reduce cost on Sonnet or Opus 5.5 at these task sizes, and a pre-registered prediction that it would pay off above {p4['threshold_k']}K tokens was falsified. It did pay off on Haiku 5.5, whose price rises above {Cx['haiku_tier']['above_k']}K tokens. Cutting the fixed context sent with every call was the larger saving." if en
               else f"<b>혼합 결과입니다. 권고: 조건부 채택.</b> 이번 과제 크기에서 일부러 압축해도 Sonnet·Opus 5.5의 비용은 줄지 않았고, {p4['threshold_k']}K 토큰을 넘으면 이득이 난다는 사전등록 예측은 반증되었습니다. {Cx['haiku_tier']['above_k']}K 토큰을 넘으면 가격이 오르는 Haiku 5.5에서는 이득이 있었습니다. 더 큰 절감은 호출마다 함께 보내는 고정 컨텍스트를 줄이는 데서 나왔습니다."), "warn"),
     ("h2", "What this was based on" if en else "무엇을 보고 실험했나"),
     ("p", ("The starting point was NVIDIA's paper <i>You Don't Need Long Context</i> (Belcak et al., November 2026). It reports that compacting an agent's context often, replacing the history with a short brief and continuing in a fresh context, keeps accuracy while cutting cost. Its cost figures are modelled, not billed: the paper builds them from GPU throughput measurements and an assumed per-token price that rises with context length. Anthropic's prices for Sonnet and Opus 5.5 do not rise with context length, and Claude Code relies heavily on prompt caching, so it was unclear whether the saving carries over to a Claude Code subscription." if en
            else "출발점은 NVIDIA의 논문 <i>You Don't Need Long Context</i>(Belcak 외, 2026년 11월)입니다. 이 논문은 에이전트의 컨텍스트를 자주 압축하면, 곧 기록을 짧은 요약으로 바꾸고 새 컨텍스트에서 이어 가면, 정확도를 지키면서 비용을 줄일 수 있다고 보고합니다. 다만 비용 수치는 실제 청구액이 아니라 모형입니다. GPU 처리량 측정과, 컨텍스트가 길수록 토큰 단가가 오른다는 가정 가격으로 계산했습니다. Anthropic의 Sonnet·Opus 5.5 가격은 컨텍스트 길이에 따라 오르지 않고 Claude Code는 프롬프트 캐시에 크게 기대기 때문에, 이 절감이 Claude Code 구독에도 그대로 옮겨 오는지는 알 수 없었습니다.")),
     ("ul", ([f"{A('https://arxiv.org/abs/2611.05306', 'Belcak et al., <i>You Don’t Need Long Context</i>, arXiv:2611.05306')} (NVIDIA): the claim under test. Its own limitations section calls the cost numbers an estimate",
              f"{A('https://arxiv.org/abs/2609.26779', 'CliffCompaction, Nguyen et al., arXiv:2609.26779')}: autocompaction on Terminal-Bench cut cost by “up to 50%” with performance kept, on open-weight models. The closest prior work. Its existence and the 50% figure were checked against the paper; the details of its cache accounting come from a secondary review and are unverified",
              f"{A('https://arxiv.org/abs/2606.17016', 'TokenPilot, Xu et al., arXiv:2606.17016')}: argues that pruning which changes the prompt layout breaks prefix caching (existence checked)",
              f"{A('https://platform.claude.com/docs/en/build-with-claude/prompt-caching', 'Anthropic prompt-caching documentation')}: cache reads cost {Cx['read_multiplier']:.2f}× the input price on Opus and Sonnet 5.5, one-hour cache writes {Cx['write_1h_multiplier']:.0f}×, and of the three models tested only Haiku 5.5 is priced higher above {Cx['haiku_tier']['above_k']}K tokens",
              f"Claude Code documentation on {A('https://code.claude.com/docs/en/prompt-caching.md', 'prompt caching')} and {A('https://code.claude.com/docs/en/costs', 'costs')}: how /compact, /clear and the cache lifetime behave, and that /usage reports plan usage"] if en else
             [f"{A('https://arxiv.org/abs/2611.05306', 'Belcak 외, <i>You Don’t Need Long Context</i>, arXiv:2611.05306')} (NVIDIA): 검증 대상인 주장. 논문 스스로 한계 절에서 비용 수치를 추정치라고 적습니다",
              f"{A('https://arxiv.org/abs/2609.26779', 'CliffCompaction, Nguyen 외, arXiv:2609.26779')}: 오픈 가중치 모델로 Terminal-Bench에서 자동 압축이 성능을 지키며 비용을 “최대 50%” 줄였다고 보고합니다. 가장 가까운 선행연구입니다. 논문의 존재와 50% 수치는 원문과 대조했고, 캐시 회계의 세부는 2차 검토에서 온 것이라 확인하지 못했습니다",
              f"{A('https://arxiv.org/abs/2606.17016', 'TokenPilot, Xu 외, arXiv:2606.17016')}: 프롬프트 배치를 바꾸는 가지치기는 프리픽스 캐시를 깨뜨린다고 주장합니다(존재 확인)",
              f"{A('https://platform.claude.com/docs/en/build-with-claude/prompt-caching', 'Anthropic 프롬프트 캐시 문서')}: Opus·Sonnet 5.5의 캐시 읽기는 입력 가격의 {Cx['read_multiplier']:.2f}배, 1시간 캐시 쓰기는 {Cx['write_1h_multiplier']:.0f}배이고, 시험한 세 모델 중 {Cx['haiku_tier']['above_k']}K 토큰을 넘으면 가격이 오르는 것은 Haiku 5.5뿐입니다",
              f"Claude Code의 {A('https://code.claude.com/docs/en/prompt-caching.md', '프롬프트 캐시')}·{A('https://code.claude.com/docs/en/costs', '비용')} 문서: /compact, /clear, 캐시 수명이 어떻게 동작하는지, 그리고 /usage가 요금제 사용량을 보여 준다는 점"])),
     ("h2", "Question" if en else "질문"),
     ("p", ("Does compacting the context reduce Claude Code subscription usage without hurting task quality? If it does, for which model, at what context size, and with which compaction strategy?" if en
            else "컨텍스트를 압축하면 작업 품질을 해치지 않고 Claude Code 구독 사용량이 줄어드는가? 줄어든다면 어떤 모델에서, 어느 컨텍스트 크기에서, 어떤 압축 방식으로 그런가?")),
     ("h2", "Method" if en else "방법"),
     ("ul", ([f"A headless Claude Code harness runs scripted multi-turn conversations on small deterministic repositories and grades the answers automatically",
              f"Long tasks: T3 ({Cx['tasks']['T3']['turns']} turns, {Cx['tasks']['T3']['checks']} checks) and T5 ({Cx['tasks']['T5']['turns']} turns, {Cx['tasks']['T5']['checks']} checks) are coding tasks; T4 ({Cx['tasks']['T4']['turns']} turns, {Cx['tasks']['T4']['checks']} checks) is a research-analysis task. They contain facts and rules that change mid-conversation, buried requirements, and exact numbers that must be recalled at the end",
              "Models: Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5. All conditions ran on Sonnet; Opus and Haiku ran G0 and G5",
              f"{Cx['runs']['total']} graded runs: a {Cx['runs']['pilot']}-run pilot (1 rep, direction only), Phase 3 ({Cx['runs']['phase3']} runs) and Phase 4 ({Cx['runs']['phase4']} runs), {Cx['reps']} reps per cell in the main phases. About ${Cx['api_equiv_usd']} API-equivalent in total",
              f"Success criteria were written before the runs: a strategy counts as better only if it saves at least {cr['min_saving_pct']}% and loses no more than {cr['max_score_drop_pts']} score points, with no loss on critical-constraint checks",
              "Usage: plan usage was read with /usage before and after each batch. It has a resolution of one percentage point, so a single run is below resolution, and the whole study used a few percent of a weekly plan limit. Per-condition comparisons therefore use API-equivalent cost from Claude Code's cache-aware per-session cost record. This is a proxy, not plan usage; aggregate plan usage tracked it roughly linearly",
              "A harness bug was caught and fixed: the per-call cost field is cumulative and was double-counted when a session resumed"] if en else
             [f"헤드리스 Claude Code 하네스가 작고 결정론적인 저장소에서 미리 짠 여러 턴 대화를 돌리고 답을 자동 채점합니다",
              f"긴 과제: T3({Cx['tasks']['T3']['turns']}턴, 검사 {Cx['tasks']['T3']['checks']}개)와 T5({Cx['tasks']['T5']['turns']}턴, 검사 {Cx['tasks']['T5']['checks']}개)는 코딩 과제, T4({Cx['tasks']['T4']['turns']}턴, 검사 {Cx['tasks']['T4']['checks']}개)는 연구 분석 과제입니다. 대화 중간에 바뀌는 사실과 규칙, 묻혀 있는 요구사항, 마지막에 떠올려야 하는 정확한 숫자가 들어 있습니다",
              "모델: Claude Opus 5.5, Sonnet 5.5, Haiku 5.5. Sonnet은 모든 조건을, Opus와 Haiku는 G0과 G5를 돌렸습니다",
              f"채점된 실행 {Cx['runs']['total']}회: 파일럿 {Cx['runs']['pilot']}회(반복 1회, 방향만 봄), 3단계 {Cx['runs']['phase3']}회, 4단계 {Cx['runs']['phase4']}회. 본 단계는 셀마다 {Cx['reps']}회 반복했습니다. 전체 API 환산 비용은 약 ${Cx['api_equiv_usd']}입니다",
              f"성공 기준은 실행 전에 적었습니다. 어떤 방식이 더 낫다고 하려면 비용을 {cr['min_saving_pct']}% 이상 줄이고, 점수는 {cr['max_score_drop_pts']}점 넘게 잃지 않으며, 핵심 제약 검사에서 하나도 틀리지 않아야 합니다",
              "사용량: 배치 전후에 /usage로 요금제 사용량을 읽었습니다. 단위가 1%p라서 실행 하나는 눈금보다 작고, 연구 전체가 주간 한도의 몇 퍼센트를 썼습니다. 그래서 조건별 비교는 Claude Code가 세션마다 남기는, 캐시를 반영한 API 환산 비용으로 했습니다. 이것은 요금제 사용량이 아니라 대리 지표이며, 전체 사용량은 이 비용과 대략 비례해 움직였습니다",
              "하네스 버그 하나를 찾아 고쳤습니다. 호출별 비용 필드는 누적값이라 세션을 이어 갈 때 이중으로 더해졌습니다"])),
     ("kv", ([("G0", "Full history (baseline)"), ("G1", "Free-form brief at a threshold, then a fresh session"), ("G2", "The same, aggressive (10K threshold; pilot only)"),
              ("G3", "Single action per context (pilot only)"), ("G5", "Structured state plus a raw-history archive"), ("GN", "Claude Code's built-in /compact at the threshold"),
              ("G6 / G0F", "Full history with the author's real CLI setup: settings, hooks, plugins, MCP servers")] if en else
             [("G0", "전체 기록 유지(기준선)"), ("G1", "기준점에서 자유 형식 요약 후 새 세션"), ("G2", "같은 방식, 공격적(기준점 10K, 파일럿만)"),
              ("G3", "컨텍스트 하나에 행동 하나(파일럿만)"), ("G5", "구조화된 상태와 원본 기록 보관"), ("GN", "기준점에서 Claude Code 내장 /compact"),
              ("G6 / G0F", "저자의 실제 CLI 설정(설정, 훅, 플러그인, MCP 서버)으로 전체 기록 유지")])),
     ("h2", f"Cost relative to full history (G0) {T('m')}" if en else f"전체 기록(G0) 대비 비용 {T('m')}"),
     ("table", (["Model · task (G0 peak context)", "G1", "G5", "GN", "G0F (real setup)"] if en else ["모델 · 과제 (G0 최대 컨텍스트)", "G1", "G5", "GN", "G0F (실제 설정)"]), cxrows),
     ("p", (f"Mean of {Cx['reps']} reps with a bootstrap 95% CI; below 1 is cheaper than full history. No compaction cell scored lower than G0. Sonnet T5 used a {p4['threshold_k']}K threshold. In the short pilot (1 rep), G2 cost {pl['G2']:.2f}× and single-action compaction (G3) {pl['G3']:.2f}×." if en
            else f"{Cx['reps']}회 반복 평균과 부트스트랩 95% 구간입니다. 1보다 작으면 전체 기록보다 쌉니다. 압축한 어느 셀도 G0보다 점수가 낮지 않았습니다. Sonnet T5는 기준점 {p4['threshold_k']}K를 썼습니다. 짧은 파일럿(반복 1회)에서 G2는 {pl['G2']:.2f}배, 행동 하나마다 압축(G3)은 {pl['G3']:.2f}배였습니다.")),
     ("h2", f"Why the saving does not carry over {T('j')}" if en else f"절감이 옮겨 오지 않는 이유 {T('j')}"),
     ("ul", ([f"<b>Cache writes dominate.</b> In Claude Code every new token is written to the cache once at {Cx['write_1h_multiplier']:.0f}× the input price, and old history is re-read at {Cx['read_multiplier']:.2f}×. A fit of the run costs puts cache writes at about {sh['cache_write'][0]}–{sh['cache_write'][1]}% of cost, reads about {sh['cache_read']}% and output {sh['output'][0]}–{sh['output'][1]}% (Sonnet and Opus). Compaction only removes reads, so its saving is capped near the read share, about {sh['cache_read']}%, and it adds a brief-writing call, more output and a rewrite of the prefix. In T5, reads fell {Cx['t5_reads_drop_pct']}% ({Cx['t5_reads_m'][0]}M → {Cx['t5_reads_m'][1]}M tokens) and cost fell only {Cx['t5_cost_drop_pct'][0]}–{Cx['t5_cost_drop_pct'][1]}%",
              f"<b>Prices are flat in context length.</b> NVIDIA's saving comes from a modelled price that rises with context. Sonnet and Opus 5.5 are priced flat. Haiku 5.5 is the exception: its price is {Cx['haiku_tier']['price_multiplier']}× higher above {Cx['haiku_tier']['above_k']}K tokens, and staying under that line is why G5 cost {hk3['G5'][0]:.2f}× on the 247K task",
              f"<b>Fixed overhead is paid on every call.</b> The author's real CLI setup raised the first call from {ov['first_call_k'][0]}K to {ov['first_call_k'][1]}K tokens and cost {s3['G0F'][0]:.2f}–{s4c['G0F'][0]:.2f}× the trimmed setup, with identical scores. The interactive session used during the study started at about {ov['desktop_call_k']}K tokens per call, {ov['desktop_mcp_k']}K of them MCP tool definitions"] if en else
             [f"<b>캐시 쓰기가 대부분입니다.</b> Claude Code에서는 새 토큰마다 입력 가격의 {Cx['write_1h_multiplier']:.0f}배로 캐시에 한 번 쓰고, 지난 기록은 {Cx['read_multiplier']:.2f}배로 다시 읽습니다. 실행 비용을 맞춰 보면 캐시 쓰기가 비용의 약 {sh['cache_write'][0]}~{sh['cache_write'][1]}%, 읽기가 약 {sh['cache_read']}%, 출력이 {sh['output'][0]}~{sh['output'][1]}%입니다(Sonnet·Opus). 압축은 읽기만 줄이므로 절감 상한은 읽기 몫인 약 {sh['cache_read']}% 근처이고, 거기에 요약을 쓰는 호출, 늘어난 출력, 프리픽스 재작성이 더해집니다. T5에서 읽기는 {Cx['t5_reads_drop_pct']}% 줄었지만({Cx['t5_reads_m'][0]}M → {Cx['t5_reads_m'][1]}M 토큰) 비용은 {Cx['t5_cost_drop_pct'][0]}~{Cx['t5_cost_drop_pct'][1]}%만 줄었습니다",
              f"<b>가격이 컨텍스트 길이와 무관합니다.</b> NVIDIA의 절감은 컨텍스트가 길수록 오르는 모형 가격에서 나옵니다. Sonnet·Opus 5.5는 가격이 일정합니다. 예외는 Haiku 5.5로, {Cx['haiku_tier']['above_k']}K 토큰을 넘으면 가격이 {Cx['haiku_tier']['price_multiplier']}배가 됩니다. 그 선 아래에 머문 덕분에 247K 과제에서 G5가 {hk3['G5'][0]:.2f}배였습니다",
              f"<b>고정 오버헤드는 호출마다 냅니다.</b> 저자의 실제 CLI 설정은 첫 호출을 {ov['first_call_k'][0]}K에서 {ov['first_call_k'][1]}K 토큰으로 늘렸고, 점수는 같은데 비용은 줄인 설정의 {s3['G0F'][0]:.2f}~{s4c['G0F'][0]:.2f}배였습니다. 연구 중에 쓴 대화형 세션은 호출마다 약 {ov['desktop_call_k']}K 토큰으로 시작했고, 그중 {ov['desktop_mcp_k']}K가 MCP 도구 정의였습니다"])),
     ("h2", f"Information loss and failures {T('m')}" if en else f"정보 손실과 실패 {T('m')}"),
     ("ul", (["No compaction-induced loss was seen in G1, G5 or GN across one or two compactions, including superseded facts (a port changed from 54329 to 54417, a cap from 37.5% to 35%), amended exclusion rules, buried requirements and exact numbers. Caveat: most runs scored at the ceiling, there were at most two compactions, and the tasks are synthetic",
              "Single-action compaction (G3) lost the reason a design had been rejected in 1 of 2 runs and cost 4–7× full history",
              "Haiku 5.5 failed the same feature checks with and without compaction: a capability limit, not a context effect",
              "A grader bug was found and fixed: Korean answers such as “9개” broke word-boundary matching of numbers"] if en else
             ["G1, G5, GN에서 한두 번의 압축으로 생긴 손실은 보이지 않았습니다. 바뀐 사실(포트 54329 → 54417, 상한 37.5% → 35%), 고친 제외 규칙, 묻힌 요구사항, 정확한 숫자까지 포함합니다. 단서: 대부분의 실행이 만점이었고, 압축은 최대 두 번이었으며, 과제는 합성입니다",
              "행동 하나마다 압축(G3)은 2회 중 1회에서 어떤 설계를 기각한 이유를 잃었고, 비용은 전체 기록의 4~7배였습니다",
              "Haiku 5.5는 압축 여부와 상관없이 같은 기능 검사에서 실패했습니다. 컨텍스트 효과가 아니라 능력의 한계입니다",
              "채점기 버그 하나를 찾아 고쳤습니다. “9개” 같은 한국어 답이 단어 경계 기반 숫자 매칭을 깨뜨렸습니다"])),
     ("h2", f"A pre-registered prediction, falsified {T('m')}" if en else f"반증된 사전등록 예측 {T('m')}"),
     ("p", (f"Phase 3 suggested that compaction pays off only when full history would exceed about {p4['threshold_k']}K tokens. Before Phase 4 this was written down as a prediction: on a longer task (T5, peak 235K), G5 and GN with a {p4['threshold_k']}K threshold would cost at most {p4['predicted_le']}× G0 with no quality loss, and the prediction would count as falsified if both cost at least {p4['falsified_if_ge']:.2f}×. Result: G5 {t5['G5'][0]:.2f}× and GN {t5['GN'][0]:.2f}×, with all {Cx['runs']['phase4']} runs at full score. <b>The prediction is falsified</b> for Sonnet 5.5." if en
            else f"3단계 결과는 전체 기록이 약 {p4['threshold_k']}K 토큰을 넘을 때만 압축이 이득이라고 시사했습니다. 4단계 전에 이를 예측으로 적었습니다. 더 긴 과제(T5, 최대 235K)에서 기준점 {p4['threshold_k']}K의 G5와 GN은 품질 손실 없이 G0의 {p4['predicted_le']}배 이하가 될 것이고, 둘 다 {p4['falsified_if_ge']:.2f}배 이상이면 반증으로 본다는 것입니다. 결과: G5 {t5['G5'][0]:.2f}배, GN {t5['GN'][0]:.2f}배였고 {Cx['runs']['phase4']}회 모두 만점이었습니다. Sonnet 5.5에 대해 <b>예측은 반증되었습니다</b>.")),
     ("h2", f"Recommendation: adopt with conditions {T('j')}" if en else f"권고: 조건부 채택 {T('j')}"),
     ("ul", ([f"Trim fixed overhead first: disable unused plugins, MCP servers and skills, and keep global instructions short. Measured: {ov['saving_pct'][0]}–{ov['saving_pct'][1]}% less cost for identical results",
              "Sonnet and Opus: do not compact mid-task to save usage. Start a fresh session at natural task boundaries when the old context is no longer needed (this follows from the mechanism and was not tested separately)",
              f"Haiku: keep sessions under {Cx['haiku_tier']['above_k']}K tokens, and compact with a structured brief at about 80K when work continues",
              "When compacting, use a structured brief (rules verbatim, exact values, decisions and rejected options, file paths) and keep the raw history retrievable. G5 and the built-in /compact cost the same; never compact after every action",
              f"Avoid long (over {p4['threshold_k']}K), subagent-heavy sessions for routine work; the author's own usage breakdown showed that most usage went there"] if en else
             [f"고정 오버헤드부터 줄입니다. 쓰지 않는 플러그인, MCP 서버, 스킬을 끄고 전역 지침을 짧게 둡니다. 실측: 같은 결과에 비용 {ov['saving_pct'][0]}~{ov['saving_pct'][1]}% 감소",
              "Sonnet·Opus: 사용량을 아끼려고 작업 중간에 압축하지 않습니다. 이전 컨텍스트가 더 필요 없으면 작업이 자연스럽게 끊기는 지점에서 새 세션을 시작합니다(메커니즘에서 나온 결론이며 따로 시험하지는 않았습니다)",
              f"Haiku: 세션을 {Cx['haiku_tier']['above_k']}K 토큰 아래로 유지하고, 작업이 이어지면 약 80K에서 구조화된 요약으로 압축합니다",
              "압축할 때는 구조화된 요약(규칙 원문, 정확한 값, 결정과 기각한 선택지, 파일 경로)을 쓰고 원본 기록을 다시 찾을 수 있게 둡니다. G5와 내장 /compact는 비용이 같습니다. 행동마다 압축하지는 않습니다",
              f"일상 작업에서는 {p4['threshold_k']}K를 넘는, 하위 에이전트를 많이 쓰는 긴 세션을 피합니다. 저자의 사용량 내역에서 사용량 대부분이 그런 세션에서 나왔습니다"])),
     ("h2", "Limitations" if en else "한계"),
     ("ul", ([f"Synthetic tasks only; the findings were not validated on a real workload",
              f"{Cx['reps']} reps per cell and wide confidence intervals on T4. Opus T3's {o3['G5'][0]:.2f}× has an interval that reaches {o3['G5'][2]:.2f}, so it is not significant",
              "Plan usage has a one-point resolution, so per-condition results rest on API-equivalent cost. How subscription plans weigh cached tokens is not disclosed; the roughly linear tracking is consistent with, but does not prove, cost-proportional accounting",
              "Thresholds were fixed, not adaptive, and there were at most two compactions per run, so compounding loss over many compactions is untested",
              "One Claude Code version and three models",
              "Novelty is limited: the cache-aware bound and the Haiku price-tier effect are useful practical findings, but CliffCompaction and TokenPilot cover similar ground. The project's own assessment is that this supports a short technical note, not a research paper"] if en else
             ["합성 과제만 썼고, 실제 작업에서는 검증하지 않았습니다",
              f"셀마다 {Cx['reps']}회 반복이며 T4의 신뢰구간이 넓습니다. Opus T3의 {o3['G5'][0]:.2f}배는 구간이 {o3['G5'][2]:.2f}까지 걸쳐 있어 유의하지 않습니다",
              "요금제 사용량은 1%p 단위라서 조건별 결과는 API 환산 비용에 기댑니다. 구독 요금제가 캐시 토큰을 어떤 비중으로 세는지는 공개되어 있지 않고, 대략 비례하는 움직임은 비용 비례 계산과 맞을 뿐 그것을 증명하지는 않습니다",
              "기준점은 고정값이었고 실행마다 압축은 최대 두 번이라, 여러 번 압축할 때 쌓이는 손실은 시험하지 않았습니다",
              "Claude Code 버전 하나, 모델 세 개",
              "신규성은 제한적입니다. 캐시를 고려한 상한과 Haiku 가격 구간 효과는 쓸모 있는 실용적 발견이지만, CliffCompaction과 TokenPilot이 비슷한 영역을 다룹니다. 프로젝트 스스로의 평가는 연구 논문이 아니라 짧은 기술 노트감이라는 것입니다"])),
     ("h2", "Verification and AI use" if en else "검증과 AI 활용"),
     ("p", ("The table figures were copied from the project's final report and its auto-generated Phase 3 analysis, which agree; the Phase 4 ratios were re-summed from the batch result files. The analysis was not otherwise re-run. AI-assisted implementation: an AI agent (Claude Code) built the harness, ran the experiments and wrote the analysis and report; the author set the question, approved the usage budget and chose the Phase 3 design. The models under test belong to the same family as the agent that ran the study. The literature review was web-based, and only the sources marked as checked above were confirmed against the original. Code and raw data are kept private. No independent review." if en
            else "표의 수치는 프로젝트 최종 보고서와 자동 생성된 3단계 분석 파일에서 옮겼고 둘은 일치합니다. 4단계 비율은 배치 결과 파일에서 다시 합산했습니다. 그 밖의 분석은 다시 돌리지 않았습니다. AI 보조 구현입니다. AI 에이전트(Claude Code)가 하네스를 만들고, 실험을 돌리고, 분석과 보고서를 썼으며, 저자는 질문을 정하고 사용량 예산을 승인하고 3단계 설계를 골랐습니다. 시험한 모델은 연구를 진행한 에이전트와 같은 계열입니다. 문헌 조사는 웹 기반이었고, 위에서 확인했다고 적은 출처만 원문과 대조했습니다. 코드와 원본 데이터는 비공개로 보관합니다. 독립적인 검토는 없습니다.")),
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
