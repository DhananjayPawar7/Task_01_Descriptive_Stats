# Pure Python vs. Pandas Comparison

## Did the results agree?

Yes, when both approaches use the same cleaning rules and the same definition of standard deviation, the results agree. The scripts deliberately normalize missing-value tokens and formatted numeric strings in the same way. They also both use **sample standard deviation** (`ddof=1`), which matches Pandas' default `Series.std()` behavior.

Small discrepancies can appear if the two implementations are allowed to make different assumptions. For example, Pandas may infer a numeric dtype automatically, while a manual CSV workflow initially sees every value as text. Pandas also has its own default missing-value recognition, whereas the pure-Python script must define missing tokens explicitly. The scripts in this repository reduce those differences by importing values as strings and applying the same normalization rules before analysis.

## Decisions that pure Python forced me to make

The pure-Python implementation required explicit decisions about several issues that Pandas can hide behind convenience methods:

- What counts as missing data?
- Should values containing commas or currency symbols be treated as numeric?
- What percentage of non-missing values must parse as numbers before a column is called numeric?
- How should standard deviation be defined?
- What should happen when a column contains zero or one numeric value?
- How should ties and top-frequency categories be represented?

Writing these rules manually made the assumptions visible. Pandas can perform the same work with much less code, but the shorter code does not remove the underlying decisions.

## What Pandas made easier

Pandas made exploration significantly faster. `shape`, `dtypes`, `info()`, `describe()`, `value_counts()`, `nunique()`, and missing-value operations provide concise ways to inspect a dataset. Once the cleaning logic is established, grouped or additional analyses would also be much easier to extend in Pandas than with repeated dictionary/list operations in base Python.

## What I learned from writing the manual version first

The manual implementation made type inference and missing-value handling much more concrete. In CSV files, every value initially arrives as text. A number becomes a number only because the program applies a rule that successfully parses it. Similarly, a blank string, `N/A`, and `null` are not automatically the same concept unless the program chooses to treat them that way.

That insight makes Pandas output easier to trust critically. Instead of treating `describe()` as a black box, I can now identify the assumptions that need to be aligned before comparing results across tools.

## Overall assessment

Pure Python is better for learning the mechanics and making assumptions explicit. Pandas is better for efficient exploratory analysis and scaling the workflow. The strongest workflow for this task was to build the logic manually first, then reproduce the same logic in Pandas and compare the outputs rather than assuming the library result must be correct.
