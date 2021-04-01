from flask import Flask, render_template
import datetime
import pickle

__SCOREBOARD_MONTH__ = "./scoreboard_file.dic";
__SCOREBOARD_FULL__  = "./flask_scoreboard.dic"

app = Flask(__name__)

MONTHS = ["de Janvier", "de Février", "de Mars", "d'Avril", "de Mai", "de Juin", "de Juillet", "d'Août", "de Septembre", "d'Octobre", "de Novembre", "de Décembre"];

@app.route('/')
def index():
	f_normalize = lambda x : x.lower().capitalize();
	score_dic = {};
	full_score_dic = {}
	try:
		with open(__SCOREBOARD_MONTH__, "rb") as pickle_file:
			score_dic = pickle.load(pickle_file);
		with open(__SCOREBOARD_FULL__, "rb") as pickle_file:
			full_score_dic = pickle.load(pickle_file);
	except:
		pass
	score_array = [];
	for key_value, value in sorted(score_dic.items(), key=lambda x: x[1], reverse=True):
		score_array.append((f_normalize(key_value), value));
	current_month = MONTHS[datetime.datetime.now().month-1];

	autre = "";
	for k,v in full_score_dic:
		current_month = int(key[0:2]);
		current_year = key[2];
		autre += "<h2>Score du mois {} {}</h2><br>".format(MONTHS[current_month], current_year);
		autre += "<table style=\"width:20%\">";
		for key_value, value in sorted(v.items(), key=lambda x: x[1], reverse=True):
			autre += "<tr>"
			autre += "<td>{}</td>".format(key_value);
			autre += "<td>{}</td>".format(str(value));
			autre += "</tr>"
		autre+= "</table>"

	return render_template("index.html", length=len(score_array), score_array=score_array, current_date=(current_month, datetime.datetime.now().year), autre=autre);


if __name__ == '__main__':
	app.run(host="0.0.0.0");
