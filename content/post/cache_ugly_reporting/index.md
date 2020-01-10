---
title: 'Cache Ugly Reporting Queries With Materialized Views and Docker'
date: 2016-04-11
draft: false
tags : [machine learning, machine intelligence, robotics]
---

<script
  type="text/javascript"
  src="https://cdn.jsdelivr.net/npm/gist-embed@1.0.2/dist/gist-embed.min.js">
  </script>

<div class="section post-body">
<span id="hs_cos_wrapper_post_body" class="hs_cos_wrapper hs_cos_wrapper_meta_field hs_cos_wrapper_type_rich_text" style="" data-hs-cos-general-type="meta_field" data-hs-cos-type="rich_text"><p>Confidence and trust in your SaaS product depends, in part,&nbsp;on the continual conveyance&nbsp;of&nbsp;<span>the value of the solution you provide. The reporting vectors (web-based dashboards, daily emails, etc.) obviously depend upon the specifics of your product and your engagement plan with your customers. But underlying all sorts of reporting is the need to derive hard metrics from databases: What's the usage of your application by seat? How has that driven value/efficiency for them? What are the trends and anomalies&nbsp;worth calling out?&nbsp;</span></p>

<p><span>The bad news is that many of the most insightful metrics require complex joins across tables; and as you scale out to more and more customers, queries across multitenant databases will take longer and longer.&nbsp;</span>The good news is that, unlike for interactive exploration and real-time monitoring&nbsp;and alerting use cases, many of the queries against your production databases can be lazy and done periodically.</p>
<p>At <a href="http://wise.io/" target="_blank">Wise.io</a>, we needed a way to cache and periodically update long-running/expensive queries so that we could have more responsive dashboards for our customers and our&nbsp;implementation&nbsp;engineers. After some research, including exploration with 3rd party vendors, we settled on leveraging <em>materialized views</em>. This is a brief primer on a lightweight caching/update solution that uses&nbsp;materialized views<em>&nbsp;</em>coupled with <a href="https://www.docker.com/" target="_blank">Docker</a>.</p>
<p><!--more--></p>
<p><a href="https://en.wikipedia.org/wiki/Materialized_view">Materialized views</a> are database objects&nbsp;that act as snapshots of certain queries. Whereas a SELECT against a&nbsp;<em>view</em>&nbsp;dynamically reissues the associated stored query, a SELECT against a materialized view queries against a cache of the original query result. Without the overhead of query planning, scanning, and executing against the database, a SELECT against a materialized view can be extremely fast. Materialized views come out of the box in Oracle, DB2, Microsoft SQL Server ("indexed views") and Postgres.</p>
<p>For reporting purposes, we can use materialized views to cache long-running/expensive queries&nbsp;and then refresh those views on a cadence that is appropriate for the use case. The outline of the strategy is as follows:</p>
<ol>
<li><strong>Identify and hone&nbsp;the SQL statements</strong> that are ripe for MVs. These are queries that take a long time to execute and/or only need refreshing periodically (as opposed to in real time).</li>
<li><strong>Set a database-wide naming convention for the MVs</strong> that will be easy to remember (e.g.,&nbsp;<span style="font-family: 'courier new', courier;">rolling_roi_all_clients_daily</span>).</li>
<li><strong>Create the MVs in your database.&nbsp;</strong>We do this programmatically&nbsp;in staging/production using Python/<a href="https://alembic.readthedocs.org/en/latest/" target="_blank">Alembic</a>. But you can certainly build these by hand.</li>
<li>Determine an approach to <strong>identify which MVs need refreshing</strong>. You can maintain&nbsp;a DB table that contains the time until next update for each MV. Another approach is to name the MVs in a way that's easy to determine on what timescale they should be updated. For instance, by adding "daily" or "hourly" to the suffix. For the toy example, below this is the strategy we employ.&nbsp;Scheduling the refreshes will allow you to control when the underlying expensive queries will add load to your DB. You might want to schedule MV refreshes for times of the day when the load is typically small.</li>
<li><strong>Create a job that performs the refreshes</strong>. We build this these jobs into our middleware (via Python/<a href="http://www.celeryproject.org/" target="_blank">Celery</a>) but you could also have a cron job running&nbsp;on the DB machine. Or, as we show below, you could have a small Docker container which runs the update jobs periodically.</li>
</ol>
<h2>Creating the Materialized Views (in Postgres)</h2>

<p>To create a materialized view, just add the appropriate line above your super ugly SQL query:
    <code data-gist-id="8c079b33f9a2a2effeefecd093aeeb81" data-gist-file="example.sql" data-gist-hide-footer="true" data-gist-line="1-7"></code></p>

<p>This should be done by a DB user that has CREATE privilege&nbsp;as well as SELECT&nbsp;privilege&nbsp;on the appropriate tables/row. Next, to allow for the refreshing of that view without blocking the usage of that view, you need to add an index of one of the columns returned in that view:
    <code data-gist-id="8c079b33f9a2a2effeefecd093aeeb81" data-gist-file="example.sql" data-gist-hide-footer="true" data-gist-line="9-10"></code></p>

<h2>Scripting to Refresh the&nbsp;Materialized Views (in Python)</h2>
<p>The key here is to leverage the strategy you set up for identifying which MVs should be updated and on what schedule. A simple strategy is to identify the MVs by name (e.g., ending in 'hourly') using the <span style="font-family: 'courier new', courier;">pg_class</span> table to query for MVs. Then loop over all the MVs that need updating and issue a <span style="font-family: 'courier new', courier;">REFRESH MATERIALIZED VIEW CONCURRENTLY</span> <em>name</em>. For example:</p>

<code data-gist-id="8c079b33f9a2a2effeefecd093aeeb81" data-gist-file="refresh.py" data-gist-line="29-45"></code>

<h2>Run the&nbsp;Refresh Script Periodically (in Docker using cron)</h2>
<p>You can create a lightweight Docker that has the ability to run cron and python. It also needs to have psycopg2 (to connect to the postgres DB): Here the 'root' file can contain the cron jobs that you wish to run
    <code data-gist-id="8c079b33f9a2a2effeefecd093aeeb81" data-gist-file="Dockerfile"></code></p>

<p>This Docker image is about 52 MB in size (thanks <a href="https://github.com/gliderlabs/docker-alpine" target="_blank">Gliderlabs</a>!).

Once this is up and running, your long-running/expensive queries should be properly cached, allowing you to worry about all the million other unoptimized things in your stack that you can now your turn attention to. ;)</p>
<p>I created a <a href="https://gist.github.com/profjsb/8c079b33f9a2a2effeefecd093aeeb81" target="_blank">github gist with all the files you need</a>, including the files needed to install this in <a href="https://aws.amazon.com/elasticbeanstalk/" target="_blank">Elasticbeanstalk</a> environment. Remember: you'll need to make sure that the instance you are running on is given proper permissions (via security groups) to access the database. Enjoy! And let us know if you have any suggestions for improvements.</p>
<hr>

Originally posted at wise.io/blog ... see the [archive.org link](https://web.archive.org/web/20160811010604/http://www.wise.io/tech/cache-ugly-reporting-queries-with-materialized-views-and-docker).

