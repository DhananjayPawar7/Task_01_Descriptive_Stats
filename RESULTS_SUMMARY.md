# Results Summary

These values describe the public 2024 Meta/Facebook political-ad extract used for the completed analysis. The source file contains **377 rows and 10 columns**.

## Dataset structure

Columns:

1. `page_name`
2. `Sum of impressions`
3. `Sum of spend`
4. `delivery_by_region`
5. `ad_creative_bodies`
6. `ad_creative_link_captions`
7. `ad_creative_link_descriptions`
8. `ad_creative_link_titles`
9. `byline`
10. `performance`

The three numeric fields are `Sum of impressions`, `Sum of spend`, and `performance`. The remaining fields are categorical/text.

## Numeric statistics

| Column | Count | Mean | Min | Max | Std. dev. | Median |
|---|---:|---:|---:|---:|---:|---:|
| Sum of impressions | 377 | 562,368.0199 | 499.5 | 19,797,451.5 | 1,575,957.0356 | 108,497.5 |
| Sum of spend | 377 | 18,165.4284 | 49.5 | 700,399.0 | 55,787.1562 | 3,098.0 |
| performance | 377 | 36.4810 | 8.0 | 175.0 | 22.3482 | 32.2031 |

Total processed impressions across the rows are **212,012,743.5**. Total processed spend is **6,848,366.5**.

The large gap between the mean and median for impressions and spend shows a right-skewed distribution: a relatively small number of high-value ads raise the average substantially above the typical row.

## Missing values

| Column | Missing |
|---|---:|
| page_name | 0 |
| Sum of impressions | 0 |
| Sum of spend | 0 |
| delivery_by_region | 0 |
| ad_creative_bodies | 2 |
| ad_creative_link_captions | 0 |
| ad_creative_link_descriptions | 16 |
| ad_creative_link_titles | 2 |
| byline | 0 |
| performance | 0 |

Missingness is therefore concentrated in optional creative-text fields rather than the numeric delivery/spending fields.

## Geographic frequency

| Region | Rows |
|---|---:|
| Pennsylvania | 90 |
| Georgia | 80 |
| Michigan | 70 |
| Arizona | 55 |
| Wisconsin | 53 |
| Nevada | 29 |

## Processed spend by region

| Region | Sum of spend |
|---|---:|
| Pennsylvania | 1,958,685.5 |
| Michigan | 1,852,964.5 |
| Georgia | 866,766.0 |
| Arizona | 849,248.0 |
| Wisconsin | 704,513.0 |
| Nevada | 616,189.5 |

Pennsylvania and Michigan together account for more than half of the processed spend in this six-state extract.

## Byline frequency

| Byline | Rows |
|---|---:|
| DONALD J. TRUMP FOR PRESIDENT 2024, INC. | 226 |
| TRUMP 47 COMMITTEE, INC. | 141 |
| TRUMP SAVE AMERICA JOINT FUNDRAISING COMMITTEE | 9 |
| Trump National Committee JFC | 1 |

## Processed spend by byline

| Byline | Sum of spend |
|---|---:|
| DONALD J. TRUMP FOR PRESIDENT 2024, INC. | 5,855,637.0 |
| TRUMP 47 COMMITTEE, INC. | 960,780.0 |
| Trump National Committee JFC | 22,000.0 |
| TRUMP SAVE AMERICA JOINT FUNDRAISING COMMITTEE | 9,949.5 |

These figures are descriptive summaries of the processed public dataset only. They should not be interpreted as a complete accounting of all 2024 political advertising on Meta.
