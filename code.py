import random
import pandas as pd
import pandas_read_xml as pdx
import re


# Elements constituant la base de l'URL

url_base = 'https://www.resultats-elections.interieur.gouv.fr/telechargements/PR2022/resultatsT'
tour = '1'
#tour = '2'


# Define regions and their ID codes plus departments codes in dictionaries

regions = {
    'etranger': '000',
    'guadeloupe': '001',
    'martinique': '002',
    'guyane': '003',
    'reunion': '004',
    'mayotte': '006',
    'IDF': '011',
    'centre_loire': '024',
    'bourgogne': '027',
    'normandie': '028',
    'HDF': '032',
    'grand_est': '044',
    'pays_loire': '052',
    'bretagne': '053',
    'aquitaine': '075',
    'occitanie': '076',
    'auvergne': '084',
    'PACA': '093',
    'corse': '094',
  }

#for i in regions.values():
#  print(i)

departements = {
    'etranger': ['975','977','986','987','988'], # 099 construit une URL qui ne repond pas a la construction de base, sera ajoute apres
    'guadeloupe': ['971'],
    'martinique': ['972'],
    'guyane': ['973'],
    'reunion': ['974'],
    'mayotte': ['976'],
    'IDF': ['075','077','078','091','092','093','094','095'],
    'centre_loire': ['018','028','036','037','041','045'],
    'bourgogne': ['021','025','039','058','070','071','089','090'],
    'normandie': ['014','027','050','061','076'],
    'HDF': ['002','059','060','062','080'],
    'grand_est': ['008','010','051','052','054','055','057','067','068','088'],
    'pays_loire': ['044','049','053','072','085'],
    'bretagne': ['022','029','035','056'],
    'aquitaine': ['016','017','019','023','024','033','040','047','064','079','086','087'],
    'occitanie': ['009','011','012','030','031','032','034','046','048','065','066','081','082'],
    'auvergne': ['001','003','007','015','026','038','042','043','063','069','073','074'],
    'PACA': ['004','005','006','013','083','084'],
    'corse': ['02A','02B'],
  }


# Quick check on departments number

# for value in departements.values():
#   print(len(value))

# count = 0
# for key, value in departements.items():
#   if isinstance(value, list):
#     count += len(value)
# print(count)

# for key, values in departements.items():
#   print(key+': '+str(len(values))+' departements')


