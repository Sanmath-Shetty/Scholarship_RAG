"""
Raw structured source data for the Government Scheme Assistant RAG project.

Each entry = one scheme-document. Post-Matric is split into 4 separate
scheme-documents (SC/ST/OBC/Minority) per our Phase 2 design decision,
rather than one blended "Post-Matric" document.

Every fact here traces back to Phase 1 research (official scholarships.gov.in
sources where noted, or cross-referenced aggregator consensus). Anything not
confirmed is explicitly marked "GAP: ..." rather than invented -- these need
follow-up before final indexing, and should NOT be embedded/indexed as-is.
"""

SCHEMES = [
    {
        "scheme_id": "csss",
        "scheme_name": "Central Sector Scheme of Scholarship (CSSS)",
        "scheme_category": "merit_general",
        "sections": {
            "basics": (
                "The Central Sector Scheme of Scholarship (CSSS) for College and University "
                "Students is administered by the Department of Higher Education, Ministry of "
                "Education, Government of India, and delivered through the National Scholarship "
                "Portal (NSP). The objective of CSSS is to provide financial assistance to "
                "meritorious students from economically weaker families to meet part of their "
                "day-to-day expenses while pursuing full-time undergraduate or postgraduate "
                "studies, including professional courses such as engineering and medicine. "
                "Around 82,000 fresh CSSS scholarships are awarded each year, split roughly "
                "equally between boys and girls."
            ),
            "eligibility": (
                "To be eligible for CSSS, a student must be in the top 20th percentile of "
                "successful candidates in their Class 12 board exam (i.e. above the 80th "
                "percentile cutoff) from a recognized board. The student's family gross annual "
                "income from all sources must not exceed Rs. 4.5 lakh. The student must be "
                "enrolled full-time in a regular undergraduate or postgraduate course at a "
                "recognized college or university -- diploma courses and distance/correspondence "
                "education are explicitly not eligible under CSSS. A CSSS applicant cannot be "
                "receiving any other scholarship or fee reimbursement at the same time. A valid "
                "Aadhaar number and a bank account in the student's own name are required."
            ),
            "benefits": (
                "Under CSSS, the scholarship amount is Rs. 12,000 per year at the graduation "
                "level for the first three years, and Rs. 20,000 per year at the postgraduate "
                "level. Students in technical courses such as B.Tech/BE receive Rs. 12,000 per "
                "year for years 1-3 and Rs. 20,000 per year in year 4 only, capped at 4 years "
                "total. CSSS scholarship amounts are disbursed via Direct Benefit Transfer (DBT) "
                "directly into the student's Aadhaar-seeded bank account."
            ),
            "renewal": (
                "To renew a CSSS scholarship each year, a student must pass the previous "
                "academic year, maintain at least 50% marks in annual university exams, "
                "maintain at least 75% attendance, continue in the same course, and have no "
                "disciplinary action against them. The total eligible duration under CSSS is a "
                "maximum of 5 years overall (4 years specifically for B.Tech/BE students)."
            ),
            "application_process": (
                "To apply for CSSS, a student registers on the National Scholarship Portal "
                "(NSP) via One-Time Registration (OTR) using an Aadhaar-linked mobile number, "
                "logs in, selects the CSSS scheme under the Post-Matric category, fills in "
                "academic and category details, uploads required documents, and submits. Fresh "
                "CSSS applicants must upload their Class 12 mark sheet, family income "
                "certificate, category/caste certificate if applicable, and a disability "
                "certificate if applicable. Renewal applicants for CSSS only need to upload "
                "their previous year's mark sheet. For the 2025-26 cycle, the CSSS portal opened "
                "on June 2, 2025; exact dates shift year to year."
            ),
            "edge_cases": (
                "Common reasons CSSS applications get rejected or marked defective include: "
                "incorrect bank details, family income exceeding the Rs. 4.5 lakh CSSS limit, "
                "not meeting the 80th percentile requirement, admission at an institution with "
                "inactive AISHE status, holding a duplicate scholarship, incomplete document "
                "uploads, institute verification failure, and Aadhaar/name mismatches between "
                "the Class 12 marksheet and Aadhaar. CSSS explicitly excludes students pursuing "
                "diploma courses, distance education, or those who took a drop year after Class "
                "12. On NSP, a 'Defective' CSSS application has correctable errors and can be "
                "resubmitted, while a 'Rejected' application is permanently disqualified."
            ),
        },
    },
    {
        "scheme_id": "aicte_pragati",
        "scheme_name": "AICTE Pragati Scholarship",
        "scheme_category": "technical_girls",
        "sections": {
            "basics": (
                "The AICTE Pragati Scholarship is administered by the All India Council for "
                "Technical Education (AICTE) under the Ministry of Education, and delivered "
                "through the National Scholarship Portal (NSP). The objective of the AICTE "
                "Pragati Scholarship is to provide financial assistance to girl students "
                "pursuing technical education at the diploma or degree level in AICTE-approved "
                "institutions. 10,000 AICTE Pragati scholarships are awarded annually, split "
                "5,000 for degree students and 5,000 for diploma students."
            ),
            "eligibility": (
                "To be eligible for the AICTE Pragati Scholarship, the applicant must be female "
                "and of Indian origin. The applicant must be admitted to the 1st year of a "
                "technical diploma or degree program at an AICTE-approved institution through "
                "the centralised admission process (2nd year admission is allowed only via "
                "lateral entry). The applicant's annual family income from all sources must not "
                "exceed Rs. 8 lakh under Pragati. A maximum of 2 girl children per family can "
                "receive the AICTE Pragati Scholarship simultaneously. Students admitted through "
                "the management quota are NOT eligible for Pragati. The applicant must hold a "
                "general savings bank account (not joint or minor) in her own name, Aadhaar-"
                "linked for DBT."
            ),
            "benefits": (
                "The AICTE Pragati Scholarship provides Rs. 50,000 per year, paid as a lump sum "
                "via Direct Benefit Transfer (DBT), for up to 4 years for a degree program or up "
                "to 3 years for a diploma program. The Pragati scholarship amount is intended to "
                "cover tuition fees, laptop, books, equipment, software, and other education-"
                "related costs, with no separate receipts required."
            ),
            "renewal": (
                "To renew the AICTE Pragati Scholarship each academic year, the student must "
                "submit passing transcripts and a regular-promotion letter from her college, and "
                "must maintain a satisfactory academic record."
            ),
            "application_process": (
                "To apply for AICTE Pragati, a student completes One-Time Registration (OTR) on "
                "the National Scholarship Portal (NSP) and then applies specifically under the "
                "Pragati scheme. Verification for Pragati flows through the District Nodal "
                "Officer (DNO), then State Nodal Officer (SNO), then AICTE's Ministry Nodal "
                "Officer (MNO). The reported application window for the 2026-27 AICTE Pragati "
                "cycle is June 1 to October 31, 2026, with verification allowed until November "
                "15, 2026 -- confirm exact dates on NSP each year."
            ),
            "edge_cases": (
                "For AICTE Pragati queries, contact pragatisaksham@aicte-india.org, or the "
                "Pragati/Saksham Scheme Helpline at 011-29581118, the AICTE Help Desk at "
                "011-26131497, or the NSP Help Desk at 0120-6619540. If there is no eligible "
                "applicant for a degree or diploma slot under Pragati in a given cycle, that "
                "scholarship slot is transferable to the other category (degree <-> diploma)."
            ),
        },
    },
    {
        "scheme_id": "aicte_saksham",
        "scheme_name": "AICTE Saksham Scholarship",
        "scheme_category": "technical_disability",
        "sections": {
            "basics": (
                "The AICTE Saksham Scholarship is administered by the All India Council for "
                "Technical Education (AICTE), delivered through the National Scholarship Portal "
                "(NSP). The AICTE Saksham Scholarship is structurally very similar to the AICTE "
                "Pragati Scholarship, but Saksham is specifically for specially-abled students, "
                "not girl students. The objective of AICTE Saksham is to provide financial "
                "assistance to specially-abled students pursuing technical diploma or degree "
                "education at AICTE-approved institutions."
            ),
            "eligibility": (
                "To be eligible for the AICTE Saksham Scholarship, the applicant must be a "
                "specially-abled or differently-abled student with a disability of not less "
                "than 40%, certified by a competent medical authority. The applicant must be "
                "admitted to the 1st year of a technical degree or diploma course at an "
                "AICTE-approved institution (2nd year allowed only via lateral entry). The "
                "annual family income from all sources must not exceed Rs. 8 lakh under Saksham. "
                "The applicant must be studying full-time."
            ),
            "benefits": (
                "The AICTE Saksham Scholarship provides Rs. 50,000 per year, described as an "
                "'incidentals' grant, for up to 4 years for a degree program (if admitted in "
                "1st year) or up to 3 years for a diploma program."
            ),
            "renewal": (
                "GAP: exact Saksham renewal conditions (attendance %, minimum marks to "
                "continue) were not clearly confirmed in Phase 1 research. Assumed similar to "
                "Pragati's renewal pattern (passing transcripts + regular-promotion letter each "
                "year) but this needs direct confirmation on the NSP/AICTE portal before being "
                "treated as fact."
            ),
            "application_process": (
                "To apply for AICTE Saksham, a student logs into the National Scholarship "
                "Portal (NSP), goes to the Student tab, selects 'Apply for Scholarship - Login', "
                "chooses 'AICTE Saksham Scholarship', completes eKYC, uploads scanned documents, "
                "and submits. The 2026-27 Saksham deadline was reported as October 31, 2026 by "
                "one source -- reconfirm on NSP directly since AICTE scheme deadlines shift "
                "yearly."
            ),
            "edge_cases": (
                "GAP: the exact list of accepted disability certificate formats and issuing "
                "authorities for AICTE Saksham was not clearly confirmed in Phase 1 research and "
                "needs direct verification before being presented as fact to end users."
            ),
        },
    },
    {
        "scheme_id": "mcm",
        "scheme_name": "Merit-cum-Means Scholarship for Professional and Technical Courses (Minority)",
        "scheme_category": "minority_professional",
        "sections": {
            "basics": (
                "The Merit-cum-Means (MCM) Scholarship for Professional and Technical Courses "
                "is administered by the Ministry of Minority Affairs, Government of India, and "
                "delivered through the National Scholarship Portal (NSP) / scholarships.gov.in. "
                "Important: the MCM Scholarship is specifically for MINORITY community students "
                "-- it is not a general merit-cum-means scheme. The objective of MCM is to "
                "provide financial assistance to poor and meritorious minority-community "
                "students to pursue professional and technical courses such as engineering, "
                "medicine, law, and management at the undergraduate and postgraduate level. "
                "Approximately 60,000 fresh MCM scholarships are awarded per year, distributed "
                "by State/UT based on minority population, with 30% of MCM scholarships "
                "reserved for girls."
            ),
            "eligibility": (
                "To be eligible for the MCM Scholarship, the applicant must belong to a "
                "notified minority community: Muslim, Sikh, Christian, Buddhist, Jain, or "
                "Zoroastrian (Parsi). The applicant's family/guardian annual income from all "
                "sources must not exceed Rs. 2.5 lakh under MCM. The applicant must have "
                "secured at least 50% marks (or equivalent grade) in the previous qualifying "
                "exam, and must be enrolled in (or newly admitted to) an approved UG/PG "
                "professional or technical course of at least 1-year duration at a recognized "
                "institution. Students admitted via a competitive exam are eligible under MCM; "
                "students admitted without a competitive exam are also eligible for MCM provided "
                "they hold at least 50% marks at the higher-secondary/graduation level. A "
                "student already availing another central government scholarship for SC/ST/OBC/"
                "minorities is NOT eligible for MCM (no double-dipping across central schemes)."
            ),
            "benefits": (
                "The MCM Scholarship provides Rs. 20,000 per year, disbursed via Direct Benefit "
                "Transfer (DBT) to the student's registered bank account. Continuation of the "
                "MCM scholarship in subsequent years depends on successful completion of the "
                "course each year."
            ),
            "renewal": (
                "GAP: exact MCM renewal eligibility conditions (minimum marks/attendance to "
                "continue) beyond 'successful completion of the course each year' were not "
                "clearly detailed in Phase 1 research and need direct verification on "
                "scholarships.gov.in."
            ),
            "application_process": (
                "To apply for MCM, a student creates an account on scholarships.gov.in, "
                "completes One-Time Registration (OTR), fills in personal, academic, and "
                "financial details, and submits along with required documents. Documents "
                "needed for MCM include: minority community certificate, income certificate, "
                "admission letter, academic transcripts, and attested Aadhaar/identity proof."
            ),
            "edge_cases": (
                "Under MCM, if a student violates school discipline or scholarship terms, the "
                "scholarship may be suspended or cancelled. False statements or incorrect MCM "
                "applications lead to cancellation and recovery of the disbursed amount. "
                "Students cannot avail benefits from multiple central government scholarship "
                "schemes simultaneously."
            ),
        },
    },
    {
        "scheme_id": "post_matric_sc",
        "scheme_name": "Post-Matric Scholarship for SC Students",
        "scheme_category": "post_matric",
        "sections": {
            "basics": (
                "The Post-Matric Scholarship for SC (Scheduled Caste) Students is administered "
                "by the Ministry of Social Justice & Empowerment, delivered through "
                "scholarships.gov.in (NSP). This is one of four parallel central Post-Matric "
                "schemes (SC, ST, OBC, and Minority), each with its own ministry, income "
                "ceiling, and benefit amounts, though all share the same NSP application flow. "
                "The Post-Matric SC Scholarship covers students from Class 11 onward, including "
                "Class 11/12, ITI/Polytechnic diploma, undergraduate, postgraduate, PhD, and "
                "professional courses such as CA/ICWA/CS. Its objective is to reimburse "
                "compulsory non-refundable course fees and pay a monthly maintenance allowance "
                "to SC students beyond matriculation."
            ),
            "eligibility": (
                "To be eligible for the Post-Matric SC Scholarship, the applicant must belong "
                "to a Scheduled Caste (SC) community with a valid caste certificate, and family "
                "income must not exceed Rs. 2.5 lakh per year. Only one central scholarship can "
                "be drawn per student per period under this scheme -- no double-dipping with "
                "other central scholarships."
            ),
            "benefits": (
                "Under the Post-Matric SC Scholarship, there are two components: reimbursement "
                "of compulsory non-refundable course fees, and a monthly maintenance allowance "
                "of roughly Rs. 230 to Rs. 1,200 per month, depending on the course group and "
                "whether the student is a hosteller or day-scholar. Disbursal is via Direct "
                "Benefit Transfer (DBT) to an Aadhaar-linked bank account. GAP: a note reported "
                "separately mentions a proposal to raise the SC income ceiling to Rs. 4.5 lakh -- "
                "treat Rs. 2.5 lakh as the current confirmed figure and verify this proposed "
                "change before treating it as active."
            ),
            "renewal": (
                "GAP: specific year-on-year renewal conditions for Post-Matric SC (minimum "
                "marks/attendance) were not itemized separately in Phase 1 research beyond the "
                "general application process below; verify against the official scheme "
                "guideline PDF."
            ),
            "application_process": (
                "To apply for the Post-Matric SC Scholarship, a student registers once via "
                "One-Time Registration (OTR) on scholarships.gov.in, then selects the Post-"
                "Matric scheme for the SC category specifically and fills the application. "
                "Required documents include: caste certificate, income certificate, previous "
                "marksheet, admission/fee proof, and bank details -- verified first by the "
                "institute, then by the state/ministry. The 2026-27 application window was "
                "reported open from around June 1, 2026, though scheme-specific deadlines are "
                "posted on the portal and frequently extended."
            ),
            "edge_cases": (
                "Common issues with Post-Matric SC applications include missing One-Time "
                "Registration (OTR), Aadhaar-bank mismatch blocking DBT disbursal, and late "
                "institution verification. Note that many state governments also run their own "
                "separate Post-Matric schemes for SC students with different amounts and income "
                "ceilings -- these are distinct from this central scheme and are out of scope "
                "for this assistant's MVP."
            ),
        },
    },
    {
        "scheme_id": "post_matric_st",
        "scheme_name": "Post-Matric Scholarship for ST Students",
        "scheme_category": "post_matric",
        "sections": {
            "basics": (
                "The Post-Matric Scholarship for ST (Scheduled Tribe) Students is administered "
                "by the Ministry of Tribal Affairs, delivered through scholarships.gov.in (NSP). "
                "This is one of four parallel central Post-Matric schemes (SC, ST, OBC, and "
                "Minority). The Post-Matric ST Scholarship covers students from Class 11 "
                "onward, including Class 11/12, ITI/Polytechnic diploma, undergraduate, "
                "postgraduate, PhD, and professional courses. Its objective is to reimburse "
                "compulsory non-refundable course fees and pay a monthly maintenance allowance "
                "to ST students beyond matriculation."
            ),
            "eligibility": (
                "To be eligible for the Post-Matric ST Scholarship, the applicant must belong "
                "to a Scheduled Tribe (ST) community with a valid tribal certificate, and family "
                "income must not exceed Rs. 2.5 lakh per year -- the same income ceiling as the "
                "SC scheme. Only one central scholarship can be drawn per student per period."
            ),
            "benefits": (
                "Like the Post-Matric SC Scholarship, the Post-Matric ST Scholarship reimburses "
                "compulsory non-refundable course fees and pays a monthly maintenance allowance "
                "of roughly Rs. 230 to Rs. 1,200 per month depending on course group and "
                "hosteller/day-scholar status, disbursed via Direct Benefit Transfer (DBT)."
            ),
            "renewal": (
                "GAP: specific year-on-year renewal conditions for Post-Matric ST were not "
                "itemized separately in Phase 1 research; verify against the official Ministry "
                "of Tribal Affairs scheme guideline."
            ),
            "application_process": (
                "To apply for the Post-Matric ST Scholarship, a student registers once via "
                "One-Time Registration (OTR) on scholarships.gov.in, then selects the Post-"
                "Matric scheme for the ST category and fills the application. Required "
                "documents include: tribal certificate, income certificate, previous marksheet, "
                "admission/fee proof, and bank details."
            ),
            "edge_cases": (
                "As with the SC scheme, common issues include missing OTR, Aadhaar-bank "
                "mismatch, and late institution verification. State-run parallel ST scholarship "
                "schemes exist separately and are out of scope for this assistant's MVP."
            ),
        },
    },
    {
        "scheme_id": "post_matric_obc",
        "scheme_name": "Post-Matric Scholarship for OBC Students",
        "scheme_category": "post_matric",
        "sections": {
            "basics": (
                "The Post-Matric Scholarship for OBC (Other Backward Classes, including EBC/"
                "DNT) Students is administered by the relevant central ministry, delivered "
                "through scholarships.gov.in (NSP). This is one of four parallel central "
                "Post-Matric schemes (SC, ST, OBC, and Minority). It covers students from Class "
                "11 onward and aims to reimburse compulsory non-refundable fees and pay a "
                "monthly maintenance allowance to OBC/EBC/DNT students beyond matriculation."
            ),
            "eligibility": (
                "To be eligible for the Post-Matric OBC Scholarship, the applicant must belong "
                "to an OBC/EBC/DNT community with a valid caste/community certificate. The "
                "central OBC scheme's family income ceiling is Rs. 1.5 lakh per year -- notably "
                "lower than the Rs. 2.5 lakh ceiling for the SC and ST versions of this scheme. "
                "Some state-run OBC scholarship variants use a different ceiling (e.g. Rs. 1 "
                "lakh in one state-specific scheme found during research) -- these state "
                "schemes should not be confused with this central OBC scheme."
            ),
            "benefits": (
                "Like the SC and ST versions, the Post-Matric OBC Scholarship reimburses "
                "compulsory non-refundable course fees and pays a monthly maintenance "
                "allowance, disbursed via Direct Benefit Transfer (DBT). GAP: the exact monthly "
                "maintenance allowance range specific to the OBC scheme (as opposed to the "
                "SC/ST range already confirmed) was not separately itemized in Phase 1 research "
                "-- verify whether it matches the Rs. 230-1,200/month range or differs."
            ),
            "renewal": (
                "GAP: specific year-on-year renewal conditions for Post-Matric OBC were not "
                "itemized separately in Phase 1 research; verify against the official scheme "
                "guideline."
            ),
            "application_process": (
                "To apply for the Post-Matric OBC Scholarship, a student registers once via "
                "One-Time Registration (OTR) on scholarships.gov.in, then selects the Post-"
                "Matric scheme for the OBC category and fills the application. Required "
                "documents include: OBC/EBC/DNT caste certificate, income certificate, previous "
                "marksheet, admission/fee proof, and bank details."
            ),
            "edge_cases": (
                "As with the SC and ST schemes, common issues include missing OTR, Aadhaar-bank "
                "mismatch, and late institution verification. Because the OBC central scheme's "
                "income ceiling (Rs. 1.5 lakh) differs from SC/ST (Rs. 2.5 lakh), and state-run "
                "OBC variants use yet other ceilings, this is a high-risk area for the assistant "
                "to confuse -- always confirm which specific OBC scheme (central vs. state) a "
                "user is asking about."
            ),
        },
    },
    {
        "scheme_id": "post_matric_minority",
        "scheme_name": "Post-Matric Scholarship for Minority Students",
        "scheme_category": "post_matric",
        "sections": {
            "basics": (
                "The Post-Matric Scholarship for Minority Students is administered by the "
                "Ministry of Minority Affairs, delivered through scholarships.gov.in (NSP). "
                "This is one of four parallel central Post-Matric schemes (SC, ST, OBC, and "
                "Minority). Note: this is DIFFERENT from the Merit-cum-Means (MCM) Scholarship "
                "-- both serve minority students, but MCM is specifically for professional/"
                "technical courses, while this Post-Matric Minority scheme has broader course "
                "coverage from Class 11 onward, similar in structure to the SC/ST/OBC Post-"
                "Matric schemes."
            ),
            "eligibility": (
                "To be eligible for the Post-Matric Minority Scholarship, the applicant must "
                "belong to a notified minority community (Muslim, Sikh, Christian, Buddhist, "
                "Jain, or Zoroastrian/Parsi) with a valid minority community certificate. "
                "GAP: the exact income ceiling for this specific Post-Matric Minority scheme "
                "(as distinct from MCM's confirmed Rs. 2.5 lakh) was not separately confirmed "
                "in Phase 1 research -- do not assume it matches MCM's ceiling without "
                "verification, since these are administratively separate schemes."
            ),
            "benefits": (
                "GAP: exact benefit amounts (fee reimbursement + maintenance allowance figures) "
                "specific to the Post-Matric Minority scheme were not separately itemized in "
                "Phase 1 research and should not be assumed identical to the SC/ST/OBC Post-"
                "Matric maintenance allowance range without verification."
            ),
            "renewal": (
                "GAP: renewal conditions for Post-Matric Minority were not confirmed in Phase 1 "
                "research."
            ),
            "application_process": (
                "To apply for the Post-Matric Minority Scholarship, a student registers once "
                "via One-Time Registration (OTR) on scholarships.gov.in, then selects the "
                "Post-Matric scheme for the Minority category and fills the application. "
                "Required documents are expected to include a minority community certificate, "
                "income certificate, previous marksheet, admission/fee proof, and bank details, "
                "consistent with the pattern seen across the other Post-Matric categories."
            ),
            "edge_cases": (
                "This scheme is easily confused with MCM since both target minority students -- "
                "the assistant should always clarify whether a user is asking about the general "
                "Post-Matric Minority scheme (broader course coverage, Class 11 onward) or the "
                "MCM scheme (specifically professional/technical courses at UG/PG level) before "
                "answering."
            ),
        },
    },
]
