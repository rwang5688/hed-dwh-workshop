/*
===============================================================================================
Starting from an empty Redshift database (dwh), the following steps setup the external schemas.
===============================================================================================
*/

/*
--Prerequisites - Create external schema to connect to the SIS data in the data lake
-- Ensure that the correct database (dwh) is selected as context (above).
-- There should be 12 tables in the external schema.  See list below.
*/
CREATE EXTERNAL SCHEMA sisraw 
FROM
    data catalog
    database 'db_raw_sisdemo' region '${AWS::Region}'
    iam_role '${RedshiftSpectrumRoleArn}';

/*
--Prerequisites - Create external schema to connect to the LMS data in the data lake
-- There should be 10 tables in the external schema, including the following:
-- assignment_dim, assignment_fact, submission_dim, submission_fact and requests.
*/
CREATE EXTERNAL SCHEMA lmsraw
FROM
    data catalog
    database 'db_raw_lmsdemo' region '${AWS::Region}'
    iam_role '${RedshiftSpectrumRoleArn}';

/*
============================================================================================
============================================================================================
*/

/*
============================================================================================
The following steps are what we demonstrate in the video and plan to do for the event. 
If concerned about running short on time, please perform the steps ahead of the event.
You can then just walk through rather than building the configuration during the demo.
============================================================================================
*/

/*
--Step 1 - Run the following steps to load the SIS datasets directly into Redshift.
*/
CREATE SCHEMA sis;
CREATE TABLE sis.course AS SELECT * FROM sisraw.course;
CREATE TABLE sis.course_outcome AS SELECT * FROM sisraw.course_outcome;
CREATE TABLE sis.course_registration  AS SELECT * FROM sisraw.course_registration;
CREATE TABLE sis.course_schedule AS SELECT * FROM sisraw.course_schedule;
CREATE TABLE sis.degree_plan AS SELECT * FROM sisraw.degree_plan;
CREATE TABLE sis.department AS SELECT * FROM sisraw.department;
CREATE TABLE sis.ed_level AS SELECT * FROM sisraw.ed_level;
CREATE TABLE sis.faculty AS SELECT * FROM sisraw.faculty;
CREATE TABLE sis.school AS SELECT * FROM sisraw.school;
CREATE TABLE sis.semester AS SELECT * FROM sisraw.semester;
CREATE TABLE sis.student AS SELECT * FROM sisraw.student;
CREATE TABLE sis.university AS SELECT * FROM sisraw.university;

/*
--Step 2 - Select some data from the local data warehouse tables
*/
SELECT COUNT(*) from sis.course_registration;

/*
--Step 3 - Query data from the data lake
*/
SELECT COUNT(*) from lmsraw.requests;

/*
--Step 4 - Executing a query combining data lake and data warehouse tables
*/
SELECT
    TO_DATE(assignment_dim.all_day_date, 'YYYY-MM-DD') due_date,
    TO_DATE(submission_dim.submitted_at, 'YYYY-MM-DD') submitted_date,
    DATEDIFF( day, due_date, submitted_date) relative_submit_date,
    *
FROM
    lmsraw.submission_dim
    JOIN sis.student
        ON submission_dim.user_id = student.student_id
    JOIN lmsraw.assignment_dim
        ON submission_dim.assignment_id = assignment_dim.assignment_id;

/*
--Step 5 - Create a new schema to abstract the data warehouse / data lake boundary for analysts
*/
CREATE SCHEMA sis_lms;

/*
--Step 6 - Use views to capture the logic to join data warehouse tables with data lake content
*/
CREATE OR REPLACE VIEW sis_lms.submit_date_view
AS
SELECT
    TO_DATE(assignment_dim.all_day_date, 'YYYY-MM-DD') due_date,
    TO_DATE(submission_dim.submitted_at, 'YYYY-MM-DD') submitted_date,
    DATEDIFF( day, due_date, submitted_date) relative_submit_date,
    CAST(EXTRACT (YEAR from TO_DATE(submission_dim.submitted_at, 'YYYY-MM-DD')) AS INTEGER) submit_year,
    submission_dim.assignment_id,
    submission_dim.user_id,
	submission_fact.course_id,
    submission_fact.score,
    student.student_id,
    student.gender,
    student.parent_highest_ed,
    student.high_school_gpa,
    student.department_id,
    student.admit_semester_id
FROM
    lmsraw.submission_dim
    JOIN lmsraw.submission_fact
    	ON submission_dim.id = submission_fact.submission_id
    JOIN lmsraw.assignment_dim
        ON submission_dim.assignment_id = assignment_dim.assignment_id
	JOIN sis.student
        ON submission_dim.user_id = student.student_id
    JOIN sis.semester
        ON student.admit_semester_id = semester_id
WITH NO SCHEMA BINDING;

/*
--Step 7 - Confirm that the new view is working
*/
SELECT * from sis_lms.submit_date_view;
SELECT COUNT(*) from sis_lms.submit_date_view;

/*
-- Step 8 - Create view of request table to support heat map
*/
CREATE VIEW sis_lms.request_info_view
AS SELECT
    id,
    EXTRACT(dayofweek FROM TO_DATE(LEFT("timestamp",10), 'YYYY-MM-DD')) dayofweek_num,
    timestamp_year,
    timestamp_month,
    timestamp_day,
    timestamp_hour,
    user_id,
    course_id,
    http_method,
    session_id,
    url
FROM
    lmsraw.requests
WITH NO SCHEMA BINDING;

/*
--Step 9 - Confirm that the new view is working
*/
SELECT * from sis_lms.request_info_view;
SELECT COUNT(*) from sis_lms.request_info_view;

/*
============================================================================================
============================================================================================
*/

/*
============================================================================================
The following steps are for returning the dwh database to its pre-demo state
============================================================================================
*/

/*
-- DROP sis_lms schema
*/
DROP SCHEMA sis_lms CASCADE;

/*
-- DROP lmsraw schema
*/
DROP SCHEMA lmsraw CASCADE;

/*
-- DROP sisraw schema
*/
DROP SCHEMA sisraw;
