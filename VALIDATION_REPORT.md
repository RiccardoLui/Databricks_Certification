# Validation report

Checked 17 November 2026.

## Completed locally

- 14 notebook files parsed as notebook format 4.5; unique cell IDs, kernel metadata, text sources, required code fields and no fabricated execution outputs checked.
- 133 cells, including 50 Python code cells, parsed; 73 assertion statements found. All bundled Python source files passed syntax parsing.
- Bundle YAML parsed; task names unique; dependencies resolve; graph is acyclic; true/false branch outcomes, publication run condition, and nested source paths checked.
- Independent Python oracle extracted the synthetic source literal and confirmed 8 raw / 2 rejected / 6 valid / 5 distinct valid events / 4 latest orders; inner=2, left=4; order revenue=220.00; event revenue=420.00; explode=3 versus explode_outer=4.
- Guide reference identifiers resolve to 77 official Databricks URLs. No third-party technical references are used. This checks reference identity, not a permanent guarantee that a live URL will never change.
- PDF layout rendered and visually inspected; table flow, reference links and page boundaries checked.

## Requires your Databricks environment

No Spark/Delta execution, Auto Loader ingestion, CLI bundle validation/deployment, pipeline update, source connector connection, administrative policy action, or multi-user access test has been performed here. Follow notebook assertions and the guide's acceptance steps. Runtime, edition, cloud and permissions can affect availability.

Optional admin/compute cells start disabled. The evolution experiment intentionally raises a schema-change error before the documented restart. All code cells have null execution counters; expected results are stated as teaching acceptance contracts, not recorded runtime output.
