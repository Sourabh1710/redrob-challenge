# Redrob Intelligent Candidate Ranker

An optimized, deterministic, and highly performant Python-native candidate evaluation and ranking system built for the Redrob "India Runs" Hackathon.

---

## System Performance

- **Dataset Evaluated:** 100,000 raw candidate profiles
- **Total Execution Time:** 13.46 seconds (on a standard 4-core CPU)
- **Memory Footprint:** < 20 MB (utilizes stream-based parsing)
- **Dependencies:** None (Written entirely in pure Python standard library to ensure absolute environment stability)

---

## Core Architectural Pillars

1. **The Honeypot Shield**
   - Hard-filters out candidate profiles with corrupted dates, impossible skills duration, or duplicate/falsified records.
2. **Consulting/Service Exclusions**
   - Programmatically identifies and filters out candidates who have *only* worked at IT services giants (e.g., TCS, Infosys, Wipro).
   - Preserves high-quality candidates who transitioned into product-focused environments.
3. **Trust-Weighted Skill Scorer**
   - Evaluates skills by a custom formula that weights proficiency, usage duration, and community endorsements.
   - Bypasses candidate "keyword-stuffing" tricks.
4. **Behavioral Platform Modifiers**
   - Adjusts candidate ranks based on live platform engagement metrics (recruiter response rate, open-to-work flag, profile views).
   - Ensures reachable-first matches.

---

## Getting Started

### Prerequisites
- Python 3.11+ (Fully tested on Python 3.12.3)

### Installation & Setup

1. **Clone this repository:**
   ```bash
   git clone <your-repo-url-here>
   cd Redrob-challenge
   ```

2. **Prepare the dataset:**
   Place the uncompressed dataset `candidates.jsonl` inside the `data/` folder structured as follows:
   ```text
   data/
   └── candidates.jsonl
   ```

### Execution

Run the orchestrator script to evaluate 100,000 candidates and output the final validated top 100 shortlist:

```bash
python3 rank.py
```

> 💾 **Output:** The final rankings will be automatically saved as a validated, format-compliant CSV file in `data/submission.csv`.
