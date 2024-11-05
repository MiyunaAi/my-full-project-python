a = ['No', 'Yes', 'Maybe']
df = pd.DataFrame(np.random.choice(a, size=(10, 3)), columns=['Col1','Col2','Col3'])
df['Col1'] = pd.Categorical(df['Col1'])

print (df.dtypes)
Col1    category
Col2      object
Col3      object
dtype: object

print (df['Col1'].cat.categories)
Index(['Maybe', 'No', 'Yes'], dtype='object')

print (df['Col2'].unique())
['Yes' 'Maybe' 'No']

print (df['Col1'].unique())
[Maybe, No, Yes]
Categories (3, object): [Maybe, No, Yes]