from sklearn.tree import DecisionTreeClassifier

# Load the dataset into a pandas dataframe
df = pd.read_excel('exam.xlsx')

# Categorising the students into 4 classes 
class_Fail = {}
class_Fair = {}
class_Good = {}
class_Exellent = {}

for index, row in df.iterrows():
    name = row['name']
    math_score = row['math score']

    if (math_score < 50):
        class_Fail[name] = math_score
    elif (math_score == 50) | (math_score <65):
        class_Fair[name] = math_score
    elif (math_score == 65) | (math_score <85):
        class_Good[name] = math_score
    elif (math_score ==85) | (math_score <=100):
        class_Exellent[name] = math_score
    else:
        print ("error math score value out of bounds")

#Make dataframe with the next math score for each student
next_math_score = df[['name', 'math score']].copy()
next_math_score['next math score'] = next_math_score['math score'].shift(-1)
next_math_score = next_math_score.dropna

#Train the decision tree classifier to predict the next mark
X = next_math_score[['math score']]
Y = next_math_score['next math']
clf = DecisionTreeClassifier()
clf.fit(X,Y)

# Test 
sample_mark = [[75]]
predicted_mark = clf.predict(sample_mark)[0]

print('Predicted next mark:', predicted_mark)

return 0