/*
============================================================================================
Starting from an empty Redshift database, the following steps setup the base SIS data.
These steps have already been done for dwh in the demo environment, but I'm including them
here for completenss.
============================================================================================
*/

/*
-- Ensure that the right Database (dwh) is selected as context (above)
-- Run the following steps to create the base SIS data directly stored in Redshift
*/
CREATE EXTERNAL SCHEMA sisraw 
FROM
    data catalog
    database 'db_raw_sisdemo' region '${AWS::Region}'
    iam_role '${RedshiftSpectrumRoleArn}';

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

DROP SCHEMA sisraw;
/*
============================================================================================
============================================================================================
*/

/*
============================================================================================
The following steps are what I demonstrate in the video and planned to do for the actual 
event.  These steps have ALREADY BEEN DONE in the dwhqs database.  So that one is ready to
use with QuickSight if you run short of time and want to just walk through rather than
building the configuration during the demo.
============================================================================================
*/
/*
--Step 1 - Create external schema to connect to the data lake
-- Three tables (assignment_fact, submission_fact and requests)
-- should be available in the external schema.
*/
CREATE EXTERNAL SCHEMA lmsraw
FROM
    data catalog
    database 'db_raw_lmsdemo' region '${AWS::Region}'
    iam_role '${RedshiftSpectrumRoleArn}';

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
    TO_DATE(assignment_fact.process_date, 'YYYY-MM-DD') due_date,
    TO_DATE(submission_fact.process_date, 'YYYY-MM-DD') submitted_date,
    DATEDIFF( day, due_date, submitted_date) relative_submit_date,
    *
FROM
    lmsraw.submission_fact
    JOIN sis.student
        ON submission_fact.user_id = student.student_id
    JOIN lmsraw.assignment_fact
        ON submission_fact.assignment_id = assignment_fact.assignment_id;

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
    TO_DATE(assignment_fact.process_date, 'YYYY-MM-DD') due_date,
    TO_DATE(submission_fact.process_date, 'YYYY-MM-DD') submitted_date,
    DATEDIFF( day, due_date, submitted_date) relative_submit_date,
    CAST(EXTRACT (YEAR from TO_DATE(submission_fact.process_date, 'YYYY-MM-DD')) AS INTEGER) submit_year,
    submission_fact.assignment_id,
    submission_fact.course_id,
    submission_fact.user_id student_id,
    submission_fact.score,
    student.gender,
    student.parent_highest_ed,
    student.high_school_gpa,
    student.department_id,
    student.admit_semester_id
FROM
    lmsraw.submission_fact
    JOIN sis.student
        ON submission_fact.user_id = student.student_id
    JOIN lmsraw.assignment_fact
        ON submission_fact.assignment_id = assignment_fact.assignment_id
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
