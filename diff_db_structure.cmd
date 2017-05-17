mysqldump -uroot appserver -d > actual_db_structure.sql
diff db_structure.sql actual_db_structure.sql | less
rm actual_db_structure.sql