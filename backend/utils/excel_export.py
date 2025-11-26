
import pandas as pd

def users_to_excel(users, path):
    df = pd.DataFrame(users)
    df.to_excel(path, index=False)
