# draw-io: aws-icons.md name check (analyst scratch, 2026-11-15)

Method: every distinct `mxgraph.aws4.<name>` in `skills/draw-io/references/aws-icons.md` at the batch BASE was looked up in two vendor sources:

- `jgraph/drawio` `src/main/webapp/js/diagramly/sidebar/Sidebar-AWS4.js`, last changed 2026-09-08 (commit f3abfe0f082c18f7b4fee8a34c2d07b1987687fd): the editor's AWS4 palette.
- `jgraph/drawio-mcp` `shape-search/search-index.json` at commit cfc1b916b9deaa7c78d23d719d4124bd76d2d0bf (2026-11-11): the vendor's shape search index (10800 entries, 1023 distinct aws4 names).

Counts: 470 distinct names; not in the palette 111; not in the search index 94; in neither 92.

A name missing from one source may still render (the palette and the index are generated differently); a name in neither is unverified and should be treated as stale until a lookup says otherwise. Candidates are fuzzy matches against the known names, not verified replacements.

| name not in either source | closest known names (unverified candidates) |
| --- | --- |
| `amazon_q` | none |
| `apache_mxnet` | `apache_mxnet_on_aws` |
| `app2container` | `containers`, `container_3`, `container_2` |
| `application_migration_service` | `application_integration`, `application_discovery_service`, `database_migration_service` |
| `appstream` | `appstream_20`, `data_stream` |
| `aurora_mysql_instance` | `aurora_instance`, `rds_mysql_instance`, `aurora_instance_alt` |
| `aurora_postgresql_instance` | `rds_postgresql_instance`, `postgresql_instance`, `rds_postgresql_instance_alt` |
| `billing_conductor` | none |
| `browser` | none |
| `codeguru_profiler` | none |
| `codeguru_reviewer` | none |
| `connect_customer_profiles` | none |
| `connect_voice_id` | none |
| `connect_wisdom` | none |
| `data_catalog` | `glue_data_catalog`, `data_table` |
| `data_center` | `data_set`, `contact_center` |
| `datasync_agent` | `datasync` |
| `documentdb` | `document`, `documents`, `documents3` |
| `ebs` | none |
| `efs` | none |
| `elastic_disaster_recovery` | `cloudendure_disaster_recovery` |
| `elb` | none |
| `elemental_appliances` | `elemental_link`, `elemental_inference` |
| `elemental_conductor` | `elemental_mediaconnect`, `elemental_mediastore`, `elemental_mediatailor` |
| `elemental_delta` | `elemental_link`, `elemental`, `elemental_mediatailor` |
| `elemental_live` | `elemental_link`, `elemental_medialive`, `elemental` |
| `elemental_server` | `elemental_medialive`, `elemental_inference`, `elemental_mediaconvert` |
| `event_bus` | `events`, `event` |
| `express_workflows` | `express_workflow` |
| `fault_injection_service` | `fault_injection_simulator`, `location_service` |
| `generic_sdk` | `generic` |
| `greengrass_connector` | `iot_greengrass_component` |
| `group_auto_scaling` | `group_auto_scaling_group`, `auto_scaling`, `auto_scaling3` |
| `group_aws_account` | `group_account`, `group_aws_cloud`, `group_aws_cloud_alt` |
| `group_elastic_beanstalk_container` | `group_elastic_beanstalk` |
| `group_generic` | `generic` |
| `group_private_subnet` | `group_subnet` |
| `group_public_subnet` | `group_subnet` |
| `group_server_contents` | `group_ec2_instance_contents` |
| `group_step_functions_workflow` | `group_aws_step_functions_workflow` |
| `iam` | none |
| `iam_identity_center` | none |
| `internet_2` | `internet`, `internet_alt2`, `internet_alt22` |
| `iot_action` | `action`, `iot_button` |
| `iot_analytics_data_set` | `iot_analytics_data_store`, `iot_analytics_channel`, `iot_analytics` |
| `iot_analytics_notebook` | `iot_analytics_channel`, `iot_analytics` |
| `iot_greengrass` | `greengrass`, `group_iot_greengrass`, `iot_greengrass_recipe` |
| `iot_hardware_board` | `hardware_board` |
| `iot_policy` | `policy`, `iot_1click` |
| `iot_rule` | `iot_core` |
| `iot_shadow` | `shadow` |
| `iot_topic` | `topic` |
| `ivs` | none |
| `laptop` | none |
| `launch_wizard` | none |
| `lookout` | none |
| `managed_grafana` | `managed_service_for_grafana` |
| `managed_prometheus` | `managed_service_for_prometheus` |
| `managed_workflows_apache_airflow` | `managed_workflows_for_apache_airflow` |
| `mariadb_instance` | `rds_mariadb_instance`, `r5ad_instance`, `db_instance` |
| `mediaconnect` | `mediaconnect_gateway`, `connect`, `elemental_mediaconnect` |
| `mediaconvert` | `elemental_mediaconvert` |
| `medialive` | none |
| `mediapackage` | `elemental_mediapackage` |
| `mediastore` | none |
| `mediatailor` | none |
| `memorydb` | none |
| `migration_hub_orchestrator` | none |
| `migration_hub_refactor_spaces` | `migration_hub_refactor_spaces_services`, `migration_hub_refactor_spaces_environments`, `migration_hub_refactor_spaces_applications` |
| `msk` | none |
| `on_premises` | `group_on_premise` |
| `opensearch` | none |
| `private_ca` | `private_5g` |
| `pytorch` | none |
| `q_business` | none |
| `q_developer` | none |
| `qldb` | none |
| `robomaker_cloud_extension` | none |
| `robomaker_development_environment` | `development_environment` |
| `robomaker_fleet_management` | `fleet_management` |
| `robomaker_simulation` | `braket_simulator` |
| `schema_registry` | `eventbridge_schema_registry` |
| `sdk` | none |
| `serverless_application_model` | `serverless_application_repository` |
| `snow_family` | none |
| `snowball_import_export` | `import_export` |
| `tablet` | `table`, `alert` |
| `tensorflow` | `tensorflow_on_aws` |
| `toolkit` | none |
| `well_architected` | `well_architect_tool` |
| `workflow` | none |
| `workspaces_web` | `workspaces`, `workspaces_workspaces_web`, `workspaces_family` |

Palette-verified group icons (Sidebar-AWS4.js lines 265-299): `group_aws_cloud`, `group_aws_cloud_alt`, `group_region`, `group_vpc2` (the palette's VPC), `group_security_group`, `group_auto_scaling_group`, `group_on_premise`, `group_corporate_data_center`, `group_elastic_beanstalk`, `group_ec2_instance_contents`, `group_spot_fleet`, `group_aws_step_functions_workflow`, `group_account`, `group_iot_greengrass_deployment`, `group_iot_greengrass`.
In the palette, Public subnet and Private subnet are `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;grStroke=0;` with `strokeColor=#7AA116;fillColor=#F2F6E8;` (public) and `strokeColor=#00A4A6;fillColor=#E6F6F7;` (private). Availability Zone and Security group are plain dashed rectangles (`fillColor=none;strokeColor=#147EBA;dashed=1;` and `strokeColor=#DD3522;`), with no grIcon.
