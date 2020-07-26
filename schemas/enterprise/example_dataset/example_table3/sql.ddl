 CREATE TABLE IF NOT EXISTS `_ENTERPRISE`.example_dataset.example_table3
 (
   name STRING,
   email STRING,
   job STRING,
   city STRING,
   country STRING    
 )
 OPTIONS(
   expiration_timestamp=TIMESTAMP "2023-01-01 00:00:00 UTC",
   description="a table that expires in 2023",
   labels=[("org_unit", "development")]
 )