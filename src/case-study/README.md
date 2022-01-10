# Case study: generate nudges

From the previous chapters, we have learned the Airflow concepts and how to write DAGs and custom Operators. In this chapter, let's work on a real-world use case and create an Airflow pipeline together.

## Background
An e-commerce company (let's call it `Cell-mate`) is a famous online shop selling phones and accessories. They have various data sources, and all of them export data in CSV files to a GCS bucket on a daily basis.

## Data sources:
`Cell-mate` has three primary data sources:
- accounts: it contains all the information from the accounts of their customers.
- items: it contains all the items that are listed on the website.
- activities: it contains all the viewer activities from the customers.

## Goal
The product team in `Cell-mate` would like to build a pipeline to generate nudge emails for the customers who recently viewed the items on their website but didn't make the purchase. As the first step, they would like the nudge data to be stored in a place so that the email campaign service can use it.

Let's go ahead and create the DAG first!
