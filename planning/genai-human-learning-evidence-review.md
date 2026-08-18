# Generative AI and Human Learning

> **Research record, not the active homework plan.** The course subsequently
> dropped the proposed Codex homework progression and adopted ten assignments.
> See `planning/homework-redesign-blueprint.md` for the current design.

## Evidence review for ME 539

**Search completed:** August 16, 2026<br>
**Population of primary interest:** graduate and advanced undergraduate learners, especially STEM and professional education<br>
**Decision in view:** whether and how to introduce Codex into weekly homework while preserving mathematical learning and trustworthy assessment

## Executive conclusion

The literature does **not** support the proposition that giving students unrestricted access to a general-purpose GenAI system improves durable human learning. It does support a narrower proposition:

> GenAI can support learning when the instructional design makes the student do the cognitively important work and uses the model as a constrained source of hints, feedback, alternatives, or implementation help.

The literature suggests the following **evidence-informed design hypothesis**. No study located tested this entire five-stage package as one intervention:

1. **Attempt, predict, derive, or self-evaluate before using AI.**
2. **Use AI for hints, critique, examples, or a candidate implementation rather than for the final answer.**
3. **Evaluate the AI output against an independent mathematical or empirical oracle.**
4. **Repair and explain the result.**
5. **Retrieve or transfer the idea later without AI.**

The distinction between assisted performance and learning is decisive. In several of the strongest experiments, AI improved the artifact or practice score but produced no advantage—and sometimes a disadvantage—when students later worked without AI. Conversely, the positive trials used substantial instructional engineering: instructor-verified solutions, staged questions, hint-first interaction, peer comparison, self-explanation, or structured reflection. Merely providing a course-grounded chatbot produced no detectable learning benefit in one semester-long randomized field experiment.

Graduate-specific causal evidence is sparse and inconclusive. It does not dispel the general concern about offloading, but it is insufficient to establish graduate-specific harm or protection. Positive results generally combine GenAI with other strong pedagogies, making the AI contribution impossible to isolate. There is currently no direct causal evidence that learning `AGENTS.md`, software harnesses, Codex skills, or dashboard generation improves mathematical or statistical understanding. Those are legitimate professional tool-use outcomes, but they should not be mistaken for proven learning mechanisms.

For ME 539, the evidence therefore favors keeping homework low stakes and formative, retaining controlled individual exams as the main certification evidence, and introducing Codex through a carefully scaffolded pilot rather than committing immediately to thirteen open-ended agent assignments.

## Scope and method

This is a broad, evidence-focused, non-exhaustive rapid review, not a registered systematic review. A formally exhaustive systematic review would require database exports, database-specific reproducible search strings, a preregistered protocol, duplicate screening and extraction, a screening flow log, author contact, and formal risk-of-bias adjudication. I did not manufacture PRISMA counts that this process cannot support.

The search covered peer-reviewed work available through August 16, 2026, using publisher indexes, PubMed, ERIC, Crossref/DOI searches, reference chaining, and targeted searches of major educational-technology and computing-education venues. Search concepts combined:

- generative AI, ChatGPT, large language model, AI tutor, AI coding assistant, GitHub Copilot, or Codex;
- learning, retention, transfer, knowledge, self-regulation, critical thinking, feedback, tutoring, assessment, or cognitive offloading;
- university, higher education, graduate, postgraduate, professional education, STEM, engineering, medicine, writing, or programming;
- randomized, controlled, experimental, quasi-experimental, meta-analysis, or systematic review.

The central efficacy synthesis includes peer-reviewed human-learning studies and systematic reviews. Preprints, vendor reports, anecdotes, perception-only surveys, and model benchmark studies were excluded from claims about learning efficacy. A few model-assessment studies are discussed separately because they establish that unsupervised products are no longer reliable evidence of authorship. Established pre-GenAI learning-science reviews were included only where they test the mechanisms used in the proposed design.

### Evidence hierarchy

The review weights outcomes in this order:

1. delayed, unaided retention or far-transfer tests;
2. immediate, unaided tests written independently of the intervention;
3. course examinations or concept tests administered without AI;
4. quality of revisions or products created while AI is available;
5. process measures and observed behavior;
6. self-reported learning, confidence, motivation, or satisfaction.

This hierarchy matters because a fluent AI-assisted product can improve while the learner's independent capability remains unchanged.

The confidence labels below are my evidence judgments, not formal GRADE ratings:

- **High:** multiple strong causal studies or a strong study plus convergent systematic evidence.
- **Moderate:** credible causal evidence, but limited by population, duration, outcome, or replication.
- **Low:** small, nonrandomized, self-reported, or indirect evidence.
- **Unproven:** no direct human-learning evidence located.

## What the meta-analyses show—and do not show

Recent meta-analyses consistently report positive mean effects, but their pooled outcomes mix human learning with assisted production, motivation, self-report, and researcher-created tests closely aligned to the intervention.

