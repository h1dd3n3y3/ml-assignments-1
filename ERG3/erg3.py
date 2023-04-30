import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Load the dataset into a pandas dataframe
df = pd.read_csv('exams.csv')

# Print the original dataset
print("Original dataset:")
print(df)

# Add the unique variable
for index, row in df.iterrows():
    df.at[index, 'name'] = 'Student ' + str(index)
#aaaa
# Categorising the students into 4 classes 
class_Fail = {}
class_Fair = {}
class_Good = {}
class_Excellent = {}

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
        class_Excellent[name] = math_score
    else:
        print ("error math score value out of bounds")

#Make dataframe with the next math score for each student
next_math_score = df[['name', 'math score']].copy()
next_math_score['next math score'] = next_math_score['math score'].shift(-1)
next_math_score = next_math_score.dropna()

#Train the decision tree classifier to predict the next mark
X = next_math_score[['math score']]
Y = next_math_score['next math score']
clf = DecisionTreeClassifier()
clf.fit(X,Y)

# Predict the next math score for each student
predictions = {}
for name, score in class_Fail.items():
    predicted_score = clf.predict([[score]])[0]
    predictions[name] = predicted_score

for name, score in class_Fair.items():
    predicted_score = clf.predict([[score]])[0]
    predictions[name] = predicted_score

for name, score in class_Good.items():
    predicted_score = clf.predict([[score]])[0]
    predictions[name] = predicted_score

for name, score in class_Excellent.items():
    predicted_score = clf.predict([[score]])[0]
    predictions[name] = predicted_score

# Print the predictions for each student
for name, predicted_score in predictions.items():
    if (predicted_score < 50):
        predicted_class="Fail"
    elif (predicted_score == 50) | (predicted_score <65):
        predicted_class="Fair"
    elif (predicted_score == 65) | (predicted_score <85):
        predicted_class="Good"
    elif (predicted_score ==85) | (predicted_score <=100):
        predicted_class="Excellent"
    else:
        print ("error math score value out of bounds")
    print(f"{name}: Predicted next math score is {predicted_class}")
    

# Print the values for each class
print("Values for each class:")
print(f"Fail: {class_Fail}")
print(f"Fair: {class_Fair}")
print(f"Good: {class_Good}")
print(f"Excellent: {class_Excellent}")

