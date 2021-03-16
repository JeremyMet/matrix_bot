from flask import Flask, render_template
import datetime
import pickle

__SCOREBOARD_MONTH__ = "./modules/loto/scoreboard_file.dic";

app = Flask(__name__)

MONTHS = ["de Janvier", "de Février", "de Mars", "d'Avril", "de Mai", "de Juin", "de Juillet", "d'Août", "de Septembre", "d'Octobre", "de Novembre", "de Décembre"];

@app.route('/')
def index():
	f_normalize = lambda x : x.lower().capitalize();
	score_dic = {};
	try:
		with open("scoreboard_file.dic", "rb") as picke_file:
			score_dic = pickle.load(pickle_file);
	except:
		pass
	score_array = [];
	for key_value, value in sorted(score_dic.items(), key=lambda x: x[1], reverse=True):
		score_array.append((f_normalize(key_value), value));
	current_month = MONTHS[datetime.datetime.now().month-1];
	return render_template("index.html", length=len(score_array), score_array=score_array, current_month=current_month)
	print(score_array)

if __name__ == '__main__':
	app.run(host="0.0.0.0");
