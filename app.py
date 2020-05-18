import os
import flask
from flask import Flask, request, render_template, send_from_directory
import numpy as np
try:
    from html import escape
except ImportError:
    import cgi
    def escape(arg):
        return cgi.escape(arg)


app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def get_ids(database, start_index):
    vs = set()
    drug_info = []
    smiles = data[database]['ids']
    i = 0
    while len(drug_info) < 24:
        try:
            ind1 = int(start_index-i)
            ind2 = int(start_index+i)
            if smiles[ind1] not in vs and ind1 >= 0:
                drug_info.append(ind1)
            vs.add(smiles[ind1])
            if smiles[ind2] not in vs and ind2 >= 0:
                drug_info.append(ind2)
            vs.add(smiles[ind2])
        except IndexError:
            pass
        i+=1
    return drug_info#[:12]

def run_page(database,page_name):
    print(coordinate_to_id[database]['scale'])
    if database not in dataset_pages.keys() or page_name not in data[database].keys():
        return render_template("Error_404.html")
    try:
        i = coordinate_to_id[database][list(request.args)[0]]
        print(i)
        ind = get_ids(database,i)
    except:
        return render_template(template,page_name=page_name,database=database,img_scale=coordinate_to_id[database]['scale'])
    page_data = []
    for i in ind:
        page_data.append([])
        page_data[-1].append(data[database]['ids'][i])
        page_data[-1].append(data[database]['links'][i])
        if "DB" in data[database]['ids'][i]:
            page_data[-1][-1] = "https://www.drugbank.ca/drugs/" + data[database]['ids'][i]
        elif "ZINC" in data[database]['ids'][i]:
            page_data[-1][-1] = "http://zinc15.docking.org/substances/"+data[database]['ids'][i]
    if dataset_pages[database] and not "Zn" in page_name:
        template = "index_smina_true.html"
        pdb = page_name.split('_')[1].split('.')[0].split('-')[0] +'_'
        ssnet_name = page_name.replace('smina','SSnet').replace('8','D')
        smina_name = page_name.replace('SSnet','smina')
        for i in range(len(page_data)):
            ssnet_score = '{:.3f}'.format(data[database][ssnet_name][ind[i]])
            smina_score = '{:.1f}'.format(data[database][smina_name][ind[i]])
            page_data[i].append(ssnet_score)
            page_data[i].append(smina_score)
            page_data[i].append('/babel/{}/{}'.format(database, ind[i]))
    else:
        template = "index_smina_false.html"
        for i in range(len(page_data)):
            page_data[i].append('{:.3f}'.format(data[database][page_name][ind[i]]))
            smiles = data[database]['smiles'][ind[i]]
            page_data[i].append('/babel/{}/{}'.format(database, ind[i]))
    protein_name = page_name.split('_')[1].split('-')[0]
    return render_template(template,protein_name=protein_name,page_name=page_name,database=database,page_data=page_data,img_scale=coordinate_to_id[database]['scale'])

@app.route("/")
def start_page():
    pages = []
    order = ["approved", "natural", "BDB"]
    for i in order:
        page_names = []
        page_url = []
        for j in data[i]:
            if j in ["ids", "links", "smiles"] or "mad" in j:
                continue
            page_url.append('/'.join(['/data',i,j]))
            page_names.append(j)
        pages.append([i, [j for j in page_names], [j for j in page_url], len(page_names)])
    return render_template("start_index.html", page_info=pages)

@app.route("/data/<string:database>/<string:page_name>")
def scores(database,page_name):
    return run_page(database, page_name)

#To be implemented
@app.route("/proteins/<string:page_name>")
def proteins(page_name):
    ids = ""
    if len(list(request.args)) != 0:
        ids = page_name + "_" + list(request.args)[0] + '.pdb'
    print(page_name)
    return render_template("protein_view.html", ids=ids, protein_name=page_name+".pdb")


@app.route('/hilbert/<directory>/<filename>')
def send_hilbert(directory,filename):
    return send_from_directory("hilbert_bar/hilbert/"+ directory, filename)

@app.route('/bar/<directory>/<filename>')
def send_bar(directory,filename):
    return send_from_directory("hilbert_bar/bar/"+ directory, filename)

@app.route('/pdbs/<pdb>')
#To be implemented
def send_pdb(pdb):
    return send_from_directory("images/pdb/", pdb)

@app.route('/babel/<database>/<int:index>')
def babel_images(database,index):
    if not os.path.isdir('babel'):
        os.mkdir('babel')
    if not os.path.isdir('babel/'+database):
        os.mkdir('babel/'+database)
    if not os.path.isfile('babel/{}/{}.png'.format(database,index)):
        print('obabel -:"{}" -O babel/{}/{}.png'.format(data[database]['smiles'][index],database,index))
        os.system('obabel -:"{}" -O babel/{}/{}.png'.format(data[database]['smiles'][index],database,index))
    return send_from_directory('babel/{}/'.format(database),'{}.png'.format(index))

data = {}
coordinate_to_id = {}
dataset_pages = {}
for i in os.listdir('dictionary_scores'):
    smina_present = False
    if "approved" in i or "natural" in i:
        smina_present = True
    dataset_pages[i.split('.')[0]] = smina_present
    data[i.split('.')[0]] = np.load(os.path.join('dictionary_scores',i),allow_pickle=True).item()
    coordinate_to_id[i.split('.')[0]] = np.load(os.path.join('coord_to_index',i),allow_pickle=True).item()

if __name__ == "__main__":
    app.run(port=5000, debug=True)