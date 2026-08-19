"""Build the full ChildEsc collaboration manuscript as a DOCX."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "paper" / "ChildEsc_Workshop_Paper.docx"


def set_font(run, name: str = "Times New Roman", size: float = 10, bold=False, italic=False):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic


def set_paragraph_spacing(paragraph, before=0, after=5.5, line=11):
    fmt = paragraph.paragraph_format
    fmt.space_before = Pt(before)
    fmt.space_after = Pt(after)
    fmt.line_spacing = Pt(line)


def set_cell_shading(cell, fill: str):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=60, start=80, bottom=60, end=80):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_table_borders(table):
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "insideH", "bottom"):
        node = OxmlElement(f"w:{edge}")
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), "6" if edge != "insideH" else "2")
        node.set(qn("w:color"), "333333" if edge != "insideH" else "B7B7B7")
        borders.append(node)
    for edge in ("left", "right", "insideV"):
        node = OxmlElement(f"w:{edge}")
        node.set(qn("w:val"), "nil")
        borders.append(node)


def mark_table_header(row):
    row_pr = row._tr.get_or_add_trPr()
    header = OxmlElement("w:tblHeader")
    header.set(qn("w:val"), "true")
    row_pr.append(header)


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend((begin, instr, end))
    set_font(run, size=9)


def add_body(
    doc,
    text: str,
    bold_lead: str | None = None,
    *,
    size: float = 10,
    after: float = 5.5,
    line: float = 11,
):
    paragraph = doc.add_paragraph()
    if bold_lead:
        lead = paragraph.add_run(bold_lead)
        set_font(lead, size=size, bold=True)
    run = paragraph.add_run(text)
    set_font(run, size=size)
    set_paragraph_spacing(paragraph, after=after, line=line)
    return paragraph


def add_heading(doc, text: str, level: int = 1):
    paragraph = doc.add_paragraph(style=f"Heading {level}")
    run = paragraph.add_run(text)
    set_font(run, size=12 if level == 1 else 10, bold=True)
    paragraph.paragraph_format.keep_with_next = True
    set_paragraph_spacing(paragraph, before=8 if level == 1 else 5.5, after=3, line=12)
    return paragraph


def add_reference(doc, text: str):
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.left_indent = Inches(0.18)
    paragraph.paragraph_format.first_line_indent = Inches(-0.18)
    run = paragraph.add_run(text)
    set_font(run, size=8.5)
    set_paragraph_spacing(paragraph, after=2, line=9)


def build() -> Path:
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1.5)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    normal.font.size = Pt(10)
    normal.paragraph_format.space_after = Pt(5.5)
    normal.paragraph_format.line_spacing = Pt(11)

    for name, size in (("Heading 1", 12), ("Heading 2", 10)):
        style = doc.styles[name]
        style.font.name = "Times New Roman"
        style._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0, 0, 0)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_before = Pt(18)
    title.paragraph_format.space_after = Pt(18)
    title_run = title.add_run(
        "Who Is Safe to Involve? ChildEsc Audits Escalation and Handoff Routing in Child-Facing AI"
    )
    set_font(title_run, size=17, bold=True)
    p_pr = title._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    for edge, size in (("top", "32"), ("bottom", "8")):
        node = OxmlElement(f"w:{edge}")
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), size)
        node.set(qn("w:space"), "8")
        node.set(qn("w:color"), "000000")
        borders.append(node)
    p_pr.append(borders)

    author = doc.add_paragraph()
    author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(author, after=11)
    set_font(author.add_run("Anonymous Author(s)"), bold=True)

    abstract_heading = doc.add_paragraph()
    abstract_heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(abstract_heading, before=11, after=5.5, line=12)
    set_font(abstract_heading.add_run("Abstract"), size=12, bold=True)
    abstract = doc.add_paragraph()
    abstract.paragraph_format.left_indent = Inches(0.5)
    abstract.paragraph_format.right_indent = Inches(0.5)
    set_paragraph_spacing(abstract, after=11)
    abstract_text = (
        "Child-facing AI must decide not only whether to escalate, but who is safe to involve. Action-only evaluation can reward "
        "the right urgency while directing a child toward an inappropriate recipient. ChildEsc is a works-in-progress testbed of "
        "80 LLM-assisted synthetic conversations in 20 counterfactual families. Each item specifies one of four actions plus "
        "permitted and forbidden handoff targets. We define the action-route gap: exact action accuracy minus exact action-plus-target "
        "routing. A policy-exposed checksum achieves 65.0% action accuracy but 53.8% exact routing, an 11.3% gap; 9/37 action-correct "
        "handoffs violate target constraints. A frozen relational contract audit passes 36/39 assertions across 7/9 families. We "
        "provide a provider-neutral, cache-replayable protocol but report no live-model comparison because frozen credentials were "
        "unavailable. ChildEsc is not a validated benchmark: practitioner and youth validation have not occurred, and no result "
        "supports deployment."
    )
    set_font(abstract.add_run(abstract_text))

    add_heading(doc, "1 Introduction")
    add_body(doc, "Children use conversational AI for information, companionship, and emotional support, where a superficially safe response can still worsen a vulnerable situation (UNICEF, 2026; Cha et al., 2026). Binary respond/refuse policies are especially ill-suited to these interactions: refusal can close a rare help-seeking window, while unbounded engagement can reinforce dependency or miss imminent danger. Interviews with 19 youth-facing practitioners found that useful systems should gather context and bridge youth to tailored human support, but should not assume a parent is safe (Cha et al., 2026). The deployment decision is therefore not simply \"is this content allowed?\" but what support action is proportionate now, and who is safe to involve?")
    add_body(doc, "Related benchmarks cover important parts of this problem. MinorBench and Safe-Child-LLM emphasize unsafe-request handling; KIDBench evaluates developmental response quality and trusted-adult redirection; CAREBench includes crisis referral and human-support behavior; and MindEval measures multi-turn adult mental-health support. CARE-Bench recently operationalized patient-facing medical triage as a four-label sequential current-action task, including whether more information is needed. Thus neither ordered routing nor action timing is our novelty. ChildEsc instead isolates child-specific severity-matched trajectories and explicit permitted and forbidden handoff sets. This maps directly to the workshop's restricted-data evaluation and deployment-safeguard themes.")
    add_body(doc, "We contribute: (1) a proposed four-action, context-constrained handoff specification instantiated as 80 synthetic trajectories; (2) metrics that separate escalation threshold errors from target-safety errors; and (3) a reproducible checksum, source-to-design register, and concrete validation protocol. We do not claim benchmark validity, child-centeredness, or system superiority before independent review.")

    add_heading(doc, "2 ChildEsc testbed")
    add_body(doc, "ChildEsc applies to text-based consumer assistants, companions, tutors, and wellness or mental-health-adjacent systems used by or accessible to people under 18. It evaluates an application-layer router before or alongside response generation. It does not diagnose, recommend treatment, or automatically contact any person or service.", "Scope. ")
    add_body(doc, "Under a written specification, an LLM coding assistant drafted 20 scenario families across eight vulnerability domains. Each family contains a shared context and four severity cues, expanded deterministically into three-user-turn conversations. No text derives from a real child, hotline transcript, clinical record, or explicit abuse material. A dated register maps domain-level rationales to public sources, but this retrospective mapping is source-informed rather than item-level grounding. The same workflow drafted labels and rules, making all results policy-exposed and unsuitable for estimating generalization.", "Construction and provenance. ")
    add_body(doc, "The ordinal action space is continue_support (0), boundary_redirect (1), human_support (2), and urgent_handoff (3). Escalated items permit one or more target classes. Forbidden targets use the same vocabulary a router can emit; safe_adult is forbidden when the conversation implicates an adult, while safe_adult_not_implicated may be permitted.", "Actions and targets. ")
    add_body(doc, "Under-escalation is conditioned on the 58 items requiring human or urgent support. Strict target validity requires a nonempty predicted set that is a subset of permitted targets and contains no forbidden target; targetless actions must emit none. Exact routing requires the exact action and a valid target decision. The action-route gap is action accuracy minus exact-route accuracy. Reaction delay is omitted because v0.1 fixes the decisive cue turn.", "Failure-oriented metrics. ")

    add_heading(doc, "3 Diagnostic implementation and audit")
    add_body(doc, "Keyword, Agnostic, and ChildEsc-Rules are policy-exposed checksum policies. A provider-neutral harness sends only conversation text and requests the same action-target schema from Gemini, OpenAI, Anthropic, or OpenRouter. It supports independent trial IDs, append-only logs, strict parsing, and cache-only replay; invalid outputs make a run incomplete. No live provider result is reported because credentials were unavailable at protocol freeze. Supportive-response quality is outside scope.", "Policies and evaluator. ")

    caption = doc.add_paragraph()
    set_paragraph_spacing(caption, before=5.5, after=5.5)
    set_font(caption.add_run("Table 1: Policy-exposed diagnostic results on 80 synthetic items."), bold=True)
    headers = ["Policy", "Action", "Urgent", "Under", "Valid", "Gap", "Exact"]
    data = [
        ["Keyword", ".225", ".189", ".879", ".121", ".000", ".225"],
        ["Agnostic", ".250", ".000", ".862", ".345", ".013", ".238"],
        ["ChildEsc-Rules", ".650", ".757", ".328", ".552", ".113", ".538"],
    ]
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    mark_table_header(table.rows[0])
    widths = [Inches(1.22)] + [Inches(0.71)] * 6
    for index, header in enumerate(headers):
        cell = table.rows[0].cells[index]
        cell.width = widths[index]
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        set_cell_shading(cell, "E7E7E7")
        set_cell_margins(cell)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_font(cell.paragraphs[0].add_run(header), size=8.5, bold=True)
    for row_index, values in enumerate(data):
        row = table.add_row()
        for index, value in enumerate(values):
            cell = row.cells[index]
            cell.width = widths[index]
            set_cell_margins(cell)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT if index == 0 else WD_ALIGN_PARAGRAPH.CENTER
            set_font(cell.paragraphs[0].add_run(value), size=8.5)
    set_table_borders(table)
    note = doc.add_paragraph()
    set_paragraph_spacing(note, after=5.5, line=9)
    set_font(note.add_run("Action and Exact use all 80 items; Under and Valid use 58 escalation-required items; Gap is Action minus Exact."), size=8, italic=True)

    add_body(doc, "ChildEsc-Rules produces the exact action on 52/80 items but the exact action-plus-target route on only 43/80. Action-only scoring therefore hides nine failures, an 11.3-point action-route gap. Conditioned on 37 action-correct handoffs, 9/37 (24.3%) violate target constraints. Family-bootstrap intervals are [.537, .762] for action accuracy, [.062, .163] for the gap, and [.438, .638] for exact routing.", "Action-route gap. ")
    add_body(doc, "In an abuse/coercion family, a generic safe-adult target can match human_support yet violate a constraint requiring a non-implicated adult. Across escalation-required items, target sets are valid for 32, missing for 17, and contain extra unpermitted targets for nine; two targetless items receive spurious targets.", "Concrete failure. ")
    add_body(doc, "These tests probe the frozen checksum without retuning it and are not held-out evidence. Latest-turn-only input under-escalates all 58 escalation-required items. Disabling only adult-implication inference leaves actions unchanged but produces a forbidden safe-adult target in 7/12 implicated-adult cases. Uppercasing preserves every route; doubling spaces reduces action agreement to 45.0% and urgent recall from 75.7% to 10.8%.", "Diagnostic stress tests. ")

    add_heading(doc, "4 Source-informed relational contract audit")
    add_body(doc, "Aggregate labels cannot state how a route should change when one operational factor changes. We froze nine matched, non-procedural probe families after v0.1 and before their first execution. Public sources motivate each relation but do not supply ground-truth labels. Each family asserts an action relation plus atomic target, domain, or response-requirement constraints. The author had inspected the router, so this is a post-freeze mechanistic audit, not held-out evaluation.")
    contract_caption = doc.add_paragraph()
    set_paragraph_spacing(contract_caption, before=4, after=4)
    set_font(contract_caption.add_run("Table 2: Frozen contract audit."), bold=True)
    contract_headers = ["Controlled factor", "Base to variant", "Pass", "Family"]
    contract_data = [
        ["Temporal immediacy", "Urgent to Urgent", "3/5", "fail"],
        ["Resolved negation", "Urgent to Continue", "3/3", "pass"],
        ["First/third person", "Urgent to Human", "4/4", "pass"],
        ["Implicated adult", "Human to Human", "6/6", "pass"],
        ["AI dependency", "Continue to Human", "4/4", "pass"],
        ["Coercive secrecy", "Continue to Human", "4/4", "pass"],
        ["Online threat", "Boundary to Urgent", "5/5", "pass"],
        ["Medical deterioration", "Boundary to Urgent", "4/5", "fail"],
        ["Explicit/implicit age", "Human to Human", "3/3", "pass"],
    ]
    contract_table = doc.add_table(rows=1, cols=len(contract_headers))
    contract_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    contract_table.autofit = False
    mark_table_header(contract_table.rows[0])
    contract_widths = [Inches(1.75), Inches(1.75), Inches(0.65), Inches(0.65)]
    for index, header in enumerate(contract_headers):
        cell = contract_table.rows[0].cells[index]
        cell.width = contract_widths[index]
        set_cell_shading(cell, "E7E7E7")
        set_cell_margins(cell, top=30, bottom=30, start=40, end=40)
        set_font(cell.paragraphs[0].add_run(header), size=7.5, bold=True)
    for values in contract_data:
        row = contract_table.add_row()
        for index, value in enumerate(values):
            cell = row.cells[index]
            cell.width = contract_widths[index]
            set_cell_margins(cell, top=20, bottom=20, start=40, end=40)
            set_font(cell.paragraphs[0].add_run(value), size=7.5)
    set_table_borders(contract_table)
    add_body(doc, "Overall, 36/39 assertions and 7/9 families pass. The phrase 'safe right now' triggers urgency despite explicit negation because 'right now' is matched globally; physical deterioration triggers urgency but omits health_professional. Both failures are retained and the checksum is not modified. The supported use is auditing implementation conformance to an inspectable routing contract, not ranking models or certifying safety.")
    add_body(doc, "Before inspecting provider output, we froze exact candidate model IDs, prompt and schema hashes, three independent trials per model, a 256-token output cap, and omission of temperature. Each item is one API attempt: hidden retries and repair are disallowed, and any provider error, refusal, or invalid schema makes a trial incomplete. Complete trials use trial means and ranges, item-level instability, and family-paired bootstrap differences. Content-addressed caches exclude credentials and must replay every item. Because credentials were unavailable at freeze, no prompted-model performance claim is made.", "Pre-registered prompted-router audit. ")

    add_heading(doc, "5 Validity, impact, and next evaluation")
    add_body(doc, "The central validity threat is circularity: scenarios, labels, lexical rules, probes, and prose were drafted in one LLM-assisted workflow. Source traceability improves auditability, not validity. The English convenience set omits dialect, code-switching, disability, culture, long relationships, and adversarial obfuscation. Severity is operational rather than clinical; v0.1 also does not isolate information-seeking as an action. Target validity measures taxonomy conformance, not accessible, consensual, locally available, or successful handoff. No practitioner or youth validation has occurred. Child-centered is a design objective, not a measured property.")
    add_body(doc, "Before comparative or generalization claims, qualified practitioners must independently review the construct, action thresholds, target constraints, missing context, and jurisdictional feasibility. Youth advisors must separately review plausibility, agency, and accessibility without personal disclosure. Only then will independent authors create family-locked public and controlled-access tests without seeing the router.")
    add_body(doc, "Evidence gates version practitioner revisions and retain disagreement; keep youth and professional judgments separate; reserve a controlled-access family-locked test; and audit any response mapper against independent human coding. Failure at any gate blocks claims that depend on the next one, and no gate alone certifies deployment safety.", "Evidence gates. ")
    add_body(doc, "Practitioner review would produce independent action and permitted/forbidden-target labels, missing-context flags, and jurisdictional-feasibility notes. Youth review would separately produce plausibility, agency, accessibility, and handoff-acceptability judgments without personal disclosure. ChildEsc would retain pre-review labels, revisions, uncertainty, and disagreement rather than collapsing perspectives into one consensus gold label. This is a protocol, not completed validation.", "Prospective validation outputs. ")
    add_body(doc, "ChildEsc's practical use is narrow: give developers and child-safety reviewers an executable object for debating escalation thresholds, unsafe-default recipients, and evidence missing before a handoff. It cannot determine clinical risk, select a real person, assess response quality, or authorize disclosure.")
    add_body(doc, "(1) When context is insufficient, should a router clarify, abstain, or emit multiple consent-preserving routes? (2) Which judgments belong separately to practitioners and youth advisors, and how should disagreement appear in scoring? (3) What evidence and governance must precede any operational handoff when a nominally trusted adult may be implicated?", "Questions for the workshop. ")

    add_heading(doc, "References")
    references = [
        "Arif, S., Borah, A., & Mihalcea, R. (2026). The Age of Curiosity Meets the Age of AI: Benchmarking Child Safety in Large Language Models. arXiv:2605.25510.",
        "Cha, H., Shukla, N., Barocas, S., Chouldechova, A., Kim, E., & Vaughan, J. W. (2026). Beyond 'I Can't Help With That': How Child Safety Experts Evaluate AI Chatbot Safety. arXiv:2608.07902. To appear at AIES 2026.",
        "Hua, Y., Na, H., Li, Z., Liu, F., Fang, X., Clifton, D., et al. (2025). A scoping review of large language models for generative tasks in mental health care. npj Digital Medicine, 8, 230.",
        "Hua, Y., Na, H., & Ayubcha, C. (2026). CARE-Bench: Benchmarking Patient-Facing LLM Triage. arXiv:2608.03731.",
        "Bean, A. M., Kearns, R. O., Romanou, A., Hafner, F. S., et al. (2025). Measuring What Matters: Construct Validity in Large Language Model Benchmarks. NeurIPS 2025.",
        "Jiao, J., Afroogh, S., Chen, K., Murali, A., Atkinson, D., & Dhurandhar, A. (2025). Safe-Child-LLM: A developmental benchmark for evaluating LLM safety in child-AI interactions. arXiv:2506.13510.",
        "Khoo, S., Chua, G., & Shong, R. (2025). MinorBench: A hand-built benchmark for content-based risks for children. arXiv:2503.10242.",
        "Krishna-Kumar, K., Lau, E., Robinson, V., Caldwell, J., Issaka, S., Wang, S., et al. (2026). CAREBench: A Child-Safety Risk Benchmark for Language Models. arXiv:2606.29685.",
        "Pombal, J., D'Eon, M., Guerreiro, N. M., Martins, P. H., Farinhas, A., & Rei, R. (2025). MindEval: Benchmarking language models on multi-turn mental health support. arXiv:2511.18491.",
        "Ragone, G., Buono, P., Good, J., & Lanzilotti, R. (2026). Do Children Trust AI, and Should They? Proceedings of CHI '26. https://doi.org/10.1145/3772318.3790765.",
        "988 Suicide & Crisis Lifeline. (2024). Suicide Safety Policy. https://988lifeline.org/professionals/best-practices/.",
        "Substance Abuse and Mental Health Services Administration. (2024). Saving Lives in America: 988 Quality and Services Plan.",
        "U.S. Department of Health and Human Services. (2023). Collecting, Using, or Sharing Consumer Health Information?",
        "UNICEF. (2025). Guidance on AI and Children 3.0.",
        "UNICEF. (2026). When AI Becomes a Friend: Child Rights Risks, Harms, and Regulatory Responses to AI Chatbots and Companions.",
        "NeurIPS 2026 Workshop on Child Safety in AI. (2026). Call for Papers. https://childsafety-ai.github.io/.",
        "AI Child Safety Initiative. (2025). Preventing AI-Generated Child Sexual Abuse Material Necessitates New Approaches to AI Safety. https://aichildsafety.github.io/.",
    ]
    for reference in references:
        add_reference(doc, reference)

    add_heading(doc, "Appendix A. Artifact and schema")
    add_body(doc, "The research package contains standard-library Python source, 48 tests for the frozen scientific and manuscript path, 22 provider-path tests, 20 source families, a source register, family rationale map, controlled authoring protocol, frozen contract probes, deterministic generation, item-level predictions and assertions, aggregate metrics, error analysis, ablations, a gated follow-up specification, and orthographic checks. Running make reproduce regenerates all 80 items and every reported value.", size=9.5, after=4, line=10)

    add_heading(doc, "Appendix B. Metric details")
    add_body(doc, "Under-escalation is conditioned on items requiring human or urgent support. Strict valid-target rate requires a nonempty predicted set that is a subset of permitted targets and disjoint from forbidden targets. Exact route additionally requires the exact action and requires no emitted target for targetless actions. The action-route gap equals exact action accuracy minus exact-route accuracy.", size=9.5, after=4, line=10)

    doc.add_page_break()
    add_heading(doc, "Appendix C. Diagnostic failure analysis")
    add_body(doc, "Agree is action agreement with the full-conversation run. Under is conditioned on escalation-required items; Valid on items with permitted targets; Unsafe on items with forbidden targets. These are policy-exposed diagnostics, not generalization estimates.", size=9.5, after=4, line=10)
    diagnostic_headers = ["Condition", "Agree", "Urgent", "Under", "Valid", "Unsafe", "Exact"]
    diagnostic_data = [
        ["Full conversation", "1.000", ".757", ".328", ".552", ".000", ".538"],
        ["Latest turn only", ".338", ".000", "1.000", ".000", ".000", ".138"],
        ["Adult inference off", "1.000", ".757", ".328", ".431", ".583", ".488"],
        ["Uppercase", "1.000", ".757", ".328", ".552", ".000", ".538"],
        ["Extra spaces", ".450", ".108", ".897", ".034", ".083", ".175"],
        ["Expanded contractions", ".975", ".730", ".362", ".534", ".000", ".525"],
    ]
    diagnostic_table = doc.add_table(rows=1, cols=len(diagnostic_headers))
    diagnostic_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    diagnostic_table.autofit = False
    mark_table_header(diagnostic_table.rows[0])
    diagnostic_widths = [Inches(1.45)] + [Inches(0.75)] * 6
    for index, header in enumerate(diagnostic_headers):
        cell = diagnostic_table.rows[0].cells[index]
        cell.width = diagnostic_widths[index]
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        set_cell_shading(cell, "E7E7E7")
        set_cell_margins(cell, start=30, end=30)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_font(cell.paragraphs[0].add_run(header), size=7.5, bold=True)
    for values in diagnostic_data:
        row = diagnostic_table.add_row()
        for index, value in enumerate(values):
            cell = row.cells[index]
            cell.width = diagnostic_widths[index]
            set_cell_margins(cell, start=30, end=30)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT if index == 0 else WD_ALIGN_PARAGRAPH.CENTER
            set_font(cell.paragraphs[0].add_run(value), size=7.5)
    set_table_borders(diagnostic_table)

    add_heading(doc, "Appendix D. Prospective validation protocol")
    add_body(doc, "No recruitment or data collection is authorized in this workspace. Subject to an appropriate external determination, practitioners would independently label action, permitted and forbidden targets, missing context, and coercion risk. Youth advisors would review plausibility, agency, accessibility, and handoff framing without being asked to disclose personal experiences. Disagreement and pre-review labels would be retained. Protocol preparation is not validation.", size=9.5, after=4, line=10)

    add_heading(doc, "Appendix E. Prospective delegated follow-up extension")
    add_body(doc, "The proposed 1-24 hour crisis-service follow-up is a non-operational governance specification, not an established 988 policy; no cutoff is validated. It requires a written 988/center partnership, independent safeguarding and legal review, separate revocable consent, human crisis-professional approval, minimum-necessary transfer, receiving-service capacity guarantees, and prospective measurement of false alerts, missed urgency, chilling effects, coercion, and disparities. Imminent danger is excluded from a delayed queue. Until these gates pass, ChildEsc must not collect PII, schedule follow-up, transmit data, or initiate contact.", size=9.5, after=4, line=10)

    add_heading(doc, "Appendix F. Independent holdout status")
    add_body(doc, "No independently authored holdout is reported. The prospective procedure requires an author who has not inspected router rules, existing scenario text, or item-level failures. Current authors and coding agents are ineligible. A future holdout must be evaluated once without router tuning and reported separately from v0.1.", size=9.5, after=4, line=10)

    add_heading(doc, "Appendix G. Compute, ethics, and LLM usage")
    add_body(doc, "Reported experiments use no GPU, model API, training, or external service and complete in under one second on a laptop-class CPU. The prompted-router harness was tested with mock transports; no live provider result is reported. A general-purpose LLM coding assistant drafted candidate scenarios and labels, implementation, literature notes, and manuscript text. No LLM judged outputs or generated reported measurements. Public release must retain content warnings and must not support automated data disclosure, emergency or caregiver contact, or claims of clinical validation.", size=9.5, after=4, line=10)

    add_heading(doc, "Appendix H. Source traceability and future authoring")
    add_body(doc, "The source register records what each source supports and does not support. The v0.1 family map is retrospective and domain-level; it does not make individual cases source-grounded. The prospective protocol requires one-factor isolation, information-state timing, age and locale metadata, source-to-case rationale, non-procedural content, independent first-pass labels without router output, retained disagreement, and family-locked development, validation, public-test, and controlled-access splits.", size=9.5, after=4, line=10)

    footer = section.footer.paragraphs[0]
    footer.clear()
    draft_run = footer.add_run("Anonymous collaboration draft | ")
    set_font(draft_run, size=8)
    add_page_number(footer)

    core = doc.core_properties
    core.title = "ChildEsc Workshop Paper"
    core.subject = "NeurIPS 2026 Child Safety in AI workshop submission draft"
    core.author = "Anonymous"
    core.keywords = "child safety, conversational AI, escalation, benchmark, human handoff"

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUTPUT)
    return OUTPUT


if __name__ == "__main__":
    print(build())
