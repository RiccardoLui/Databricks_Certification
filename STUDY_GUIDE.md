# Databricks Data Engineer Associate
## Theory, guided labs, and an advanced bridge

Prepared for Riccardo Lui | Documentation checked 17 November 2026

This is an original study curriculum grounded exclusively in official Databricks documentation and the attached official exam guide updated 6 August 2026. It is not an official Databricks training product or a reproduction of exam questions. Technical references appear beside the material they support and in the reference catalog. The notebook exercises, schedules, readiness rubric, and explanations are author-designed learning aids. The attached expanded study guide is background only; it is not treated as an authoritative technical source.

## How to use this kit

Read a chapter, open its official references, predict the lab result, then execute the companion notebook. Explain the result without looking at the solution. Repeat selected exercises with a deliberate defect and diagnose it using evidence. A notebook that runs once is weaker evidence of learning than a notebook whose rerun, error handling, and data grain you can explain.

The IPYNB files are standard Jupyter-format notebooks intended to run in Databricks. Import them into a workspace folder and attach compatible compute. Ordinary local Jupyter does not provide Unity Catalog, Auto Loader, Lakeflow, spark, or dbutils automatically. The kit uses synthetic data and existing writable catalogs, avoiding a dependency on sample-data downloads. References [R71], [R05], [R04].

Change CATALOG and PREFIX consistently in every notebook. Use an existing catalog you can write to. The default catalog name workspace is a convenience, not a universal Databricks guarantee. Notebook 00 creates three dedicated schemas, a managed volume, and initial tables. Subsequent core notebooks depend on those tables; ingestion experiments create their own isolated state paths. Use a personal prefix if several people share a workspace. References [R08], [R58].

### Execution and validation status

The kit is checked locally for notebook JSON structure, Python syntax, internal links, bundle YAML structure, task dependency integrity, and the synthetic-data answer contract. It has not been executed in your Databricks workspace: no workspace credentials or compute connection were supplied. Assertions in the notebooks are your runtime acceptance checks. Optional administrative and advanced features are clearly gated. Small performance examples verify correctness and plan reasoning; they do not establish production speedups.

## 1. Exam scope and learning route

The attached official August 2026 guide describes seven domains. The current certification page confirms the percentages below. Use the exam guide linked from that page again approximately two weeks before your examination, because objectives and supported features can change. References [R01].

| Domain | Weight | Core chapters | Main notebooks |
| --- | --- | --- | --- |
| Databricks Intelligence Platform | 6% | 2-3 | 00 |
| Data Ingestion and Loading | 21% | 4-6 | 04, 05, 06, 13 |
| Data Transformation and Modeling | 22% | 7-9 | 01, 02, 03, 07 |
| Working with Lakeflow Jobs | 16% | 10 | 08 and bundle sources |
| Implementing CI/CD | 10% | 11 | 09 and bundle project |
| Troubleshooting, Monitoring, Optimization | 10% | 12 | 11 |
| Governance and Security | 15% | 13 | 10 |

The current page lists 45 scored questions and 90 minutes; the attached newer guide allows possible additional unscored items. Current official certification FAQs do not publish a fixed passing score. Therefore the older attached practice exam's 32/45 rule should not be assumed to describe today's scoring policy. Treat that practice exam as a source of older-style fundamentals rather than the current blueprint. References [R01]; attached official exam guide, About the Exam.

### An eight-week route (suggested, not official)

| Week | Focus | Evidence to retain |
| --- | --- | --- |
| 1 | Platform, compute, UC paths, Delta fundamentals | Lab 00 plus your compute-selection explanations |
| 2 | COPY INTO, Auto Loader, schema evolution | Lab 04/05 rerun counts and a rescued-data example |
| 3 | Cleaning, nulls, joins, nested data | Labs 01/02; reconciliation from 8 events to 4 orders |
| 4 | Delta operations, streaming, declarative pipelines | Labs 03/06/07; recovery and quality-policy notes |
| 5 | Jobs branching, loops, scheduling | Both branch runs; a repaired failure |
| 6 | Git, CLI, bundle promotion | Commit SHA, dev/test runs, target comparison |
| 7 | Governance and performance diagnosis | Access test matrix; query-plan and task-metric evidence |
| 8 | Capstone, scenario review, weak spots | Rebuild unaided; review wrong answers with official references |

Suggested effort: 6-10 focused hours per week, adjusted to your experience. Your Teradata/BigQuery migration background is useful for joins, reconciliation, types, and validity logic; spend extra time on Databricks-specific state, governance, and deployment mechanics.

## 2. Platform architecture and compute decisions

### 2.1 What each component owns

The workspace is the collaboration and execution environment. An account can manage multiple workspaces and identities. Unity Catalog organizes governed assets in a metastore under catalog.schema.object. Workspaces attached to the same metastore can share governed data access. Distinguish the control plane from compute: classic compute runs in the customer cloud account, while serverless compute is managed in the Databricks account. Do not generalize an old classic-cluster diagram to every serverless deployment. References [R02].

Spark provides distributed execution; Delta supplies table storage reliability; Unity Catalog supplies governance; Lakeflow Connect supplies ingestion options; declarative pipelines manage dataset transformations; Jobs orchestrates tasks; bundles version and deploy resource definitions. These are complementary responsibilities. A successful Jobs run alone does not prove that a table has appropriate access controls. References [R72], [R07], [R13], [R32], [R37], [R46], [R58].

### 2.2 Choose compute by workload

| Need | Starting choice | Reason to investigate alternatives |
| --- | --- | --- |
| Interactive notebook development | Serverless notebook compute | Required unsupported libraries, APIs, networking, or settings |
| Scheduled production notebook ETL | Serverless Jobs, or compatible classic jobs compute | Runtime control, custom dependencies, policy requirements |
| Concurrent BI and ad hoc SQL | SQL warehouse | Validate warehouse features, concurrency and workload needs |
| Custom runtime or infrastructure control | Classic compute | More management and startup/configuration responsibility |
| Managed ingestion/transformation | Supported serverless pipeline | Connector, source, region, and pipeline requirements |

