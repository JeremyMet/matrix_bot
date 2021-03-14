from flask import Flask, render_template
import pickle

app = Flask(__name__)

months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"];

@app.route('/')
def index():
	f_normalize = lambda x : x.lower().capitalize();
	score_dic = {};
	score_dic["tersaken"] = 10;
	score_dic["quentin"] = 30;
	score_array = [];
	for key_value, value in sorted(score_dic.items(), key=lambda x: x[1], reverse=True):
		score_array.append((f_normalize(key_value), value));
	print(score_array)
	return render_template("index.html", length=len(score_array), score_array=score_array)

if __name__ == '__main__':


	app.run()
