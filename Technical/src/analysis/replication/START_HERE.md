# START HERE: Perfect Replication Runner

Quick path to reproduce authentic artifacts and text-aligned checks.

## 1. Prereqs
- Windows + Python 3.9+ (venv recommended)
- Activate venv in project root

## 2. Run
```bash
python "src/analysis/replication/run_authentic_pipeline.py"
python "src/analysis/replication/textual_consistency_checks.py"
```

## 3. Inspect
- Authentic table: `src/analysis/replication/output/table_5_4_authentic.csv`
- Validation summary: `src/analysis/replication/output/authentic_validation_summary.json`
- Text alignment: `src/analysis/replication/output/BOOK_TEXT_ALIGNMENT.md`

## 4. Next
- Add citations to the alignment report
- Reconcile gK definition
- Build per-year identity ledger for final confirmation
