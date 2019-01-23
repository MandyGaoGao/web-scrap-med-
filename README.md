# web-scrap-med-
Data Crawling,Cleaning,Visualization;Word Doc Auto Generation;Math modeling


                                                Detailed Description: See 0)documentation
# Automation of literature mining ###########################################################################################
1) subtract pharmacokinetic section from RCP from ‘base-donnees-publique.medicaments.gouv.fr’ based on random IDs loop---return to excel
2) search of papers based on drug substance name and keywords (key in at prompt) from PubMed and return [article title, author, abstract,link] in excel 
3) 1.get all the drug names and corresponding RCP link from ‘base-donnees-publique.medicaments.gouv.fr’ return both in csv file ##
3) 2.request links in 3.1)csv file, return drug name, substance, RCP pharmacokinetics section, return in excel
3) 3. from 3.1)csv file, string manipulation return drug name, substance name to excel file and put all active substance name in a txt file without repetition ##
4) 1.request links in 3.1)csv file, return drug name, substance name, drug composition, drug form, RCP pharmacokinetic section, return all in excel##
4) 2.transform information in 4.1)excel to word document one word document per drug , save under the name of each drug ##
5) 1.search PubMed articles about substance written in a txt file, return substance name, keyword for search, article title, author, link,abstract, date of search return in excel
5) 1.search PubMed articles about substance written in a txt file, return substance name, keyword for search, article title,DOI, author, link,abstract, date of search return in excel, eliminate repeated articles by DOI check
5) 2.search PubMed articles about substance written in a txt file, return substance name, keyword for search, article title,PMID,DOI, author, link,abstract, date of search return in excel, eliminate repeated articles by PMID check in single substance database ##
# Construction of SQL database structure ###########################################################################################
6) 0.Build SQL database on both local server and remote server (SQL server Mattieu) using SSMS** ##
6) 1.Populate the SQL database(local/online) from excel  ##
6) 2.Generate math model of drug intake from request from SQL database ##
# Knime workflow construction ###########################################################################################
7) 0.Build knime workflow to connect online/local SQL server and populate the SQL database and retrieve info and generate equation model ** ##
7) 1.Python extension and code to generate a graph of RCP modelling ##


