# DDL to Data Dictionary

I don't like create Data Dictionary, just simply copying columns, data types to another document.

Try to defined some DDL format, and use Python to extract the information, and output to `Markdown` or `Confluence Wiki` syntax.

## Quick Start

It is very easy to use this parser, just give the whole content as `str` to the constructor, and call the `get_output` method to get text format markup.

Example:

```python

from ddl2dd import DDL
ddl_text = """
  /* desc
  this is table desc
  another line
  desc */
  -- ddstart
  c1 varchar(11,2) not null --dd comment1
  c2 Decimal(11,2) null --dd comment2
  -- ddend
  dummy
  """

d = DDL('table_name', ddl_text)

print(d.gen_output('MD'))
```

You will get

```
## table_name

this is table desc
another line

|Name|Data Type|Nullable|Comment|
|:---|:-------|:-------|:-------|
|c1|varchar(11,2)|No|comment1|
|c2|Decimal(11,2)|Yes|comment2|
```

**The SQL Format**

```sql
-- Header
/* desc
Here is the desc for a table
desc */

-- ddstart
  Column1 Varchar(10) NOT NULL, --dd example comment for a Column1
  Column2 Decimal(10,2) --dd comment2
-- ddend

```

1. Must have two lines with `/* desc` and `desc */`, nothing else on those lines,
the content between those lines will be captured as table description.
2. Must have two lines with `--ddstart` and `--ddend`, nothing else on those lines,
and all lines in between are considered as one column per line
3. All lines between 2) must have ` --dd `, if that is a definition for column
4. Must give `NULL` or `NOT NULL`
5. The Data Type must not having space
6. Any lines between 2) - if wihout a ` --dd ` will be skipped

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