Compute has workload-dependent usage costs; classic infrastructure and Databricks usage charges must be considered together. Compare startup time, active runtime, concurrency, retries, and idle behavior rather than memorizing a cheapest universal option. Reference [R03].

Free Edition uses serverless compute and imposes usage/concurrency and network limits. Some enterprise administration labs cannot be completed there. In serverless notebooks/jobs, use supported DataFrame APIs and explicit AvailableNow streaming triggers for these exercises; RDD APIs and many Spark configuration changes are unavailable. Pipeline continuous modes have separate rules. References [R05], [R04].

### Check your understanding

A shared analyst workload should lead you toward a SQL warehouse; a scheduled notebook belongs in a Job. Explain which product starts the work and which compute executes it. Lab 00: identify table format, table type, catalog, schema, volume, and actual compute independently. References [R03], [R37], [R08].

## 3. Lakehouse layers and Delta fundamentals

Bronze retains source-shaped evidence; Silver enforces usable types and quality contracts; Gold serves analytical grains. These are quality roles, not mandatory schema names. A Bronze event can be legitimate source evidence even if it is rejected from Silver. Preserve a path to investigate bad records. Gold aggregates should declare their grain, such as one row per country per reporting period. Reference [R06].

Delta extends Parquet data with a transaction log, supporting ACID table operations and batch/stream processing. A Delta table is not merely a directory of independently editable Parquet files. Use supported table operations rather than modifying its files manually. A DataFrame is a query/data abstraction, not by itself a durable table. References [R07], [R18].

In the lab, eight raw rows include an exact duplicate and a correction to an order. Six pass the amount/timestamp/order rules, five distinct valid events remain, and four latest orders survive. Total current-order revenue is 220.00. An event-level sum has different semantics: the pipeline lab intentionally reports six valid event rows and 420.00. These numbers are synthetic acceptance criteria, not documentation examples.

## 4. Ingestion patterns and connector selection

### 4.1 Batch, incremental, and streaming are separate choices

Batch reads a bounded input. Incremental processing tracks what has already been consumed. A stream can run in micro-batches and stop after available input is processed, so it can deliver scheduled incremental behavior. Continuous execution and incremental logic are not synonyms. AvailableNow is useful when a Job should process currently available files and finish. References [R29], [R04].

Before choosing a tool, specify source type, change semantics, latency, initial/backfill volume, file count, schema drift, deletion handling, credentials, and recovery requirements. Determine whether you need to copy the data or query it where it already lives. References [R13], [R70].

| Situation | Candidate | Validate first |
| --- | --- | --- |
| Bounded SQL-driven file loads | COPY INTO | File tracking, schema, supported format, reload policy |
| High-volume incremental cloud files | Auto Loader | Discovery mode, state, schema policy, replay |
| Supported SaaS/database ingestion | Managed Lakeflow Connect connector | Source setup, change capture, limits and release state |
| Custom SQL/Spark ingestion logic | Standard APIs/connectors | Operational code, driver support, authentication |
| Partner integration fits the requirement | Supported partner connector | Ownership of retries, cursor, secrets and costs |
| Live remote access without copying | Lakehouse Federation | Pushdown, remote load, read-only behavior |

References [R09], [R10], [R13], [R16], [R70].

### 4.2 Managed versus custom responsibility

Managed Connect connectors combine UC-governed connections, ingestion pipelines, and destination tables. Managed database CDC connectors additionally use components such as an ingestion gateway and staging storage. Source prerequisites vary. Query-based connectors use queries rather than requiring database-log CDC; inspect their supported keys, incremental behavior, and deletion handling before choosing one. Do not assume every connector captures arbitrary updates and deletes. References [R13], [R14], [R15].

The standard API route offers more code-level control and source flexibility, but your solution must own more extraction and recovery logic. With an external client, distinguish direction: Spark reading a source database is different from an ODBC/JDBC application querying Databricks. A client connection that executes SELECT does not by itself persist a UC destination table. References [R16], [R75].

For custom REST extraction, define pagination, bounded retries, a stable source cursor, and an immutable raw landing contract. Keep credentials out of code and logs. Advance a durable extraction cursor only after the relevant output is safely committed; reason about retries spanning an API call and a table write. Lab 13 uses offline fixtures and labels live-source work separately. References [R17], [R16].

### 4.3 Files, JSON, and unstructured input

A UC volume governs files, including JSON, documents, images, or ingestion checkpoints; a table governs rows. A volume path is /Volumes/catalog/schema/volume/path. Nested JSON can become structs and arrays in a DataFrame, then be selected or exploded. Reading file content does not automatically define the business grain of the resulting dataset. References [R08], [R19].

## 5. COPY INTO and Auto Loader

### 5.1 COPY INTO

COPY INTO loads source files into a Delta target and skips previously loaded files by default. This supports repeatable file ingestion, but it does not remove the same business event arriving under another filename. A target can therefore be file-idempotent and still contain business duplicates. Lab 04 proves both properties by rerunning a load and then introducing a new file with an existing ID. Reference [R09].

The essential SQL shape is COPY INTO target FROM 'source_path' FILEFORMAT = JSON. Specify target schema or use documented schema-inference options intentionally. Understand the implications of forcing reloads. Choose file paths governed through approved storage access rather than embedding cloud credentials. References [R09], [R08].

### 5.2 Auto Loader state and execution

Auto Loader provides the cloudFiles Structured Streaming source for incremental file discovery. Reader schema state and stream checkpoint state have different responsibilities. Use a dedicated checkpoint for each query; keep it stable over normal restarts. Exactly-once ingestion guarantees depend on supported source/sink/state behavior and do not mean business-key deduplication across independently delivered files. References [R10], [R30].

Directory listing and file notifications are discovery strategies; AvailableNow controls query execution. Managed file events on external locations are the recommended discovery choice for many production workloads, while directory listing is convenient for a small permission-light lab. Neither mode guarantees file processing order. Reference [R12].

### 5.3 Schema decisions

| Reader mode | New column behavior | Operator response |
| --- | --- | --- |
| addNewColumns | Updates inferred schema, then fails the stream | Restart with same state; coordinate target evolution |
| rescue | Keeps schema stable and captures unexpected fields | Inspect rescued data and decide on a contract change |
| failOnNewColumns | Fails without automatic schema update | Fix source/schema deliberately |
| none | Does not evolve schema | Understand ignored versus rescued fields |

