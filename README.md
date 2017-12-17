# DDL to Data Dictionary

I don't like create Data Dictionary, just simply copying columns, data types to another document.

Try to defined some DDL format, and use Python to extract the information, and output to `Markdown` or `Confluence Wiki` syntax.

**The SQL Format**

```sql
-- Header
/* desc
Here is the desc for a table
desc */

--ddstart
  Column1 Varchar(10) NOT NULL, --dd example comment for a Column1
  Column2 Decimal(10,2) --dd comment2
--ddend

```

1. Must have two lines with `/* desc` and `desc */`, nothing else on those lines,
the content between those lines will be captured as table description.
2. Must have two lines with `--ddstart` and `--ddend`, nothing else on those lines,
and all lines in between are considered as one column per line
3. All lines between 2) must have ` --dd `, if that is a definition for column
4. If `NOT NULL` found, the column is not Nullable
5. The Data Type must not having space

**Markdown**

```
**Table Name**
> Table Desc

|Column Name|Data Type|Nullable|Comment|
|:----------|:--------|:-------|-------|
|Column1|Varchar(10)|No|example comment for a column1|
|Column2|Decimal(10,2)|No|example comment for a column2|
```

**Confluence Wiki**

```
**Table Name**
Table Desc

||Column Name|||Data Type|||Nullable|Comment||
|Column1|Varchar(10)|No|example comment for a column1|
|Column2|Decimal(10,2)|No|example comment for a column2|
```
