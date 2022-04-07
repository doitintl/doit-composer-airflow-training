# Case study: generate nudges

From the previous chapters, we have learned the Airflow concepts and how to write DAGs and custom Operators. In this chapter, let's work on a real-world use case and create an Airflow pipeline together.

## Background

An e-commerce company (let's call it `Cell-mate`) is a famous online shop selling phones and accessories. They have various data sources which export data in CSV files to a _Google Cloud Storage_ (GCS) bucket on a daily basis.

## Data sources

The `Cell-mate` has three primary data sources:

- Accounts&mdash;It contains all the information from the accounts of their customers.
- Items&mdash;It contains all the items that are listed on the <!-- textlint-disable terminology -->website<!-- textlint-enable -->.
- Activities&mdash;It contains all the viewer activities from the customers.

## Goal

The product team in `Cell-mate` would like to build a pipeline to generate nudge emails for the customers who recently viewed the items on their <!-- textlint-disable terminology -->website<!-- textlint-enable --> but didn't make the purchase. As the first step, they would like the nudge data to be stored in a place so that the email campaign service can use it.

Let's continue and create the DAG first.