# Generate URL's based on dictionaries infos
*Voir question ici : [StackOverflow](https://stackoverflow.com/questions/71914668/build-urls-by-iterating-through-multiple-dictionaries-in-python/71914727#71914719)*

urls = []

for reg, reg_code in regions.items():
    for dep_code in departements[reg]:
        urls.append(f"{url_base}{tour}/{reg_code}/{dep_code}/{dep_code}{'com.xml'}")

#print(urls)
#print(len(urls))


# Alternative method

# base = "https://www.resultats-elections.interieur.gouv.fr/telechargements/PR2022/resultatsT{}/{}/{}/{}{}"
# urls = [base.format(tour, dept, subdept, subdept, 'com.xml') for region, dept in regions.items() for subdept in departements[region]]
# print(urls)


# French living abroad (slightly different form of URL, can be done manually)

fr_etranger_url = ['https://www.resultats-elections.interieur.gouv.fr/telechargements/PR2022/resultatsT1/000/099/099.xml']


# List of all URL's

urls_all = urls+fr_etranger_url

# Print last 10 items of the list
#print(urls_all[-9:])
#print(len(urls_all))
# Print n items randomly
#print(random.sample(urls, 10))


# Convert XML data into a more efficient dataframe
# Check if column number is identical for every dataframe
pattern = "T1(.*?)com"

for i in urls:
  data = pdx.read_xml(i)
  df = pdx.fully_flatten(data)
  substring = re.search(pattern, i).group(1)
  print(substring+" : "+str(len(df.columns)))


dfs = []

#for i in urls_list:
for i in urls:
  data = pdx.read_xml(i)
  dataframe = pdx.fully_flatten(data)
  dfs.append(dataframe)

df = pd.concat(dfs)


# Rename the columns

#cols = list(df)
#cols

df = df.rename(columns={'Election|Scrutin|Type':'type',
                        'Election|Scrutin|Annee':'annee',
                        'Election|Departement|CodReg':'code_region',
                        'Election|Departement|CodReg3Car':'code_region_3',
                        'Election|Departement|LibReg':'libelle_region',
                        'Election|Departement|CodDpt':'code_departement',
                        'Election|Departement|CodMinDpt':'code_min_departement',
                        'Election|Departement|CodDpt3Car':'code_departement_3',
                        'Election|Departement|LibDpt':'libelle_departement',
                        'Election|Departement|Communes|Commune|CodSubCom':'code_commune',
                        'Election|Departement|Communes|Commune|LibSubCom':'libelle_commune',
                        'Election|Departement|Communes|Commune|Tours|Tour|NumTour':'numero_tour',
                        'Election|Departement|Communes|Commune|Tours|Tour|Mentions|Inscrits|Nombre':'nombre_inscrits',
                        'Election|Departement|Communes|Commune|Tours|Tour|Mentions|Abstentions|Nombre':'nombre_abstention',
                        'Election|Departement|Communes|Commune|Tours|Tour|Mentions|Abstentions|RapportInscrit':'rapport_inscrits_abstention',
                        'Election|Departement|Communes|Commune|Tours|Tour|Mentions|Votants|Nombre':'nombre_votants',
                        'Election|Departement|Communes|Commune|Tours|Tour|Mentions|Votants|RapportInscrit':'rapport_inscrits_votants',
                        'Election|Departement|Communes|Commune|Tours|Tour|Mentions|Blancs|Nombre':'nombre_vote_blanc',
                        'Election|Departement|Communes|Commune|Tours|Tour|Mentions|Blancs|RapportInscrit':'rapport_inscrits_vote_blanc',
                        'Election|Departement|Communes|Commune|Tours|Tour|Mentions|Blancs|RapportVotant':'rapport_votant_vote_blanc',
                        'Election|Departement|Communes|Commune|Tours|Tour|Mentions|Nuls|Nombre':'nombre_votes_nuls',
                        'Election|Departement|Communes|Commune|Tours|Tour|Mentions|Nuls|RapportInscrit':'rapport_inscrits_votes_nuls',
                        'Election|Departement|Communes|Commune|Tours|Tour|Mentions|Nuls|RapportVotant':'rapport_votant_votes_nuls',
                        'Election|Departement|Communes|Commune|Tours|Tour|Mentions|Exprimes|Nombre':'nombre_exprimes',
                        'Election|Departement|Communes|Commune|Tours|Tour|Mentions|Exprimes|RapportInscrit':'rapport_inscrits_exprimes',
                        'Election|Departement|Communes|Commune|Tours|Tour|Mentions|Exprimes|RapportVotant':'rapport_votant_exprimes',
                        'Election|Departement|Communes|Commune|Tours|Tour|Resultats|Candidats|Candidat|NumPanneauCand':'numero_panneau_candidat',
                        'Election|Departement|Communes|Commune|Tours|Tour|Resultats|Candidats|Candidat|NomPsn':'nom',
                        'Election|Departement|Communes|Commune|Tours|Tour|Resultats|Candidats|Candidat|PrenomPsn':'prenom',
                        'Election|Departement|Communes|Commune|Tours|Tour|Resultats|Candidats|Candidat|CivilitePsn':'civilite',
                        'Election|Departement|Communes|Commune|Tours|Tour|Resultats|Candidats|Candidat|NbVoix':'nombre_de_voix',
                        'Election|Departement|Communes|Commune|Tours|Tour|Resultats|Candidats|Candidat|RapportExprime':'rapport_exprimes',
                        'Election|Departement|Communes|Commune|Tours|Tour|Resultats|Candidats|Candidat|RapportInscrit':'rapport_inscrits'})


# Export dataframe as csv file

with open(path, 'w', encoding = 'utf-8') as f:
  df.to_csv(f, index=False)