With an explicit schema, defaults differ from inferred-schema loading. CSV/JSON inference often uses strings unless configured otherwise. Reader-schema evolution and a Delta writer's mergeSchema are separate decisions. Newer widening modes have explicit runtime/release requirements; do not assume arbitrary changes such as integer to string are automatically safe. Reference [R11].

### Failure exercise

If a new field appears and the stream fails once, inspect whether schema evolution updated the schema location. Restarting can be correct for addNewColumns. Deleting the checkpoint is a different action that can replay old input. A silent rescue is also not an operational success unless the unexpected fields are monitored. References [R11], [R30].

## 6. Structured Streaming: progress, state, and recovery

A checkpoint records offsets, commits, metadata, and state for stateful queries. Starting with a new checkpoint starts a new logical query history. Reusing a checkpoint after incompatible stateful-query changes is not a general migration strategy. Changes to sources, sinks, and stateful operators have documented restart restrictions. Reference [R30].

Output mode determines what a sink receives: append emits new finalized rows; update emits changed result rows for compatible queries/sinks; complete emits the full result table for supported aggregations. Choose a source, query, mode, sink, and trigger combination the runtime supports. In lab 06 the source is append-only Delta and the sink receives appended rows; updates/deletes require a different change-processing design. Reference [R29].

A watermark bounds retained streaming state using event time. It is not a schedule or a promise that all old events are discarded at a precise wall-clock instant. Data within the supported lateness range is protected; older data is outside the guarantee. Stateful deduplication and stream joins require deliberate time/state policies. Reference [R31].

Checkpoint recovery and application idempotency are related but separate. If an external side effect or foreachBatch operation is retried, the application must avoid duplicate effects. For a Delta MERGE, source ordering, duplicate handling, and match conditions matter. The advanced extension asks you to design that contract rather than assume every write is exactly-once. References [R30], [R26].

## 7. PySpark and SQL transformation skills

### 7.1 DataFrames and execution

A DataFrame has named typed columns and a query plan. Transformations build new plans; actions such as count, show, collect, and writes require execution. Filter/project early when appropriate and prefer built-in expressions for common cleaning. A driver collection is suitable for a tiny known result, not an unbounded production dataset. References [R18], [R19], [R54].

Practice reading tables; select, filter, withColumn, withColumnRenamed, drop, split, and explode; and write explicit Silver outputs. Know which operations change columns, which change row count, and which change grain. To unpack an array, explain why explode can remove a row with an empty/null array while explode_outer retains a placeholder row. References [R19], [R74].

### 7.2 Data types and null semantics

Malformed casts can raise errors under ANSI behavior. Use try_cast when invalid input should become an explicit quality failure rather than silently breaking a whole batch. Preserve identifiers with leading zeroes as strings. Use DECIMAL precision/scale for the lab money contract and explicit timestamps/time zones for reproducibility. References [R04], [R19].

Ordinary comparisons with NULL return unknown. A filter keeps true rows; unknown is not true. Use IS NULL for missingness, coalesce for a documented fallback, and <=> or eqNullSafe for null-safe equality. count(*) counts rows, while count(column) excludes NULL values. A null-safe difference is useful in migration reconciliation: NOT(a <=> b). Reference [R25].

Do not replace unknown money with zero merely to satisfy a type requirement. In the kit, malformed and negative amounts go to quarantine; absent or unrecognized customer IDs remain valid orders for later enrichment. Those are explicit teaching business rules, not universal platform defaults.

### 7.3 Joins and reconciliation

An inner join retains matching keys. A left join retains all left rows and fills unmatched right attributes with NULL. Multiple right matches multiply a left row, so uniqueness of the dimension key matters. Use multi-column join keys when the business key is composite. A cross join creates the Cartesian product. A broadcast hint changes the execution strategy and requires the broadcast side to be appropriately small. Reference [R20].

After a left join, WHERE right.country='IT' eliminates unmatched rows. A condition in ON has different preservation behavior. Diagnose counts at each join before adding DISTINCT; otherwise duplicates may hide a bad relationship. Lab 02 deliberately introduces a duplicate dimension row to expose fanout. Reference [R20].

### 7.4 Union and deduplication

DataFrame union appends rows by column position and preserves duplicates. SQL UNION ALL preserves duplicates; SQL UNION removes duplicate full rows. DataFrame unionByName aligns columns by name, optionally filling missing columns with NULL. Match types intentionally and do not confuse combining datasets with joining them. References [R21], [R22].

Exact-row distinctness differs from current-state selection. dropDuplicates on a key does not encode which version should win. For a deterministic latest row, use row_number over a key partition with a total descending sequence/timestamp/tie-break ordering. Lab 01 removes exact duplicates, then keeps the latest order event. References [R23], [R24].

### 7.5 Aggregation and dimensional modeling

Practice count, count distinct, approx_count_distinct, mean, sum, grouping and summary. Approximate counts trade precision for scale; they are unsuitable when an acceptance check requires an exact business count. Declare whether your fact is an event or a current entity snapshot before aggregating. A dimension join that fans out a fact can overstate revenue. References [R74], [R20].

For the kit, latest-order fact grain is one row per order ID. Customer is a dimension. Country revenue is a Gold summary with one row per country bucket. Mapping unknown customers to UNKNOWN preserves all valid-order money; discarding them would give a different analytical contract. Lab 02 checks total revenue and the unmatched rows explicitly.

## 8. Delta DDL, DML, and retention

Know CREATE TABLE, CREATE TABLE AS SELECT, CREATE OR REPLACE TABLE, INSERT INTO, UPDATE, DELETE and MERGE in context. IF NOT EXISTS preserves an existing object; replacing an object is not the same intention. Use the UC namespace to reference tables rather than their internal storage path. References [R07], [R59].

MERGE matches source and target and applies selected update/insert/delete actions. It is not automatic deduplication: multiple source matches can make an update ambiguous, and duplicate source rows can also produce duplicate new rows. The lab uses a unique source and a sequence guard so replaying the same update does not overwrite newer state. Runtime-specific duplicate-match behavior should be checked in the command documentation. Reference [R26].