| Review | Scope | Pooled result | Main interpretive problem |
|---|---:|---:|---|
| [Chen & Cheung (2025)](https://doi.org/10.1016/j.edurev.2025.100737) | 57 university studies; 97 effects; 5,389 learners | Overall \(g=.804\); achievement \(g=.633\); higher-order thinking \(g=.580\); metacognition \(g=.078\), not significant | Very large language-learning effects, substantial heterogeneity, short studies, and mixed outcome types |
| [Han, Peng, & Liu (2025)](https://doi.org/10.1016/j.edurev.2025.100714) | 68 experimental/quasi-experimental studies; 337 effects | Overall SMD \(=.45\) | \(I^2\approx95\%\); larger effects in small, short, and precollege studies |
| [Deng et al. (2025)](https://doi.org/10.1016/j.compedu.2024.105224) | 69 studies reviewed; 62 entered at least one meta-analysis | Achievement \(g=.71\), \(k=51\); higher-order-thinking propensities \(g=.70\), \(k=15\); mental effort \(g=-.68\), \(k=4\) | Publication-bias signals for achievement and affective outcomes, underpowered studies, subjective measures, and frequent conflation of product quality with learning |
| [Fan et al. (2026)](https://doi.org/10.3389/fpsyg.2026.1758670) | 36 higher-education studies; 132 effects; 7,229 learners | Overall \(g=.499\) | 88/132 effects were self-rated; little long-duration evidence; no graduate subgroup |
| [Huang et al. (2026)](https://doi.org/10.3390/educsci16060816) | 36 studies of GenAI feedback; 4,538 learners for achievement | Achievement \(g=.61\) | \(I^2=86.3\%\); metacognition estimate came from only five effects; mixed publication types |
| [Kaliisa et al. (2026)](https://doi.org/10.1080/01443410.2025.2553639) | 41 published studies and 4,813 learners overall; posttest synthesis used 11 papers/12 studies | AI versus human posttest performance \(g=.25\), 95% CI \([-.11,.60]\), not significant | Only five studies involved GenAI; 33 involved language/writing; substantial heterogeneity |

These reviews overlap heavily in a young primary-study pool, so they are not six independent replications. The most defensible conclusion is that **well-designed GenAI-supported interventions can improve the outcomes being measured**, not that unrestricted AI improves durable learning by half a standard deviation.

## Strongest direct studies

### Studies that separate assisted performance from independent learning

| Study | Design | Assisted performance | Later or independent learning | Interpretation |
|---|---|---|---|---|
| [Bastani et al. (2025)](https://doi.org/10.1073/pnas.2422633122) | Preregistered field RCT; nearly 1,000 high-school mathematics students; unrestricted GPT, guarded tutor, or control | GPT Base +48%; guarded tutor +127% | GPT Base students scored 17% below control after AI removal; the guarded tutor largely eliminated the harm but did not clearly outperform control | Strong evidence that answer-giving can raise practice scores while reducing learning; the bundled guarded tutor mitigated the harm, but answer withholding was not isolated from verified solutions, common-error content, and other constraints |
| [Bassner et al. (2026)](https://doi.org/10.1016/j.caeai.2025.100537) | Three-arm RCT; 275 CS1 students; scaffolded Iris, unrestricted ChatGPT, or no AI | Both AI groups earned much higher exercise scores and less frustration | Neither AI group improved pre/post knowledge or code comprehension | Direct programming evidence that completion and conceptual learning dissociate |
| [Fan et al. (2025)](https://doi.org/10.1111/bjet.13544) | RCT; 117 university students; ChatGPT, human expert, analytics support, or no support | ChatGPT produced the largest essay improvement | No difference in knowledge gain or transfer; less learner orientation and self-evaluation | Product improvement did not become learning; process traces are consistent with metacognitive offloading |
| [Munsell et al. (2026)](https://doi.org/10.1080/15214842.2026.2659409) | Individually randomized experiment; 65 master's students, 58 quiz completers; ChatGPT as the primary resource with no class versus classroom instruction plus notes | Homework scores did not differ significantly | Traditional-instruction students scored .512 versus .405 on a later conceptual quiz, \(d=.57\); confidence was similar | Directly relevant graduate quantitative evidence, but the ChatGPT-instead-of-class bundle cannot isolate an AI effect from the loss of classroom instruction |
| [Kalam et al. (2025)](https://doi.org/10.7759/cureus.85767) | RCT; 33 first-year medical students; GPT-4, web resources, or institutional materials | GPT and web groups scored higher during the resource-assisted quiz | One week later, unaided retention did not differ significantly | Very underpowered, but again separates immediate performance from retention |
| [Çiçek et al. (2025)](https://doi.org/10.1093/postmj/qgae170) | RCT; 129 medical students; pregenerated ChatGPT or expert feedback | Both supported repeated practice | No significant overall difference on immediate or 10-day key-feature tests; experts were better for complex cases | AI feedback can supplement routine cases but was not superior to expert feedback |
| [Gustafsson et al. (2026)](https://doi.org/10.2196/79134) | Pilot randomized by team; 41 final-year medical students in trauma simulations | No improvement in decision accuracy or speed; some complex cases took longer | No four-week retention advantage; no-AI teams showed stronger confidence gains | Unstructured AI can disrupt collaborative reasoning |
| [Barcaui (2025)](https://doi.org/10.1016/j.ssaho.2025.102287) | RCT; 120 business students, 85 retained at surprise 45-day test | AI group studied for less time | ChatGPT 57.5% versus traditional 68.5%, \(d\approx.68\) | Suggestive harm to retention, but low confidence because of 29% attrition and weak fidelity monitoring |

### Studies showing that carefully engineered support can work

| Study | Design and result | What made the intervention different | Limits |
|---|---|---|---|
| [Kestin et al. (2025)](https://doi.org/10.1038/s41598-025-97652-6) | Randomized crossover; 194 Harvard introductory-physics students. Immediate unaided posttest effect about \(d=.63\), median 49 versus 60 minutes | Expert-authored solutions; staged questions; sequential scaffolding; videos; content-rich system prompt; feedback and self-pacing | Two lessons; immediate test; no delayed retention; months of platform development |
| [Lee et al. (2024)](https://doi.org/10.1186/s41239-024-00447-4) | RCT; 61 first-year chemistry students. Guided ChatGPT outperformed ordinary ChatGPT on posttest and week-15 delayed chemistry test | Students supplied their own answer first; AI supplied hints rather than answers; iterative refinement and logs | Single small course; no no-AI arm; several outcomes self-reported |
| [Li et al., InquiryGPT (2025)](https://doi.org/10.1177/07356331241289824) | Eight-week randomized comparison; 62 engineering students. Immediate scores were 77.6 versus 69.6; delayed means were 74.8 versus 68.2 | Predict–observe–explain–evaluate inquiry cycle rather than ordinary ChatGPT | Small, paired work, no no-AI arm, several self-reported higher-order outcomes; the published inferential statistics for the delayed effect are internally inconsistent, so delayed significance is uncertain |
| [Wu et al. (2025)](https://doi.org/10.1111/jcal.13085) | Eight-week RCT; 61 first-year engineering students. Structured peer-assessment GPT reported higher knowledge and self-reported higher-order outcomes than ordinary ChatGPT | Compare, assess, revise, and peer-evaluation cycle | Small, one course, no delayed transfer, many self-reported outcomes; conflicting reported F statistics and an impossible residual degree of freedom lower confidence pending correction |
| [Zheng, Shi, & Gao (2026)](https://doi.org/10.1016/j.compedu.2025.105489) | Two studies, 234 college learners. Expert-plus-assistant agents outperformed single-chatbot and traditional groups on immediate achievement and collaborative problem solving | Explicit complementary roles and structured collaborative process | Short-term outcomes; no delayed independent test; limited direct relevance to individual mathematical mastery |
| [Ateş (2026)](https://doi.org/10.1186/s41239-026-00614-9) | Multisite cluster RCT; 1,176 first-year science students. Reflective and hybrid feedback sequences outperformed direct AI on supervised delayed AI-free transfer | Criterion-based self-evaluation before AI critique; hybrid self/peer/AI sequence; justification of revisions | Very recent; treatment groups differed in structure and likely time on task; needs replication |
| [Pardos & Bhandari (2024)](https://doi.org/10.1371/journal.pone.0304013) | Randomized 3×4 study; 274 adults. ChatGPT hints yielded 17% gain, human hints 11.6%, no hints 1.9%; GPT and human not significantly different | Hints were screened and self-consistency checks were used | Crowdworkers, brief intervention, 30% attrition, no delayed transfer; raw AI hints failed quality checks on 32% of items |

Lee, InquiryGPT, and Wu share multiple authors, closely related ChatGPT/Apple-Shortcuts designs, and the same southern-Taiwan research ecosystem. They should be treated as one related research program, not three independent replications; this matters especially because two of the papers contain statistical inconsistencies.

### Studies showing that access or grounding alone is insufficient

| Study | Design and result | Implication |
|---|---|---|
| [Thoeni & Fryer (2026)](https://doi.org/10.1016/j.chbr.2026.101061) | Semester-long randomized field experiment with 454 in-person and asynchronous undergraduates; a course-grounded RAG chatbot produced no statistically detectable effect on achievement, interest, self-efficacy, or engagement | In this introductory-marketing implementation, grounding and availability alone were insufficient to produce detectable gains; use was shallow |
| [Nie et al. (2025)](https://doi.org/10.1145/3698205.3733960) | Randomized offer of a course GPT to 5,831 learners; only 14.2% adopted it; no intention-to-treat exam-score effect; exam participation fell 4.3 percentage points. An instrumental-variable estimate suggested a 6.8-point benefit among compliers under strong assumptions | Optional availability produces low, selective adoption; the full pattern is compatible with a benefit for some adopters but does not establish a population-wide learning gain |
| [Brender et al. (2026; first online 2025)](https://doi.org/10.1007/978-3-032-03870-8_7) | 58 graduate robotics students; structured prompting versus ordinary ChatGPT across two labs and a transfer lab; no performance or learning difference, and prompted behavior did not persist | A prompting interface is not enough to create durable learning habits |
| [Avello-Martínez et al. (2024)](https://doi.org/10.6018/red.604621) | RCT; 41 master's students in digital storytelling; no significant short-term skill advantage, though germane cognitive load decreased | Efficiency or lower effort does not necessarily mean better skill acquisition |
| [Farrokhnia et al. (2026)](https://doi.org/10.1186/s41239-026-00579-9) | RCT; 70 educational-sciences students; teacher, zero-shot AI, or chain-of-thought AI feedback. Elaborate prompting improved feedback quality but not revised essay quality | The article is internally inconsistent about level: its abstract/limitations say graduate, while Methods says third-year bachelor's. It is not counted below as confirmed graduate evidence |

## Graduate-level evidence

Graduate-specific experimental evidence is sparse and inconclusive. The most relevant studies are:

- **Graduate quantitative/professional learning:** the master's finance experiment found lower conceptual quiz scores in the ChatGPT-instead-of-class condition despite similar homework and confidence; this bundled substitution cannot identify whether AI, missing classroom instruction, or both caused the difference.
- **Graduate robotics:** structured prompting produced no learning advantage and did not transfer after the prompt scaffold was removed. Exploratory prompt-log associations linked clarity/understanding patterns with gains; they did not causally establish conceptual prompts as superior to debugging or implementation requests.
- **Graduate digital storytelling:** ChatGPT reduced some cognitive load but did not improve the measured skill.
- **Graduate online-learning discussions:** a 16-week randomized study of 63 graduate students reported improved engagement and higher-order-thinking measures with ChatGPT-enhanced messaging, but the outcomes were largely scales and content analyses rather than delayed independent subject tests ([Huang et al., 2025](https://doi.org/10.1016/j.chb.2025.108659)).
- **Postgraduate dental research methods:** a nonrandomized, bundled intervention combining flipped instruction, peer critique, active tasks, faculty discussion, and AI feedback increased satisfaction, but performance differences were not significant ([Natto, 2026](https://doi.org/10.1186/s12909-026-08576-2)).

The graduate evidence does not dispel the general caution: advanced students are not demonstrably protected from offloading, overconfidence, or shallow implementation work. It is insufficient, however, to establish graduate-specific harm or protection.

## Mechanisms that have the best support

### 1. Generate before receiving

This is the most plausible and transferable design principle, but the direct GenAI studies test bundled instructional designs rather than isolating a single ingredient.

- The guarded tutor in Bastani et al. withheld direct answers and mitigated the learning harm of unrestricted GPT, while also bundling verified solutions, common-error content, and other constraints.
- Lee et al. required an initial student response before hints and found better posttest and delayed performance than ordinary ChatGPT.
- InquiryGPT used prediction, observation, explanation, and evaluation.
- A pre-GenAI meta-analysis of 53 productive-failure studies found that problem solving before instruction improved conceptual and transfer outcomes, \(g=.36\) ([Sinha & Kapur, 2021](https://doi.org/10.3102/00346543211019105)).

**Confidence: moderate** from direct GenAI studies and **high** from indirect pre-GenAI learning science that generation before instruction is preferable to immediate answer access; **moderate** that this exact implementation will improve graduate mathematical learning in this course.

### 2. Require self-explanation and falsifiable checks

Self-explanation has a stronger evidence base than generic reflection. A meta-analysis of 69 effects and about 5,900 learners found induced self-explanation improved learning by \(g=.55\), remaining \(g=.41\) in time-matched comparisons ([Bisra et al., 2018](https://doi.org/10.1007/s10648-018-9434-x)).

For ME 539, useful prompts are domain-specific:

- What result do you predict before running the code?
- What assumption is required for this derivation?
- Which limiting case would falsify the result?
- What invariant, normalization condition, unit check, or analytic special case acts as an oracle?
- Why does this test distinguish the correct model from a plausible wrong one?

A polished after-the-fact “reflection on AI use” is weaker because it can be generated by the same system and does not prove that verification occurred.

**Confidence: high** for self-explanation generally; **moderate** for the GenAI-specific implementation.

### 3. Use adaptive, task-specific prompts rather than prompt tricks

Pre-GenAI prompt syntheses find modest benefits from task-specific and action-oriented metacognitive prompts: roughly \(g=.40\) for learning in one review and bias-adjusted \(d=.22\) in another ([Guo, 2022](https://doi.org/10.1111/jcal.12650); [Thomann & Deutscher, 2025](https://doi.org/10.1016/j.edurev.2025.100686)).

The educational purpose of a prompt should be to cause a learner action—predict, compare, test, explain—not simply to elicit a more impressive answer.

**Confidence: moderate.**

### 4. Return to the idea later without AI

The testing effect is robust. A meta-analysis of 222 classroom studies, 573 effects, and 48,478 learners found retrieval practice improved learning by \(g=.499\) ([Yang et al., 2021](https://doi.org/10.1037/bul0000309)). A higher-education causal review likewise identified low-stakes quizzing as one of the most promising approaches ([Morris, Perry, & Wardle, 2021](https://doi.org/10.1002/rev3.3292)).

Every important AI-supported concept should therefore reappear later in a short AI-free quiz or exam item that changes the surface details while preserving the reasoning.

**Confidence: high** for retrieval practice; **moderate** for the exact spacing and item format in this course.

### 5. Make students process feedback

Feedback is heterogeneous. A synthesis of 435 studies found a mean effect around \(d=.48\), but effects depended strongly on information content ([Wisniewski, Zierer, & Hattie, 2020](https://doi.org/10.3389/fpsyg.2019.03087)). In the classic feedback meta-analysis, more than one-third of interventions worsened performance ([Kluger & DeNisi, 1996](https://doi.org/10.1037/0033-2909.119.2.254)).

As a course-design hypothesis, students can classify important AI suggestions as **accept, modify, or reject**, and justify at least one decision with mathematical evidence. The literature establishes that feedback content and learner processing matter; it does not directly establish this particular classification routine.

**Confidence: high** for the importance of feedback content and learner processing; **low to moderate** for this particular implementation.

### 6. Add cognitive forcing, not just a warning

Simple warnings that AI can make mistakes are not sufficient on their own. In one randomized medical task, a “ChatGPT can make mistakes” warning did not change whether 186 students revised an initial diagnosis after conflicting ChatGPT-attributed advice ([Kıyak, Coşkun, & Budakoğlu, 2026](https://doi.org/10.1111/medu.70056)). Related human-AI decision studies show that forcing a person to form an answer or request advice can reduce acceptance of incorrect recommendations, though friction is often disliked ([Buçinca, Malaya, & Gajos, 2021](https://doi.org/10.1145/3449287)).

The relevant control is an independent oracle created before the model output is visible—not a disclaimer.

**Confidence: moderate.**

### 7. Combine complementary human and AI roles

A preregistered meta-analysis of 106 human–AI experiments found that teams beat humans alone but performed worse than the better of human or AI alone on average ([Vaccaro, Almaatouq, & Malone, 2024](https://doi.org/10.1038/s41562-024-02024-1)). Human–AI collaboration is therefore not automatically synergistic.

Productive role division is more plausible when the human owns the model assumptions, derivation, acceptance criteria, and final justification while the AI supplies candidate implementations, counterexamples, or alternatives.

**Confidence: moderate** for complementary roles; **low** for any particular group-work recipe.

## AI literacy can be taught, but it is not disciplinary mastery

The strongest direct AI-literacy experiment randomized 65 course sections containing 1,368 undergraduate and graduate students. A 90-minute asynchronous module with instruction, practice, and feedback improved GenAI knowledge, prompt engineering, fact/source checking, and self-efficacy. It did **not** improve bias evaluation ([Connell Pensky et al., 2026](https://doi.org/10.1016/j.compedu.2026.105640)).

This supports a short common onboarding module before required Codex work. It does not show that prompting or fact-checking skills transfer to Bayesian reasoning, Monte Carlo analysis, or code verification. Domain-specific judgment must be practiced repeatedly.

## What the evidence says about the proposed Codex topics

| Proposed topic | Direct evidence that it improves subject learning | Defensible role in the course |
|---|---|---|
| Basic Codex operation and task framing | Limited AI-literacy RCT evidence | Teach briefly so access and interface skill do not confound the assignment |
| `AGENTS.md` | None located | Professional configuration skill; use it to encode scope, environment, and test boundaries, not as a learning intervention |
| A software harness | No Codex-specific learning evidence; strong indirect evidence for tests, feedback, and explicit criteria | Make verification executable and grading scalable; the student must still understand and author at least one oracle |
| Codex skills | None located | Reusable professional workflow; introduce only after students understand the underlying verification sequence |
| Interactive dashboards | No evidence that dashboard generation improves mathematical learning | Useful for exploration and communication if students must predict and interpret quantitative behavior; a convincing plot is not validation |
| Agent-generated tests | No evidence that tests generated from the same model supply independent verification | Do not accept as the sole oracle; require a human-derived property, analytic case, or instructor-hidden test |
| Prompt engineering | Evidence that basic prompting can be taught; little causal evidence of transfer to subject mastery | Keep it subordinate to task decomposition, verification, and mathematical judgment |
| Long AI-use reflections or chat transcripts | Little evidence; easily generated and expensive to grade | Do not grade. Use a short verification card tied to observable evidence |

The closest peer-reviewed coding-assistant evidence finds productivity gains but weak or absent learning gains. A ten-student fixed-order within-subjects study found GitHub Copilot made brownfield tasks 35% faster and increased progress by 50%, while students worried that they did not understand the suggestions; all students used Copilot second, so practice and order effects favor the tool, and the study remains productivity rather than learning evidence ([Shihab et al., 2025](https://doi.org/10.1145/3702652.3744219)). In two controlled studies of cognitive friction in generated code, Lead-and-Reveal showed the strongest alignment between perceived and actual ability, but a direct between-condition calibration effect was not established and later unaided coding did not differ significantly ([Kazemitabaar et al., 2025](https://doi.org/10.1145/3708359.3712104)).

## Assessment in the presence of GenAI

### Homework should be practice, not certification

The established evidence supports low-stakes quizzing, repeated retrieval, and feedback. GenAI-era studies show that homework or artifact quality can become disconnected from independent competence. Given ME 539's scale, staffing, modalities, and exam plan, keeping homework at 10% is a defensible course-specific choice—not a literature-derived optimum—provided homework is designed for practice and feedback rather than interpreted as a clean measure of mastery.

Homework can still be valuable if it:

- has a fixed weekly cadence;
- gives rapid feedback;
- uses retries or correction where appropriate;
- requires manual setup, prediction, or derivation;
- includes a bounded AI role;
- returns to key ideas later without AI;
- and makes verification criteria visible.

### Controlled individual assessment is a strong scalable certification method here

Engineering assessment studies show that current models can pass many numerical, programming, selected-response, and written tasks. In one broad STEM benchmark, GPT-4 passed most represented courses under a 50% threshold, including open-response work ([Borges et al., 2024](https://doi.org/10.1073/pnas.2414955121)). In a live university examination system, 94% of fully GPT-4-generated submissions escaped any concern flag ([Scarfe et al., 2024](https://doi.org/10.1371/journal.pone.0305354)). These are vulnerability studies rather than learning studies, but they show why authenticity alone does not establish authorship. Controlled individual assessments are the most direct evidence of what each student can do independently.

For ME 539's enrollment, modalities, staffing, and room constraints, the current three one-hour, noncomprehensive exams are a defensible course-specific design judgment. The literature does not dictate three exams or the exact 90%/10% weighting. A scoping review finds weak justification for making a single final overwhelmingly dominant and identifies anxiety, equity, and validity concerns; distributing certification over several assessments is preferable to a single all-or-nothing event ([French, Dickerson, & Mulder, 2024](https://doi.org/10.1007/s10734-023-01148-z)).

Each exam should include one or more **transfer probes** from prior AI-supported homework: a changed parameterization, a wrong derivation to diagnose, a limiting case, a required assumption, or a test-selection question. This is the course’s evidence that the AI-supported activity became human knowledge.

### Authentic projects and peer work are learning tools, not authorship guarantees

Authentic assessment reviews report benefits for problem solving, collaboration, reflection, and employability, but the evidence is heterogeneous and largely observational ([Vlachopoulos & Makri, 2024](https://doi.org/10.1016/j.stueduc.2024.101425)). Peer feedback is most useful formatively when students receive training, criteria, and repeated opportunities to apply it ([Fleckney, Thompson, & Vaz-Serra, 2024](https://doi.org/10.1080/07294360.2024.2407083)). Neither a project nor a process log establishes individual mastery without an individual check.

### AI detectors should not determine grades

Known-origin evaluations show substantial false positives, false negatives, bias, and rapid performance drift; simple adversarial modification substantially reduced detection in one seven-detector evaluation ([Perkins et al., 2024](https://doi.org/10.1186/s41239-024-00487-w)). Detector output can at most trigger a broader human review; it should not determine a grade or misconduct finding.

## Implications for the ME 539 homework plan

### What I would retain

- Homework remains 10% and primarily formative as a course-specific judgment, not a literature-derived optimum.
- Manual mathematics remains the majority of each assignment.
- At most one bounded Codex problem appears on a homework.
- Students learn to verify software against mathematics rather than trust a polished notebook.
- By approximately Homework 4, students may undertake a nontrivial agent-assisted computational task.

### What I would change before committing

1. **Add a common 60–90 minute AI-literacy onboarding before the first graded Codex task.** It should include practice and feedback, not only policy text. It should teach task framing, fact/source checks, privacy, model fallibility, and the distinction between performance and learning.
2. **Use faded scaffolding.** Homework 1 uses a fully instructor-provided environment and a seeded faulty output. Homework 2 introduces a concise `AGENTS.md` inside an instructor-provided harness. Homework 3 asks students to author one mathematical oracle or extend one test. Homework 4 combines the pieces in a nontrivial task.
3. **Protect the oracle.** Codex must not edit locked instructor tests. At least one graded verification criterion must originate from the student before AI output is viewed. Hidden tests should check edge cases, but hidden tests alone do not prove understanding.
4. **Replace long reflections with a short verification card.** Require: initial prediction, decisive test, discrepancy found, repair, and why the final result is credible. Cap at roughly 150–200 words plus equations/evidence.
5. **Schedule delayed AI-free transfer.** Put one concept-equivalent item on the next quiz or exam. This is essential; without it, we would only know whether students produced a good artifact with Codex.
6. **Do not require a fabricated failure.** Either seed a real defect or grade the quality of an attempted falsification even when the candidate passes.
7. **Treat `AGENTS.md`, harnesses, skills, and dashboards as explicit professional-learning outcomes.** Do not claim they improve probability or inference learning unless the transfer evidence shows that they do.
8. **Pilot before scaling to all thirteen homeworks.** The strongest defensible initial commitment is the first four assignments plus predeclared evaluation criteria, followed by a decision using exam transfer performance, support burden, completion time, and equity data.

### A defensible first-four-homework progression

| Homework | Human work before Codex | Codex role | Verification evidence | Later transfer |
|---|---|---|---|---|
| 1 | Hand-derived probability/RV result and predicted output | Critique a seeded candidate solution or implementation | Normalization, exact moment, limiting case, and one repaired claim | Short independent probability item |
| 2 | Joint-distribution identities and expected covariance behavior | Work inside a provided harness governed by a short local `AGENTS.md` | Marginals, covariance symmetry/PSD, linear-transform identity, singular edge case | Changed joint PMF/covariance diagnosis |
| 3 | Derive Monte Carlo target, variance convention, and expected \(N^{-1/2}\) scaling | Implement to a fixed interface; student authors or extends one oracle | Seeded aggregate tests, analytic benchmark, nonflaky tolerance rationale | Select/justify an MC diagnostic without code |
| 4 | Predict an uncertainty-propagation result and confidence-interval behavior | Complete an end-to-end bounded experiment using the existing harness | Hidden parameters, coverage check, convergence behavior, and concise audit | Diagnose an erroneous uncertainty statement |

This progression is evidence-informed, not yet evidence-proven. It should remain provisional until the course’s own transfer data are available.

## How to evaluate the pilot without disadvantaging students

Predeclare four outcomes:

1. **Independent learning:** performance on concept-equivalent exam items, not homework score.
2. **Verification quality:** whether students can specify a valid oracle, detect a seeded error, and explain the repair.
3. **Operational cost:** median student time, help requests, TA exception time, and environment failures.
4. **Equity and access:** completion and transfer by modality, prior coding experience, and access needs.

Useful low-risk comparisons include item-level analysis against non-Codex topics, within-student transfer probes, and randomized problem parameters. Do not withhold essential instruction from a control group. If stronger causal evaluation is desired, use a crossover of two equivalent topics so all students eventually receive both formats.

### Continue the Codex progression only if

- students can execute the starter environment reliably;
- the Codex task does not crowd out the manual mathematics;
- transfer-item performance is at least comparable to matched conventional homework topics;
- students can identify and justify valid mathematical checks;
- TA exception handling remains sustainable for 160 students;
- and access or prior coding experience does not create an unacceptable performance gap.

If those gates fail, keep Codex as an optional professional-skills activity or concentrate it in fewer, better-supported assignments.

## Confidence summary

| Claim | Confidence |
|---|---|
| Unrestricted GenAI often improves assisted production without reliably improving human learning | **High** |
| Independent, unaided assessment is necessary to distinguish learning from assisted performance | **High** |
| The attempt-first, constrained-support, self-explanation, and later-retrieval package is preferable to immediate answer access | **Moderate as a GenAI design hypothesis; stronger indirect support for its individual components** |
| A carefully engineered, curriculum-grounded AI tutor can improve immediate learning | **Moderate** |
| Course grounding alone reliably improves learning | **Unsupported; one strong field implementation found no detectable effect** |
| A short module can improve basic AI knowledge, prompting, and fact/source checking | **Moderate** |
| Prompt literacy transfers to mathematical competence | **Low** |
| Critiquing AI output automatically develops critical thinking | **Low unless coupled to prior knowledge, explicit criteria, and independent checks** |
| `AGENTS.md`, harnesses, skills, or dashboards improve disciplinary learning | **Unproven** |
| Authentic projects or process logs establish individual authorship | **Low** |
| AI detectors can safely determine misconduct | **Contradicted by current evidence** |
| The same effects generalize to a 160-student graduate predictive-modeling course | **Low to moderate; direct graduate STEM evidence is sparse** |

## Decision recommendation

Do **not** finalize thirteen Codex problems yet. Retain the manual-first Homework 1–3 drafts as drafts, revise them to follow the attempt–hint/implementation–verify–transfer sequence, and design Homework 4 as the first integrated task. Pilot those four with a common onboarding module and explicit exit gates. Commit to later topics—skills, dashboards, multiagent workflows—only after the pilot demonstrates both independent learning and manageable operational cost.

This is not an argument against teaching Codex. It is an argument for teaching it as a professional instrument under mathematical control, while measuring whether students—not only their notebooks—improve.

## Core references

### Direct GenAI learning evidence

- [Ateş (2026), reflective and hybrid AI-feedback sequences](https://doi.org/10.1186/s41239-026-00614-9)
- [Avello-Martínez, Gajderowicz, & Gómez-Rodríguez (2024), graduate digital storytelling](https://doi.org/10.6018/red.604621)
- [Barcaui (2025), delayed retention](https://doi.org/10.1016/j.ssaho.2025.102287)
- [Bassner et al. (2026), programming performance versus learning](https://doi.org/10.1016/j.caeai.2025.100537)
- [Bastani et al. (2025), guarded versus unguarded math tutor](https://doi.org/10.1073/pnas.2422633122)
- [Brender et al. (2026; first online 2025), structured prompts in graduate robotics](https://doi.org/10.1007/978-3-032-03870-8_7)
- [Çiçek et al. (2025), ChatGPT versus expert clinical-reasoning feedback](https://doi.org/10.1093/postmj/qgae170)
- [Fan et al. (2025), metacognitive laziness](https://doi.org/10.1111/bjet.13544)
- [Farrokhnia et al. (2026), AI versus teacher feedback; participant level reported inconsistently](https://doi.org/10.1186/s41239-026-00579-9)
- [Gustafsson et al. (2026), trauma simulation and retention](https://doi.org/10.2196/79134)
- [Huang et al. (2025), graduate ChatGPT-enhanced messaging](https://doi.org/10.1016/j.chb.2025.108659)
- [Kalam et al. (2025), medical-student retention](https://doi.org/10.7759/cureus.85767)
- [Kestin et al. (2025), structured physics tutor](https://doi.org/10.1038/s41598-025-97652-6)
- [Lee et al. (2024), guidance mechanism in chemistry](https://doi.org/10.1186/s41239-024-00447-4)
- [Li et al. (2025), InquiryGPT](https://doi.org/10.1177/07356331241289824)
- [Munsell et al. (2026), graduate real-estate finance](https://doi.org/10.1080/15214842.2026.2659409)
- [Nie et al. (2025), large programming-course GPT deployment](https://doi.org/10.1145/3698205.3733960)
- [Pardos & Bhandari (2024), screened ChatGPT math hints](https://doi.org/10.1371/journal.pone.0304013)
- [Thoeni & Fryer (2026), RAG chatbot field experiment](https://doi.org/10.1016/j.chbr.2026.101061)
- [Wu et al. (2025), peer-assessment-cycle GPT in engineering](https://doi.org/10.1111/jcal.13085)
- [Zheng, Shi, & Gao (2026), structured multiagent collaborative learning](https://doi.org/10.1016/j.compedu.2025.105489)

### Reviews and adjacent learning science

- [Chen & Cheung (2025), university GenAI meta-analysis](https://doi.org/10.1016/j.edurev.2025.100737)
- [Deng et al. (2025), experimental ChatGPT meta-analysis](https://doi.org/10.1016/j.compedu.2024.105224)
- [Han, Peng, & Liu (2025), GenAI experimental meta-analysis](https://doi.org/10.1016/j.edurev.2025.100714)
- [Fan et al. (2026), three-level higher-education meta-analysis](https://doi.org/10.3389/fpsyg.2026.1758670)
- [Connell Pensky et al. (2026), GenAI competency-module cluster RCT](https://doi.org/10.1016/j.compedu.2026.105640)
- [Bisra et al. (2018), self-explanation meta-analysis](https://doi.org/10.1007/s10648-018-9434-x)
- [Sinha & Kapur (2021), productive-failure meta-analysis](https://doi.org/10.3102/00346543211019105)
- [Yang et al. (2021), classroom retrieval-practice meta-analysis](https://doi.org/10.1037/bul0000309)
- [Morris, Perry, & Wardle (2021), formative assessment in higher education](https://doi.org/10.1002/rev3.3292)
- [Vlachopoulos & Makri (2024), authentic-assessment systematic review](https://doi.org/10.1016/j.stueduc.2024.101425)
- [Fleckney, Thompson, & Vaz-Serra (2024), peer-assessment systematic review](https://doi.org/10.1080/07294360.2024.2407083)
- [French, Dickerson, & Mulder (2024), high-stakes-exam scoping review](https://doi.org/10.1007/s10734-023-01148-z)
- [Vaccaro, Almaatouq, & Malone (2024), human–AI collaboration meta-analysis](https://doi.org/10.1038/s41562-024-02024-1)
