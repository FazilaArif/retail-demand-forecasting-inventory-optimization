\# dbt Retail Transformation Pipeline



\## Overview



This dbt project transforms retail sales data stored in Google BigQuery into clean analytical datasets for demand forecasting and dashboarding.



\## Data Warehouse



\- Platform: Google BigQuery

\- Project: tonal-justice-507110-s6

\- Dataset: retail\_forecasting



\## Transformation Lineage



The dbt models follow this transformation flow:



stg\_sales

&#x20;   |

&#x20;   v

daily\_sales

&#x20;   |

&#x20;   +-----------> weekly\_sales

&#x20;   |

&#x20;   +-----------> monthly\_sales

&#x20;   |

&#x20;   +-----------> sales\_mart



\## Models



\### stg\_sales



Cleans and standardizes the source `fact\_sales` data.



\### daily\_sales



Aggregates sales at the daily level by:



\- Date

\- Item

\- Store

\- Department

\- Category

\- State



It calculates:



\- Total sales

\- Average selling price

\- Record count



\### weekly\_sales



Aggregates daily sales into weekly sales using Monday as the beginning of the week.



\### monthly\_sales



Aggregates daily sales into monthly sales.



\### sales\_mart



Provides a clean daily sales dataset for downstream analytics, forecasting, and dashboards.



\## Data Quality



The project contains 21 dbt data-quality tests.



Latest test result:



\- Tests executed: 21

\- Passed: 21

\- Failed: 0



\## Documentation



dbt documentation is generated using:



```bash

dbt docs generate