DESCRIBE HISTORY shows operations and versions. VERSION AS OF reads an earlier state. RESTORE writes a new version based on an earlier state. Required historical files and log history must still exist. A long log retention setting alone does not retain all data files; history and file-retention thresholds are separate. Reference [R27].

VACUUM removes obsolete data files beyond the retention threshold; it is not file compaction. The default data retention threshold is seven days. OPTIMIZE is a layout/compaction operation. Choose retention from recovery, readers, and streaming outage requirements. Lab 03 uses VACUUM DRY RUN and never disables retention protection. References [R28], [R56].

## 9. Declarative pipelines and serving objects

Declarative pipelines let you declare datasets and dependencies while the service manages pipeline execution. Current Python examples import pipelines as dp from pyspark. Dataset definition functions return DataFrames; avoid inserting actions and side effects into functions that the framework can evaluate during planning. Older dlt examples appear in historical material, while this kit uses the current documented interface. References [R32], [R33].

| Object | What persists | How results change | Good fit |
| --- | --- | --- | --- |
| Regular table | Rows/data plus metadata | Explicit supported writes | Controlled ingestion or curated output |
| View | Query definition | Query evaluates against source | Reusable lightweight logic |
| Materialized view | Precomputed query results | Managed refresh | Expensive reusable analytics |
| Streaming table | Incremental table output | Pipeline flows process input incrementally | Ingestion and stream processing |

Materialized views maintain query results as of refresh; some queries/workloads use full refresh instead of incremental refresh. A streaming table's incremental handling does not mean that upstream historical data is automatically recomputed after every transformation change. Use documented full-refresh/reprocessing semantics when needed. References [R35], [R36].

Expectations express row-level data checks. Retain-and-report, drop invalid records, and fail the update are distinct policies. Select the policy from downstream correctness requirements; track bad-row counts and reasons. A drop policy needs a separate quarantine design if invalid records must be retained for remediation. Reference [R34].

In lab 07, the streaming output validates incoming events, and the materialized view summarizes those valid events. It intentionally does not perform latest-order deduplication. Explain why its 420.00 event sum and the Silver latest-order total 220.00 answer different questions before extending the pipeline.

## 10. Lakeflow Jobs orchestration

### 10.1 Tasks, dependencies, and parameters

A Job coordinates tasks in a directed acyclic graph. Notebook, SQL, pipeline, and dashboard tasks invoke different assets with their own compute and permissions. An edge defines dependency behavior; it does not guarantee the upstream notebook's data passed all quality checks unless those checks are part of the task. References [R37], [R43].

Separate three parameter mechanisms: ${var.catalog} is a bundle deployment substitution; {{job.parameters.join_type}} is a Job runtime reference; {{tasks.quality.values.valid_rows}} references a value produced by another task. Pass resolved runtime references through notebook parameters and retrieve them through widgets. Task values are small JSON-serializable metadata, not a way to transfer a DataFrame. References [R48], [R40], [R41].

### 10.2 Conditional tasks and loops

An If/else condition evaluates two operands. Its true and false successors need the appropriate outcome dependency. Otherwise merely placing a condition task upstream does not identify which branch should execute. Equality/inequality operands use string comparison; ordering comparisons use numeric comparison. Inspect evaluated expressions in run details when a branch seems ignored. Reference [R38].

The bundle tests join_type equal to left; quality first rejects unsupported parameter values. Left and inner branches share one output table because they are exclusive, and overlapping Job runs are limited. Publish waits for the branches with AT_LEAST_ONE_SUCCESS. The For each task receives a JSON array and passes the current item's country to its nested notebook. It cannot directly nest another For each. References [R38], [R39], [R73].

### 10.3 Scheduling and recovery

Choose scheduled triggers for calendar requirements, file arrival for unpredictable file deliveries, and table update for table-driven dependencies. A continuous Job schedules another run after the prior one; it is not identical to a continuously executing streaming query. Validate supported source locations, permissions, and feature constraints for each trigger. Reference [R42].

Configure retries for recoverable transient failures and make writes replay-safe. A task timeout terminates overlong execution; a warning threshold produces an observability signal. An upstream failure or excluded branch can prevent a downstream task from running. Repair/retry history should be inspected in the Job run view instead of interpreting every skipped task as a notebook failure. References [R43], [R44].

### Hands-on acceptance

Lab 08 succeeds only after both left and inner runs have been inspected, with 4 and 2 output rows respectively. Also submit evidence of one deliberately failed validation, its blocked downstream tasks, and a corrected repair. The files are provided; no job has been deployed into your account by this kit.

## 11. Git, bundles, and CI/CD

Git folders connect workspace development to remote Git. Practice cloning, branch creation/switching, diff review, commit, push, pull, and conflict resolution. Separate developer folders avoid one person's branch switch disrupting another. Pull request review and merge happen through the linked Git workflow/provider. Source control does not by itself deploy a Job or promote a data schema. Reference [R45].

Declarative Automation Bundles, previously Databricks Asset Bundles, describe code plus workspace resources for repeatable deployment. The root databricks.yml can include resource files. This kit defines one Job; pipeline source files are provided for a separate guided pipeline lab. References [R46], [R47].

Variables and target overrides let the same code use different catalogs, schemas, names, or other settings. Dev/test/prod are target names, while development/production are deployment modes with defined behaviors. A target named test can use production mode to avoid development defaults. Do not assume a production mode is a substitute for reviewed access, identity, and data isolation. References [R48], [R49].

A practical promotion sequence is: review code, run relevant tests, validate configuration, deploy dev, run data acceptance checks, deploy test, review evidence, deploy the approved revision to prod. The commands validate, deploy and run have different jobs. Configuration validation cannot prove source connectivity or output correctness. Reference [R51].

For personal practice, use supported user authentication. For CI automation, use an authorized machine identity or supported identity federation. Keep deployment identity separate conceptually from the identity that runs data operations. Do not store access tokens in notebooks or YAML. Reference [R50].

