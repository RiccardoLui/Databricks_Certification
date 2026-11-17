# Deploy the training job

Official documentation: [Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/), [CLI commands](https://docs.databricks.com/aws/en/dev-tools/cli/bundle-commands), [authentication](https://docs.databricks.com/aws/en/dev-tools/cli/authentication), [If/else](https://docs.databricks.com/aws/en/jobs/tasks/if-else), [For each](https://docs.databricks.com/aws/en/jobs/tasks/for-each).

1. Complete notebooks 00 and 01 for the target catalog/prefix. Dev defaults to workspace.dea_riccardo_silver and workspace.dea_riccardo_gold. Choose a catalog that actually exists.
2. Set variables in databricks.yml. Add workspace.host under each target, for example `workspace: {host: https://YOUR-WORKSPACE-HOST}`. Authenticate to the matching workspace.
3. From this directory run the commands below individually. The job uses serverless notebook compute. In a workspace without supported serverless Jobs, configure compatible classic job compute using the current resource schema before deployment.

```bash
databricks auth login --host https://YOUR-WORKSPACE-HOST
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run -t dev orders_job --params join_type=left
databricks bundle run -t dev orders_job --params join_type=inner
```

Expected branch row counts: left=4, inner=2. Inspect branch outcomes and publish's AT_LEAST_ONE_SUCCESS dependency. `quality` rejects any other join_type. Max concurrent runs is 1 because both branches use one target table. For each creates separate IT/FR result tables.

Test/prod targets use distinct prefixes; run 00/01 with those prefixes first. These are training target examples, not a production deployment recommendation. Production promotion should use an authorized automation identity and reviewed run_as/permissions configuration appropriate to your organization. No production identity, schedules, secrets, external infrastructure, or pipeline resource is provisioned by this bundle. Lab 07 creates its pipeline separately so it also works without CLI access.

Validate is necessary but not runtime validation. The supplied YAML has been parsed and its dependencies checked locally; CLI validation/deployment must be performed in your workspace. Use a current CLI compatible with the linked schema. Do not deploy over an unrelated existing job.
