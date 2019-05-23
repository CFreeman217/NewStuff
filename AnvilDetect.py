from openpyxl import load_workbook
import matplotlib.pyplot as plt 
import datetime, csv, os

def get_filename(prefix, suffix, base_path):
    '''
    Gets a unique file name in the base path.
    
    Appends date and time information to file name and adds a number
    if the file name is stil not unique.
    prefix = Homework assignment name
    suffix = Extension
    base_path = Location of log file
    '''
    # Set base filename for compare
    fileNameBase = base_path + prefix + "_" + datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    # Set base for numbering system if filename exists
    num = 1
    # Generate complete filename to check existence
    fileName = fileNameBase + suffix
    # Find a unique filename
    while os.path.isfile(fileName):
        # if the filename is not unique, add a number to the end of it
        fileName = fileNameBase + "_" + str(num) + suffix
        # increments the number in case the filename is still not unique
        num = num + 1
    return fileName

wkbk = load_workbook('Results.xlsx')
wkst = wkbk['Test 3']
goodPrimers_10 = []
noAnvil_10 = []
emptyCup_10 = []
goodPrimers_40 = []
noAnvil_40 = []
emptyCup_40 = []
for val in range(504):
    goodPrimers_10.append(wkst['B{}'.format(val+3)].value)
for val in range(377):
    noAnvil_10.append(wkst['E{}'.format(val+3)].value)
for val in range(106):
    emptyCup_10.append(wkst['H{}'.format(val+3)].value)
for val in range(314):
    goodPrimers_40.append(wkst['K{}'.format(val+3)].value)
for val in range(273):
    noAnvil_40.append(wkst['N{}'.format(val+3)].value)
for val in range(34):
    emptyCup_40.append(wkst['Q{}'.format(val+3)].value)

count1 = len(goodPrimers_10) + len(noAnvil_10) + len(emptyCup_10)
count2 = len(goodPrimers_40) + len(noAnvil_40) + len(emptyCup_40)

dataFile = get_filename('anvilTestData','.csv','')
heading = ['goodPrimers_10','noAnvil_10','emptyCup_10','goodPrimers_40','noAnvil_40','emptyCup_40']
with open(dataFile, 'a', newline='\n') as myFile:
    writer = csv.writer(myFile)
    writer.writerow(heading)
    for key, val in enumerate(goodPrimers_10):
        dataOut = []
        try:
            dataOut.append(val)
        except:
            dataOut.append(' ')
        try:
            dataOut.append(noAnvil_10[key])
        except:
            dataOut.append(' ')
        try:
            dataOut.append(emptyCup_10[key])
        except:
            dataOut.append(' ')
        try:
            dataOut.append(goodPrimers_40[key])
        except:
            dataOut.append(' ')
        try:
            dataOut.append(noAnvil_40[key])
        except:
            dataOut.append(' ')
        try:
            dataOut.append(emptyCup_40[key])
        except:
            dataOut.append(' ')
        writer.writerow(dataOut) 
fileName1 = get_filename('below_10','.png','')
n1, bins1, patches1 = plt.hist(goodPrimers_10, 50, range=(0,1000), stacked=True, label='Good Primers')
n2, bins2, patches2 = plt.hist(noAnvil_10, 50, range=(0,1000), stacked=True, label='No Anvil')
n3, bins3, patches3 = plt.hist(emptyCup_10, 50, range=(0,1000), stacked=True, label='Empty Cup')
plt.xlabel('Sensor Reading')
plt.ylabel('Quantity')
plt.title('0.010" Below Primer Pocket Sensor Value Distribution\nN={}'.format(count1))
plt.legend()
# plt.savefig(fileName1, bbox_inches='tight')
plt.show()

fileName2 = get_filename('below_40','.png','')
n4, bins4, patches4 = plt.hist(goodPrimers_40, 50, range=(0,1000), stacked=True, label='Good Primers')
n5, bins5, patches5 = plt.hist(noAnvil_40, 50, range=(0,1000), stacked=True, label='No Anvil')
n6, bins6, patches6 = plt.hist(emptyCup_40, 50, range=(0,1000), stacked=True, label='Empty Cup')
plt.xlabel('Sensor Reading')
plt.ylabel('Quantity')
plt.title('0.040" Below Primer Pocket Sensor Value Distribution\nN={}'.format(count2))
plt.legend()
# plt.savefig(fileName2, bbox_inches='tight')
plt.show()