Secret management is a separate concern. Injecting a bundle variable from an environment variable avoids committing a literal but is not encryption and does not make deployment state a secret store. Prefer approved runtime secret retrieval or a governed connection. The attached sample's environment-variable answer should not be expanded into a claim that all bundle-variable use is confidential. References [R17], [R48].

## 12. Monitoring and optimization

### 12.1 Start with evidence

Use Job history to compare current duration with a relevant baseline, and separate waiting/startup time from execution. Inspect task state and upstream dependencies. Compare input size and business changes before declaring a regression. Where available, use system.lakeflow and billing data for cross-run/cost analysis with the required privileges. Reference [R44].

On classic Spark workloads, locate the longest stage, then inspect task duration distribution, shuffle read/write, spill, and failures. A high max/median task disparity points toward skew; many spilling tasks may indicate large partitions or insufficient memory per core. Serverless notebook/job diagnostics differ and do not expose every classic UI or setting. References [R52], [R53], [R04].

### 12.2 Match the intervention to the bottleneck

| Evidence | Hypothesis | Candidate action to test |
| --- | --- | --- |
| Few very slow tasks with huge input | Skewed keys/partitions | Review keys; preaggregate; correct salting where appropriate |
| Large broadcast or executor OOM | Join-side memory pressure | Remove inappropriate broadcast; reduce input; reassess strategy |
| Many spilling tasks | Oversized partitions/memory pressure | Adjust partitions or memory per core; reduce row width |
| Driver OOM around collect | Too much local result data | Aggregate/filter before collection; avoid full driver materialization |
| Failure before work begins | Compute/environment issue | Inspect events, permissions, networking and library versions |
| Changed row counts after a join | Data relationship defect | Check key uniqueness and join/filter logic |

References [R53], [R54], [R52], [R20].

AQE adapts physical execution using observed statistics, including coalescing shuffle partitions, join changes, and skew-join handling. It is not a universal repair for skewed aggregations. Salting a decomposable SUM needs two aggregation stages; an average needs sum and count, and a distinct count needs additional reasoning. Lab 11 verifies equal results rather than promising a speedup. Reference [R55].

### 12.3 Parameters to recognize

| Parameter | What it influences | Caution |
| --- | --- | --- |
| spark.sql.shuffle.partitions | SQL shuffle partitioning | Too few increases per-task work; too many adds overhead |
| spark.default.parallelism | Default parallelism for applicable Spark operations | Not a replacement for SQL shuffle configuration |
| spark.executor.memory | Executor process memory | Compute configuration, skew and per-core memory matter |
| spark.driver.memory | Driver process memory | Does not enlarge executor memory or justify unbounded collect |
| spark.sql.autoBroadcastJoinThreshold | Eligibility for automatic broadcast | Forcing a large broadcast can cause memory failure |

Use compatible compute configuration and read current defaults/overrides; serverless limits configurability. Re-measure representative workload duration, shuffle, spill and cost after one change. References [R18], [R54], [R55], [R04], [R76], [R77].

Liquid clustering organizes table data by chosen clustering keys and replaces traditional partitioning/ZORDER for supported tables. It supports changing clustering keys over time. It is a layout technique, distinct from Spark task partitioning. Automatic clustering has its own requirements. Reference [R56].

Predictive optimization automates eligible UC managed-table maintenance such as OPTIMIZE, VACUUM and ANALYZE. Understand eligibility and retained-history implications rather than scheduling unnecessary duplicate maintenance. Neither clustering nor automatic maintenance corrects a business-key fanout or an invalid deduplication rule. Reference [R57].

## 13. Unity Catalog governance and security

### 13.1 Object hierarchy and lifecycle

UC privileges apply to principals and securable objects. A table reader normally needs USE CATALOG, USE SCHEMA, and SELECT on the table. Storage-file privileges and volume privileges govern different access paths; granting table SELECT does not imply permission to list arbitrary cloud files. Apply least privilege at the appropriate hierarchy level. Reference [R58].

A managed table lets UC manage storage and maintenance. An external table uses a specified authorized location and retains its underlying files when the table metadata is dropped. It remains UC-governed for Databricks access; external file access outside Databricks needs independent cloud controls. A managed table also lives in cloud storage: managed/external does not mean internal/external to the cloud. References [R59], [R60].

External-to-managed Delta conversion can use ALTER TABLE ... SET MANAGED under documented requirements. ALTER TABLE ... UNSET MANAGED is a rollback of that conversion within a 14-day window, not a general-purpose command to convert any managed table to an arbitrary external path. Check runtime, writer compatibility, data retention, and downstream consumers before conversion. Reference [R61].

### 13.2 Grants and effective access

GRANT adds a privilege; REVOKE removes a particular grant. Effective access can still come from group membership or inheritance. Account groups are appropriate reusable principals for data policy. Service principals represent automation identities. Separate permissions on a Job/notebook from permissions to the UC data it uses. Reference [R58].

In lab 10, the grant pattern is USE CATALOG on the chosen catalog, USE SCHEMA on the chosen Silver schema, and SELECT on one disposable demo table. After REVOKE, verify access under the intended identity and check alternate grants. An owner-only query is not a complete access test. Reference [R58].

### 13.3 Row filters, masks, and ABAC

A row filter is a Boolean SQL UDF applied to selected table columns; it controls which rows are visible. A column mask returns the value visible to a user. Match function parameter types to bound columns and verify supported compute. The kit tests is_account_group_member with an account group and uses synthetic email data. References [R62], [R63].

ABAC applies policies centrally using governed tags and scope rather than independently configuring each table. It is useful for consistent masking/filtering across many tagged objects. Tags identify policy targets; the policy and function enforce the behavior. Test multiple identities and new tagged objects, and verify who can change tags or policies. References [R64], [R65].

The exam outline uses the word DENY, but do not assume generic DENY SELECT syntax. Current official ABAC DENY policies are Beta and support denying MANAGE ACCESS CONTROL on supported securables; the documentation explicitly limits the supported privilege. Read current requirements before using the feature. Access restriction, privilege administration, row filtering, and masking solve distinct problems. Reference [R66].

### 13.4 Lineage and evidence

