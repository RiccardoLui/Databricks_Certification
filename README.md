# Start here - Databricks certification kit

Prepared for Riccardo Lui, 17 November 2026. This is an original curriculum based only on official Databricks technical documentation and the attached August 2026 exam guide. Read STUDY_GUIDE.pdf or STUDY_GUIDE.md first. Every technical chapter and notebook includes official references.

## Contents

- STUDY_GUIDE.pdf / STUDY_GUIDE.md: theory, exam domain mapping, decision tables, scenario explanations, advanced bridge and reference catalog.
- notebooks/: 14 Jupyter-format tutorials, 00 through 13, with exercises, expected results, assertions and explanations.
- bundle/: complete serverless Jobs training project with conditional left/inner join branches, a publication task, a For each country task, and dev/test/prod targets.
- pipelines/: current Python declarative pipeline source and advanced AUTO CDC source, intended to be attached to pipelines.
- OFFICIAL_REFERENCES.md / references.json: official source catalog.
- VALIDATION_REPORT.md: checks performed locally and runtime checks still required.

## Setup and execution

1. Import the IPYNB files into Databricks (Workspace > folder > Import). Official [import instructions](https://docs.databricks.com/aws/en/notebooks/notebook-export-import).
2. Attach Python-capable UC compute. Set CATALOG to an existing writable catalog, and PREFIX to your personal lab prefix in each notebook. No CREATE CATALOG is required.
3. Run 00, then 01, then 02. Run the other labs in numeric order; their headers identify prerequisites and execution contexts.
4. Read bundle/README.md before deployment. The pipeline Python files run inside a Lakeflow pipeline, not as ordinary local Python.
5. Keep source-schema/checkpoint state with its intended target during incremental exercises. UUID experiment paths isolate re-runs. Notebook 00 deliberately resets the main Bronze table; do not rerun it while an append-only streaming pipeline is consuming that table.

Official [Free Edition limitations](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations) and [serverless limitations](https://docs.databricks.com/aws/en/compute/serverless/limitations) determine available labs. Core synthetic exercises aim to work on supported UC compute. Managed connectors, external storage/events, multiple identities, ABAC administration, detailed classic Spark UI, and classic settings need additional capabilities. Optional cells start disabled. No live external API/database is required for the core exercises.

## Synthetic acceptance contract

8 raw events -> 2 invalid amounts -> 6 valid event rows -> 5 distinct valid events -> 4 latest valid orders. Inner customer join=2; left join=4; unmatched=2. Latest-order revenue=220.00. The separate pipeline summarizes all valid event rows: 6 rows, amount 420.00. This intentional difference teaches data grain.

## Verification status

Locally checked notebook structure/Python syntax, YAML and DAG structure, file references, and synthetic expected answers. No Databricks workspace execution, live managed connector, multi-user security test, CLI validation, or deployment has been performed. Run the embedded assertions and collect the evidence described in the guide. No fabricated notebook outputs are included.

## Cleanup

Only remove objects in the dedicated prefix after stopping streams/pipelines/jobs. Review table types before dropping: managed and external table lifecycles differ. Keep the checkpoint/target pair until finished with the incremental experiment. A separate notebook with a new prefix is the simplest fresh run. Bundle resource destruction and data cleanup are different actions; use the documented commands deliberately.
