# Findings

## Overview

The dataset used for this analysis is a public extract of 2024 Meta/Facebook political advertising associated with Donald J. Trump campaign advertising across six states: Pennsylvania, Georgia, Michigan, Arizona, Wisconsin, and Nevada. It contains 377 rows and 10 columns. Each row includes processed measures of impressions and spend, a delivery region, creative text fields, a payer/byline, and a performance measure.

The first feature that stands out is the shape of the numeric data. The mean number of impressions per row is about 562,368, but the median is only about 108,498. The same pattern is even clearer for spend: the mean is approximately 18,165, while the median is 3,098. This difference indicates a strongly right-skewed distribution. Most rows are relatively modest compared with a smaller number of very large ad buys, including a maximum processed spend value of 700,399 and a maximum processed impression value of nearly 19.8 million. Looking only at averages would therefore make the "typical" row appear much larger than the median row.

The dataset is relatively complete in the fields needed for descriptive analysis. The numeric delivery and spend fields have no missing values. Missingness appears mainly in creative text: two rows are missing `ad_creative_bodies`, sixteen are missing `ad_creative_link_descriptions`, and two are missing `ad_creative_link_titles`. This distinction matters because an analysis of spending and geography can use essentially the entire dataset, whereas a text-focused content analysis would need to account for incomplete creative descriptions.

## Geographic pattern

The six-state distribution is uneven. Pennsylvania has the largest number of rows at 90, followed by Georgia with 80 and Michigan with 70. Arizona has 55, Wisconsin has 53, and Nevada has 29. The processed spending totals show a similar concentration at the top, although frequency and spending are not identical measures. Pennsylvania accounts for approximately 1.96 million in processed spend, and Michigan approximately 1.85 million. Georgia and Arizona are both below 0.9 million, while Wisconsin and Nevada are lower still.

Pennsylvania and Michigan together account for more than half of the processed spend represented in this extract. That finding shows why grouped analysis is useful even in an assignment focused on descriptive statistics: an overall total hides substantial geographic differences. It also illustrates why counts alone are not enough. A state may appear frequently in the data, but the amount associated with those rows can differ considerably.

## Advertiser/byline concentration

The `byline` field is also highly concentrated. `DONALD J. TRUMP FOR PRESIDENT 2024, INC.` appears in 226 of the 377 rows, while `TRUMP 47 COMMITTEE, INC.` appears in 141. The other two bylines together account for only ten rows. Processed spend is even more concentrated: the first byline accounts for about 5.86 million of the dataset's 6.85 million total processed spend, while `TRUMP 47 COMMITTEE, INC.` accounts for about 0.96 million.

This means that the dataset is not a balanced sample of many unrelated political advertisers. It is a focused campaign-ad extract with most activity associated with one primary committee/byline. That scope should shape any interpretation. The results describe this dataset; they should not be generalized to all political advertising on Facebook or Instagram during the 2024 election.

## What surprised me

The most surprising statistical feature was the size of the gap between the median and mean for both impressions and spend. Before computing both measures, it would have been easy to summarize the dataset using only an average. The median shows that a small number of very large rows have a strong effect on that average. This is a practical example of why descriptive statistics should be interpreted together rather than individually.

The second important observation was data quality. The core numeric fields are complete, while missing values are concentrated in optional text fields. That means the quality of the dataset depends partly on the question being asked: it is comparatively straightforward for numeric descriptive analysis, but less complete for detailed creative-text analysis.

Overall, the analysis shows that even a simple descriptive-statistics workflow can reveal the structure of a political-ad dataset: skewed spending and impression distributions, geographic concentration, concentration among a small number of payer/byline categories, and field-specific missingness. Those findings provide a useful baseline before moving to more complicated modeling or LLM-generated interpretation.