UC captures supported query lineage across governed objects and attached workspaces, including column-level lineage for supported paths. Use it for impact analysis and upstream investigation, while respecting visibility permissions and documented limitations. In the lab, find Bronze -> Silver -> Gold relationships and explain which transformation introduced a business metric. Reference [R67].

## 14. Advanced bridge for later study

These extensions prepare deeper engineering judgment. They are not an exhaustive Professional exam guide or a claim about any future certification's objectives. Finish the Associate acceptance checks first, then use the official references below to deepen one topic at a time.

### 14.1 CDF, CDC, and slowly changing dimensions

CDF exposes row changes plus metadata. Current documentation distinguishes automatic CDF from the explicitly enabled legacy Delta CDF mechanism. Lab 12 chooses the latter for a controlled experiment and shows insert, update pre/postimages, and delete. CDF history is retention-bound, so durable replay/audit needs a deliberate archival strategy. Reference [R68].

AUTO CDC supports ordered change processing and SCD patterns. Type 1 maintains current attributes; Type 2 preserves versions and validity boundaries. AUTO CDC replaces older APPLY CHANGES terminology in current recommendations. A sequence field is essential for out-of-order events. Review keys, deletes, null handling, ordering ties, and late-change retention. Reference [R69].

Project extension: ingest synthetic customer updates with sequences 1, 3, then 2. Verify that a late older event does not simply overwrite the latest state. For Type 2, validate effective ranges and identify the current row. Connect this to the validity-from/to comparisons you use in migration transformers, but implement Databricks semantics from the official API rather than copying another platform's assumptions.

### 14.2 Stateful streaming and recovery design

Measure lateness before choosing watermarks; budget state and recovery duration. Plan checkpoint changes, schema changes, and reprocessing with compatible query definitions. Build a replay drill in a separate target before altering production state. References [R31], [R30].

### 14.3 Performance engineering

Compare query plans and representative input, including skew, file counts, and variable join selectivity. Benchmark repeated runs with a stated compute/environment and inspect physical evidence. Separate algorithm changes from layout and scaling changes. Review whether SQL built-ins can replace costly custom logic. References [R52], [R54], [R55], [R56].

### 14.4 Production delivery and governance

Extend the bundle with authorized run identities, narrowly scoped permissions, automated data tests, and reviewed target configuration. Add pipeline resources only after their standalone definitions work. Design central policy/tag ownership and verify ingestion identities cannot bypass intended access. References [R46], [R50], [R65], [R73].

### 14.5 Migration and federation

Lakehouse Federation can query supported remote sources through governed foreign catalogs. This is different from copying data into a managed Delta table with Lakeflow Connect. In your Teradata/BigQuery context, compare remote-query access, backfill, recurring incremental replication, and final cutover as separate designs. Reference [R70].

Advanced exercise: define a common extraction cutoff, normalize types deliberately, compare counts by source code/date, check join fanout, then compare detailed business keys and null-safe values. Preserve meaningful leading zeroes, decimal scale rules and timestamp semantics. The kit's join and type exercises are a foundation for that reconciliation design. References [R19], [R20], [R25], [R26].

## 15. Objective coverage matrix

This maps every topic in the attached August 2026 outline to learning and evidence. A guided/admin exercise is deliberately distinguished from an executable synthetic-data lab. References are the official technical sources, not third-party exam banks.

| Outline topic | Guide/lab evidence | References |
| --- | --- | --- |
| Architecture, Delta, UC | Ch 2-3; 00/03/10 | R02,R07,R58 |
| Compute characteristics and costs | Ch 2; Free/serverless checks | R03,R04,R05 |
| Batch/stream/incremental; local files | Ch 4; 00/04/06 | R08,R09,R29 |
| COPY INTO | 04 rerun and new-file counts | R09 |
| Auto Loader inference/evolution/discovery | 05 rescue and opt-in evolution | R10,R11,R12 |
| Managed Connect reliability/setup | 13 guided external-source exercise | R13,R14,R15 |
| JDBC/ODBC/REST clients | Ch 4; 13 optional JDBC/ODBC, REST fixture | R16,R17,R75 |
| Select ingestion method/partner options | Ch 4 comparison; 13 scenarios | R13,R16,R70 |
| Nested/semi/unstructured data | 00 JSON; 02 explode; volumes | R08,R19 |
| Cleaning/nulls/types to Silver | 01 quarantine and explicit contract | R19,R25 |
| Inner/left/broadcast/multikey/cross/union | 02 assertions and fanout | R20,R21,R22 |
| Column and row manipulation | 01/02 select, filter, rename, split, explode | R19 |
| Dedup/count/approx/mean/summary | 01 deterministic latest + summaries | R23,R24,R74 |
| Basic Spark tuning parameters | Ch 12; 11 opt-in classic exercise | R18,R54,R55 |
| Gold views/tables/MVs/streaming tables | 02/07 grain comparison | R35,R36 |
| Data quality | 01 quarantine; 07 expectations | R34 |
| Retries/branching/looping | 08; complete executable bundle DAG | R38,R39,R43 |
| Notebook/SQL/dashboard/pipeline tasks | 08 executable notebooks + UI extensions | R43 |
| Schedule/file/table triggers | Ch 10; 08 trigger selection | R42 |
| Time versus data triggers | 08 scenario explanations | R42 |
| Git branches/commit/push/PR | 09 guided Git workflow | R45 |
| Bundle variables/overrides | 09; dev/test/prod target YAML | R48,R49 |
| Bundle resource deployment | 09 executable Job; 07 pipeline code | R46,R47,R73 |
| CLI validate/deploy/manage | 09 terminal commands | R50,R51 |
| Job runtime baselines/history | 08/11 monitoring evidence | R44 |
| Status/task graph/failure rates | 08 failure and repair exercise | R43,R44 |
| Spark UI skew/shuffle/spill | 11 metrics exercise; Ch 12 cases | R52,R53,R54 |
| Liquid clustering/predictive optimization | 11 optional clustering; Ch 12 | R56,R57 |
| Startup/library/OOM diagnosis | Ch 12 diagnostic table; 11 | R52,R54 |
| Managed/external/create/convert/drop | 10 sandbox + admin conversion | R59,R60,R61 |
| UI/SQL privileges/GRANT/REVOKE/DENY | 10 templates and DENY limits | R58,R66 |
| Row security/column masks | 10 opt-in synthetic policies | R62,R63 |
| UC ABAC | 10 guided central-tag policy exercise | R64,R65 |

