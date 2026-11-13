import pandas as pd


df = pd.read_csv("/Users/radmirkurgunaev/Documents/devs/python/homework4/tested.csv")
df_loaded = pd.read_csv("/Users/radmirkurgunaev/Documents/devs/python/homework4/titanic-processed.csv")

df_expected = df.drop(columns=["Cabin"])

pd.testing.assert_frame_equal(
    df_expected.reset_index(drop=True),
    df_loaded,
    check_dtype=False
)

