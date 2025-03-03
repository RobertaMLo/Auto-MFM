import numpy as np
import os
import csv


# need to read just the mean
def read_mean_from_csv(file_path):
    file = open(file_path)
    csvreader = csv.reader(file)
    rows = []

    for row in csvreader:
        rows.append(row)

    file.close()

    rows = np.array(rows)
    mossy_input = rows[:, 0]
    f_mean = rows[:, 1]

    # mossy_input[i] = type string --> need to map into an array of type float
    mossy_input = list(map(float, mossy_input))
    f_mean = list(map(float, f_mean))

    return np.array(mossy_input), np.array(f_mean)


new_FOLDER, filename_csv = 'MLI_STATS', 'MLI_firing_rate_stats.csv'

#fixed parameters
stell_file_path = '/home/bcc/projects/BSB4_demo/cerebellum_zmin/stellate_cell_fr_for_TF.csv'
bask_file_path = '/home/bcc/projects/BSB4_demo/cerebellum_zmin/basket_cell_fr_for_TF.csv'
#stell_file_path = '/home/bcc/bsb-ws/Zebrine_minus/bsb_preprocessing/STELL_STATS/stellate_fr_stats.csv'
#bask_file_path = '/home/bcc/bsb-ws/Zebrine_minus/bsb_preprocessing/BASK_STATS/basket_fr_stats.csv'
#Nstell, Nbas = 299, 147

Nstell, Nbas = 302, 150
#read data from csv file computed with compute_stats.py
f_mossy, stell_mean_fr= read_mean_from_csv(stell_file_path)
_, bask_mean_fr  = read_mean_from_csv(bask_file_path)

# compute the MLI mean freq as a weighted mean on basket & stellate firing rate (weigth  = N cells)
mli_mean_fr = (stell_mean_fr*Nstell + bask_mean_fr*Nbas) / (Nstell + Nbas)


#create a direcotry to save the results for MLI
#work_dir = os.getcwd()
work_dir = '/home/bcc/projects/BSB4_demo/cerebellum_zmin/'

if os.path.exists(work_dir + '/' +new_FOLDER):
    print('Folder %s has been already created!' % new_FOLDER)
else:
    try:
        os.mkdir(work_dir+'/'+new_FOLDER)
    except OSError:
        print("Creation of the directory %s failed" % new_FOLDER)
        exit()
    else:
        print("Successfully created the directory %s " % new_FOLDER)


#jump into the folder just created and write the csv file with the FR for the MLI
os.chdir(work_dir+'/'+new_FOLDER)
path = os.getcwd()+'/'+filename_csv

row = np.zeros([len(f_mossy), 2])
for i in range(len(f_mossy)):

    row[i, :] = [f_mossy[i], mli_mean_fr[i]]
    print(row[i,:])

with open(path, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(row)

os.chdir(work_dir)


