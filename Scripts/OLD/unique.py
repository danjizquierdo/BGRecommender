with open('users.txt','r') as f:
    output=f.read()
    output=output.split(',')
    stuff=pd.Series(output)
    series=pd.Series(stuff.unique())
    series.to_csv('uniqueusers.csv')
