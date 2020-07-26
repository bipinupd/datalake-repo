 CREATE TABLE IF NOT EXISTS `_ENTERPRISE`.example_dataset.example_table2
 (
   x INT64 OPTIONS(description="An optional INTEGER field"),
   y STRUCT<
     a ARRAY<STRING> OPTIONS(description="A repeated STRING field"),
     b BOOL
   >
 )
 OPTIONS(
   expiration_timestamp=TIMESTAMP "2023-01-01 00:00:00 UTC",
   description="a table that expires in 2023",
   labels=[("org_unit", "development")]
 )