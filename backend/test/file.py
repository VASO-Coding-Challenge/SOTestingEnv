import polars as pl

df = pl.DataFrame({"a": [1, 2, 3, 1], "b": [1, 2, 3, 2], "3": [1, 2, 3, 3]})

print(df.filter(pl.col("a") == 1).select(pl.col("b")).sum())
print(df)