## 16. Original scenario review with explanations

These are author-written learning checks, not actual or reconstructed exam questions. First answer without references; then read the rationale and the linked official source. A suggested learning target is at least 85% across two different practice sets, but this is not an official pass threshold.

### Ingestion and state

1. You run COPY INTO twice on the same immutable files, then upload the same customer event under a new filename. What must you verify? Answer: prior-file skipping and business-key duplication separately. New files are eligible even if their content represents an existing event. Reference [R09].

2. Auto Loader rescue mode receives an extra field. Should you expect a new top-level target column? Answer: inspect _rescued_data; rescue keeps the schema stable. Reference [R11].

3. An operator deletes a checkpoint but keeps the destination table. What is at risk? Answer: the new query history can reprocess existing source input and duplicate application-level output. Reference [R30].

4. A serverless notebook stream errors before processing with an unsupported infinite trigger. What should you review? Answer: use a supported explicit trigger such as AvailableNow for this lab; pipeline continuous processing has separate support. Reference [R04].

### Transformation and modeling

5. A left join increases row count. Is Spark necessarily wrong? Answer: no; multiple matching dimension rows cause fanout. Check right-key uniqueness and intended grain. Reference [R20].

6. unionByName produces duplicate rows. Is it broken? Answer: no; name alignment does not imply deduplication. Reference [R22].

7. You need the latest correction per order. Is key-only dropDuplicates sufficient? Answer: it does not specify the winning record. Use ordered row_number with deterministic ties. References [R23], [R24].

8. Comparing nullable source/target values with a<>b misses some differences. Why? Answer: ordinary comparisons can return unknown. Use a deliberately null-safe comparison, such as NOT(a <=> b). Reference [R25].

9. A materialized view is stale immediately after a source write. What do you check? Answer: refresh timing/state; its maintained result is current as of refresh, unlike a normal view evaluated when queried. Reference [R35].

### Jobs and deployment

10. Both join notebooks run even though an If/else task exists. Where do you look? Answer: outcome dependencies on true/false and the evaluated operands; a dependency edge alone does not identify the branch outcome. Reference [R38].

11. A notebook contains the literal text {{job.parameters.join_type}} and does not resolve it. Why? Answer: dynamic references belong in Job configuration fields and should be passed as parameters. Reference [R40].

12. A task warns at 30 minutes but must be terminated at 90. Which settings are distinct? Answer: warning threshold versus timeout; idle compute auto-termination is another concept. Reference [R43].

13. CLI validate passes, then the Job fails reading a table. Is the validation inconsistent? Answer: configuration validation is not proof of runtime UC privileges or data availability. References [R51], [R58].

14. Test and prod need different catalogs. Should you fork notebook logic? Answer: use variables/target overrides and deploy the same tested revision. Reference [R48].

### Operations and governance

15. Most tasks finish fast but one aggregation partition is enormous. Will adding executors necessarily fix it? Answer: one hot partition can remain the bottleneck. Inspect skew and consider a mathematically correct distribution/preaggregation strategy. References [R53], [R55].

16. A driver crashes after collecting all rows. Which component's memory matters first? Answer: the driver; reduce collection rather than assuming more executor memory solves it. Reference [R54].

17. A user has SELECT but cannot query a table. What else is needed? Answer: verify USE CATALOG, USE SCHEMA, bindings, and effective identity/access. Reference [R58].

18. Dropping an external table leaves files behind. Is that a failure? Answer: this is the documented external-table lifecycle. Reference [R60].

19. Can UNSET MANAGED turn any managed table into an external table at any time? Answer: it is a documented rollback for an eligible earlier conversion within its window. Reference [R61].

20. Can you mask sensitive columns with a general DENY SELECT statement? Answer: use masks/ABAC for visibility. Current ABAC DENY has its own restricted privilege scope and Beta requirements. References [R62], [R66].

## 17. Capstone and readiness checklist

Rebuild the lab from a fresh personal prefix without reading solution cells. Record the environment, source contract, each table grain, quality counts, retained input/state paths, and chosen trigger. Demonstrate both Job branches, target isolation, and a failure/repair. Show where monitoring would reveal drift, duplicate files, rejected records, and performance regressions. The notebook 13 rubric scores evidence, not memorization.

A reasonable readiness gate is being able to explain each objective, execute the associated core exercise, and diagnose a deliberate failure using official documentation. For admin-only features, describe the exact requirements and provide a test plan; do not claim a multi-user access test you could not perform.

Before booking or taking the exam, revisit the current certification page and linked exam guide. Resolve any terminology or feature discrepancy with the current official docs and the guide for your exam date. Reference [R01].

## 18. Official reference catalog

All technical references below are Databricks-owned pages. Most use AWS documentation URLs for a consistent reference set; use the documentation cloud selector for your Azure/GCP workspace and verify cloud-specific source setup, networking, release state and feature requirements. Platform features evolve independently from the exam blueprint. Documentation checked 17 November 2026.

### R01 - Certification and current exam outline

https://www.databricks.com/learn/certification/data-engineer-associate

### R02 - High-level architecture

https://docs.databricks.com/aws/en/getting-started/high-level-architecture

### R03 - Compute

https://docs.databricks.com/aws/en/compute/

### R04 - Serverless compute limitations

https://docs.databricks.com/aws/en/compute/serverless/limitations

### R05 - Free Edition limitations

https://docs.databricks.com/aws/en/getting-started/free-edition-limitations

### R06 - Medallion architecture

https://docs.databricks.com/aws/en/lakehouse/medallion

### R07 - Delta Lake

https://docs.databricks.com/aws/en/delta/

### R08 - Unity Catalog volumes

https://docs.databricks.com/aws/en/volumes/

### R09 - COPY INTO tutorial

https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/copy-into

### R10 - Auto Loader

https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader

