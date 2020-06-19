from flask import Flask, render_template, send_from_directory
from flask import url_for
import core_functionality
import os

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/screening/')
def screening():
    return core_functionality.start_page()

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route("/data/<string:database>/<string:page_name>")
def scores(database,page_name):
    return core_functionality.hilbert_map_page(database, page_name)

@app.route("/structures/<string:protein>/<string:ids>")
def proteins(protein, ids):
    drug = protein+"_"+ids+".pdb"
    return render_template("protein_view.html", drug_fname=drug, protein_fname=protein+".pdb")

@app.route('/hilbert/<directory>/<filename>')
def send_hilbert(directory,filename):
    return send_from_directory("hilbert_bar/hilbert/{}/".format(directory),filename)

@app.route('/bar/<directory>/<filename>')
def send_bar(directory,filename):
    return send_from_directory("hilbert_bar/bar/"+ directory, filename)

@app.route('/pdbs/<directory>/<pdb>')
def send_pdb(directory,pdb):
    return send_from_directory("pdb/"+directory+"/", pdb)

@app.route('/babel/<database>/<int:index>')
def obabel(database,index):
    return send_from_directory(*core_functionality.babel_images(database,index))

if __name__ == "__main__":
    app.run(port=8080, debug=False, host="0.0.0.0")

#just making workflow