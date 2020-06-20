from flask import render_template, request
import os
import numpy as np
''' try:
    from html import escape
except ImportError:
    import cgi
    def escape(arg):
        return cgi.escape(arg)
'''

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

def hilbert_map_page(database,page_name):
    print(coordinate_to_id[database]['scale'])
    if database not in dataset_pages.keys() or page_name not in data[database].keys():
        return render_template("Error_404.html")
    if len(list(request.args)) != 0:
        i = coordinate_to_id[database][list(request.args)[0]]
        ind = get_ids(database,i)
    else:
        if dataset_pages[database][page_name]:
            template = "index_smina_true.html"
        else:
            template = "index_smina_false.html"
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
    if dataset_pages[database][page_name]:
        template = "index_smina_true.html"
        pdb = page_name.split('_')[1].split('.')[0].split('-')[0] +'_'
        ssnet_name = page_name.replace('smina','SSnet').replace('8','D')
        smina_name = page_name.replace('SSnet','smina')
        for i in range(len(page_data)):
            ssnet_score = '{:.3f}'.format(data[database][ssnet_name][ind[i]])
            smina_score = '{:.2f}'.format(data[database][smina_name][ind[i]])
            smina_mad = '{:.2f}'.format(data[database][smina_name+'_mad'][ind[i]])
            page_data[i].append(ssnet_score)
            page_data[i].append(smina_score)
            page_data[i].append(smina_mad)
            page_data[i].append('/babel/{}/{}'.format(database, ind[i]))
    else:
        template = "index_smina_false.html"
        for i in range(len(page_data)):
            page_data[i].append('{:.3f}'.format(data[database][page_name][ind[i]]))
            smiles = data[database]['smiles'][ind[i]]
            page_data[i].append('/babel/{}/{}'.format(database, ind[i]))
    protein_name = page_name.split('_')[1].split('-')[0]
    return render_template(template,protein_name=protein_name,page_name=page_name,database=database,page_data=page_data,img_scale=coordinate_to_id[database]['scale'])

global data
global coordinate_to_id
global dataset_pages
data = {}
coordinate_to_id = {}
dataset_pages = {}
for i in os.listdir('dictionary_scores'):
	fname = i.split('.')[0]
	data[fname] = np.load(os.path.join('dictionary_scores',i),allow_pickle=True).item()
	coordinate_to_id[fname] = np.load(os.path.join('coord_to_index',i),allow_pickle=True).item()
	dataset_pages[fname] = {}
	for j in data[fname]:
		if j in ["ids", "links", "smiles"] or "mad" in j:
			continue
		dataset_pages[fname][j] = fname in ["approved", "natural"] and "Zn" not in j

def babel_images(database,index):
    if not os.path.isdir('babel'):
        os.mkdir('babel')
    if not os.path.isdir('babel/'+database):
        os.mkdir('babel/'+database)
    if not os.path.isfile('babel/{}/{}.png'.format(database,index)):
        print('obabel -:"{}" -O babel/{}/{}.png'.format(data[database]['smiles'][index],database,index))
        os.system('obabel -:"{}" -O babel/{}/{}.png -xb none'.format(data[database]['smiles'][index],database,index))
    return ('babel/{}/'.format(database),'{}.png'.format(index))