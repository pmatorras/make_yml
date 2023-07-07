import argparse, sys, os

def modify_text_file(file_i, line_dict):
    # Read the text file
    with open(file_i, 'r') as file:
        lines = file.readlines()

    # Modify the desired line
    for i in range(len(lines)):
        for key, value in line_dict.items():
            if key + ':' in lines[i]:
                prefix = lines[i].split(':')[0] + ':'
                lines[i] = prefix + ' ' + str(value) + "\n"

    # Write the modified lines back to the file
    print(file_i)
    with open(file_i, 'w') as file:
        file.writelines(lines)
# Example usage:



# Create the argument parser
parser = argparse.ArgumentParser(description='Process file content')
parser.add_argument('--i_file', '-i', dest='i_file',  default = None, help='Path to the input file')
parser.add_argument('--samples' , '-s', dest='samples' ,  default = 'try', help='input sample')

args = parser.parse_args()
i_file = args.i_file

# Read Sample files
if '.txt' in args.samples:
    with open(args.samples, 'r') as file:
        lines = file.read().splitlines()
    samples = ', '.join(lines)
else:
    samples = args.samples 

# Loop over samples
for sample in samples.split(','):
    isEE = True if 'EEMini' in sample else False 
    line_dict = {'storageSite'  : 'T1_DE_KIT_Disk',
                 'outLFNDirBase': '/store/user/pmatorra/PFNano'}
    isData = False 
    isMC   = False
    i_fol  = ''
    f_fol  = 'final_yml/'
    if 'Run2022' in sample: isData = True
    if 'Run3'    in sample: isMC   = True
    if isData is False and isMC is False: 
        print ('something wrong')
        continue
    if args.i_file is None:
        i_fol = 'card_templates/'
        #Choose specific template depending on the file to run
        if isMC:
            if isEE: i_file = 'card_example_mcEE.yml'
            else:    i_file = 'card_example_mc.yml'
        if isData:
            #pick the correct json
            json_ = 'jsons/Cert_Collisions2022_355100_362760_Golden.json'
            if os.path.isfile(json_): line_dict['lumiMask'] = json_
            else: 
                print ("json", json_,"doesnt exist")
                exit()
            print(isData, bool('2022E' in sample))
            if '2022E' in sample: 
                i_file = 'card_example_dataE.yml'
            elif '2022F' in sample or '2022G' in sample: i_file = 'card_example_dataFG.yml'
            else: i_file = 'card_example_dataABCD.yml'
    else: 
        if '/' in args.i_file:
            i_fol  = args.i_file.split('/')[0]
            i_file = args.i_file.split('/')[1]

        else:
            i_file = args.i_file

    #Fill dictionary
    line_dict['datasets'] = sample
    if isMC:
        line_dict['data'] = 'False'   
        workarea = sample.split('/Run3')[0].split('Pt5')[0].replace('/','')+'Pt5'
        if isEE: workarea+= '_EE'
    if isData:
        line_dict['data'] = 'True'
        workarea ='Run2022'+sample.split('/Run2022')[1].split('-')[0]
    workarea = workarea.replace(' ','')
    line_dict['workArea'] = 'summer22_'+workarea+'_yml'
    line_dict['name']     = workarea

    #Write to new file
    file_path  = i_fol+i_file 
    outputfile = f_fol+(workarea+'.yml').replace('\'','').replace(' ','')
    print(outputfile, workarea, sample)
    print('Input file: ', file_path,'\n')
    print('Changing the following lines to')
    os.system('cp '+file_path+' '+outputfile)
    for key, value in line_dict.items():
        print(key,'\t:', value)
        modify_text_file(outputfile, {key: value})
    print('\nOutput file:', outputfile)
