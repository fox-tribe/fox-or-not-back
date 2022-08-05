import BadWord

model = BadWord.load_badword_model()
data = BadWord.preprocessing("그게 뭔데 씹덕아...")
print(model.predict(data))