### R11 - Auto Loader schema inference and evolution

https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/schema

### R12 - Auto Loader file detection modes

https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/file-detection-modes

### R13 - Lakeflow Connect concepts

https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/

### R14 - Managed database connectors

https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/cdc-overview

### R15 - Query-based connectors

https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/query-based-overview

### R16 - Spark data sources

https://docs.databricks.com/aws/en/connect/spark-data-sources

### R17 - Secret management

https://docs.databricks.com/aws/en/security/secrets/

### R18 - PySpark overview

https://docs.databricks.com/aws/en/pyspark/

### R19 - PySpark basics

https://docs.databricks.com/aws/en/pyspark/basics

### R20 - DataFrame joins

https://docs.databricks.com/aws/en/pyspark/reference/classes/dataframe/join

### R21 - DataFrame union

https://docs.databricks.com/aws/en/pyspark/reference/classes/dataframe/union

### R22 - DataFrame unionByName

https://docs.databricks.com/aws/en/pyspark/reference/classes/dataframe/unionByName

### R23 - dropDuplicates

https://docs.databricks.com/aws/en/pyspark/reference/classes/dataframe/dropDuplicates

### R24 - row_number

https://docs.databricks.com/aws/en/pyspark/reference/functions/row_number

### R25 - NULL semantics

https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-null-semantics

### R26 - Delta MERGE

https://docs.databricks.com/aws/en/delta/merge

### R27 - Table history and time travel

https://docs.databricks.com/aws/en/tables/history

### R28 - VACUUM

https://docs.databricks.com/aws/en/tables/operations/vacuum

### R29 - Structured Streaming concepts

https://docs.databricks.com/aws/en/structured-streaming/concepts

### R30 - Streaming checkpoints

https://docs.databricks.com/aws/en/structured-streaming/checkpoints

### R31 - Watermarks

https://docs.databricks.com/aws/en/structured-streaming/watermarks

### R32 - Lakeflow pipelines

https://docs.databricks.com/aws/en/ldp/

### R33 - Develop pipelines in Python

https://docs.databricks.com/aws/en/ldp/developer/python-dev

### R34 - Pipeline expectations

https://docs.databricks.com/aws/en/ldp/expectations

### R35 - Materialized views

https://docs.databricks.com/aws/en/ldp/concepts/materialized-views

### R36 - Streaming tables

https://docs.databricks.com/aws/en/ldp/concepts/streaming-tables

### R37 - Lakeflow Jobs

https://docs.databricks.com/aws/en/jobs/

### R38 - If/else tasks

https://docs.databricks.com/aws/en/jobs/tasks/if-else

### R39 - For each tasks

https://docs.databricks.com/aws/en/jobs/tasks/for-each

### R40 - Dynamic value references

https://docs.databricks.com/aws/en/jobs/dynamic-value-references

### R41 - Task values

https://docs.databricks.com/aws/en/jobs/task-values

### R42 - Job triggers

https://docs.databricks.com/aws/en/jobs/triggers

### R43 - Configure job tasks and timeouts

https://docs.databricks.com/aws/en/jobs/configure-task

### R44 - Monitor Jobs

https://docs.databricks.com/aws/en/jobs/monitor

### R45 - Git folders operations

https://docs.databricks.com/aws/en/repos/git-operations-with-repos

### R46 - Declarative Automation Bundles

https://docs.databricks.com/aws/en/dev-tools/bundles/

### R47 - Bundle configuration

https://docs.databricks.com/aws/en/dev-tools/bundles/settings

### R48 - Bundle variables

https://docs.databricks.com/aws/en/dev-tools/bundles/variables

### R49 - Bundle deployment modes

https://docs.databricks.com/aws/en/dev-tools/bundles/deployment-modes

### R50 - CLI authentication

https://docs.databricks.com/aws/en/dev-tools/cli/authentication

### R51 - Bundle CLI commands

https://docs.databricks.com/aws/en/dev-tools/cli/bundle-commands

### R52 - Spark UI diagnosis

https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/

### R53 - Skew and spill

https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/long-spark-stage-page

### R54 - Spark memory issues

https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/spark-memory-issues

### R55 - Adaptive query execution

https://docs.databricks.com/aws/en/optimizations/aqe

### R56 - Liquid clustering

https://docs.databricks.com/aws/en/tables/clustering

### R57 - Predictive optimization

https://docs.databricks.com/aws/en/optimizations/predictive-optimization

### R58 - UC privileges reference

https://docs.databricks.com/aws/en/data-governance/unity-catalog/access-control/privileges-reference

### R59 - UC managed tables

https://docs.databricks.com/aws/en/tables/managed

### R60 - External tables

https://docs.databricks.com/aws/en/tables/external

### R61 - Convert to managed tables

https://docs.databricks.com/aws/en/tables/convert-to-managed

### R62 - Table-level row filters and masks

https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks/

### R63 - Apply row filters and masks

https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks/manually-apply

### R64 - ABAC overview

https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac/

### R65 - ABAC policy creation

https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac/policies

### R66 - ABAC DENY policies (Beta)

https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac/deny-policies

### R67 - Unity Catalog lineage

https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-lineage

### R68 - Change data feed

https://docs.databricks.com/aws/en/tables/features/change-data-feed

### R69 - AUTO CDC

https://docs.databricks.com/aws/en/ldp/cdc

### R70 - Lakehouse Federation

https://docs.databricks.com/aws/en/query-federation/

### R71 - Import/export notebooks

https://docs.databricks.com/aws/en/notebooks/notebook-export-import

### R72 - Spark overview

https://docs.databricks.com/aws/en/spark/

### R73 - Bundles resource reference

https://docs.databricks.com/aws/en/dev-tools/bundles/resources

### R74 - DataFrame reference

https://docs.databricks.com/aws/en/pyspark/reference/classes/dataframe

### R75 - Python ODBC client

https://docs.databricks.com/aws/en/dev-tools/pyodbc

### R76 - Set Spark configuration

https://docs.databricks.com/aws/en/spark/conf

### R77 - Classic compute best practices

https://docs.databricks.com/aws/en/compute/cluster-config-best-practices
