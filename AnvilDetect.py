from openpyxl import load_workbook
import matplotlib.pyplot as plt 
from matplotlib.ticker import PercentFormatter
import numpy as np 
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

def dec_mat(threshold, good_list, bad_list):
    acceptGood = 0
    rejectGood = 0
    acceptBad = 0
    rejectBad = 0
    for val in bad_list:
        if val >= threshold: acceptBad += 1
        else: rejectBad += 1
    for val in good_list:
        if val >= threshold: acceptGood += 1
        else: rejectGood += 1

    return acceptGood, rejectGood, acceptBad, rejectBad
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

count_10 = len(goodPrimers_10) + len(noAnvil_10) + len(emptyCup_10)
count_40 = len(goodPrimers_40) + len(noAnvil_40) + len(emptyCup_40)

# dataFile = get_filename('anvilTestData','.csv','')
# heading = ['goodPrimers_10','noAnvil_10','emptyCup_10','goodPrimers_40','noAnvil_40','emptyCup_40']
# with open(dataFile, 'a', newline='\n') as myFile:
#     writer = csv.writer(myFile)
#     writer.writerow(heading)
#     for key, val in enumerate(goodPrimers_10):
#         dataOut = []
#         try:
#             dataOut.append(val)
#         except:
#             dataOut.append(' ')
#         try:
#             dataOut.append(noAnvil_10[key])
#         except:
#             dataOut.append(' ')
#         try:
#             dataOut.append(emptyCup_10[key])
#         except:
#             dataOut.append(' ')
#         try:
#             dataOut.append(goodPrimers_40[key])
#         except:
#             dataOut.append(' ')
#         try:
#             dataOut.append(noAnvil_40[key])
#         except:
#             dataOut.append(' ')
#         try:
#             dataOut.append(emptyCup_40[key])
#         except:
#             dataOut.append(' ')
#         writer.writerow(dataOut) 
# fileName1 = get_filename('below_10','.png','')
# n1, bins1, patches1 = plt.hist(goodPrimers_10, 50, range=(0,1000), stacked=True, label='Good Primers')
# n2, bins2, patches2 = plt.hist(noAnvil_10, 50, range=(0,1000), stacked=True, label='No Anvil')
# n3, bins3, patches3 = plt.hist(emptyCup_10, 50, range=(0,1000), stacked=True, label='Empty Cup')
# plt.xlabel('Sensor Reading')
# plt.ylabel('Quantity')
# plt.title('0.010" Below Primer Pocket Sensor Value Distribution\nN={}'.format(count_10))
# plt.legend()
# # plt.savefig(fileName1, bbox_inches='tight')
# plt.show()

# fileName2 = get_filename('below_40','.png','')
# n4, bins4, patches4 = plt.hist(goodPrimers_40, 50, range=(0,1000), stacked=True, label='Good Primers')
# n5, bins5, patches5 = plt.hist(noAnvil_40, 50, range=(0,1000), stacked=True, label='No Anvil')
# n6, bins6, patches6 = plt.hist(emptyCup_40, 50, range=(0,1000), stacked=True, label='Empty Cup')
# plt.xlabel('Sensor Reading')
# plt.ylabel('Quantity')
# plt.title('0.040" Below Primer Pocket Sensor Value Distribution\nN={}'.format(count_40))
# plt.legend()
# # plt.savefig(fileName2, bbox_inches='tight')
# plt.show()

numRounds = 6065124
# while not numRounds.isdigit():
#     numRounds = input('Number of Rounds Generated = ')

numAnvils = 96
# while not numAnvils.isdigit():
#     numAnvils = input('Number of Anvils Generated = ')

sensorThreshold = 'one'
while not sensorThreshold.isdigit():
    sensorThreshold = input('Sensor Threshold for Good Part = ')

# numRounds = int(numRounds)
# numAnvils = int(numAnvils)
sensorThreshold = int(sensorThreshold)

bad_10 = noAnvil_10 + emptyCup_10

# acceptGood = 0
# rejectGood = 0
# acceptBad = 0
# rejectBad = 0

# for val in bad_10:
#     if val >= sensorThreshold: acceptBad += 1
#     else: rejectBad += 1
# for val in goodPrimers_10:
#     if val >= sensorThreshold: acceptGood += 1
#     else: rejectGood += 1

acceptGood, rejectGood, acceptBad, rejectBad = dec_mat(sensorThreshold, goodPrimers_10, bad_10)

p_tAcc = acceptGood/len(goodPrimers_10)
p_fAcc = acceptBad/len(bad_10)
p_fRej = rejectGood/len(goodPrimers_10)
p_tRej = rejectBad/len(bad_10)

print(
'''
       | GOOD Pt.| BAD Pt. 
------------------------------
Accept | {:1.6f} | {:1.6f}
------------------------------
Reject | {:1.6f} | {:1.6f}
'''.format(p_tAcc,p_fAcc,p_fRej,p_tRej))

goodParts = numRounds - numAnvils

tAcc = goodParts*p_tAcc
fAcc = numAnvils*p_fAcc
fRej = goodParts*p_fRej
tRej = numAnvils*p_tRej

print(
'''
       | GOOD Pt.| BAD Pt. 
------------------------------
Accept | {:1.2f} | {:1.2f}
------------------------------
Reject | {:1.2f} | {:1.2f}
'''.format(tAcc,fAcc,fRej,tRej))

sps = fRej/(12*4*4)

print('Scrap Per Shift: {}'.format(sps))


AG = []
RG = []
AB = []
RB = []
scrapPerShift = []
partsMissedPcnt = []
values = range(1000)
for sensVal in range(1000):
    acceptGood, rejectGood, acceptBad, rejectBad = dec_mat(sensVal, goodPrimers_10, bad_10)
    p_tAcc = acceptGood/len(goodPrimers_10)
    p_fAcc = acceptBad/len(bad_10)
    p_fRej = rejectGood/len(goodPrimers_10)
    p_tRej = rejectBad/len(bad_10)
    tAcc = goodParts*p_tAcc
    fAcc = numAnvils*p_fAcc
    fRej = goodParts*p_fRej
    tRej = numAnvils*p_tRej
    AG.append(tAcc)
    RG.append(fRej)
    AB.append(fAcc)
    RB.append(tRej)
    scrapPerShift.append(fRej/(12*4*4))
    partsMissedPcnt.append(100*tRej/numAnvils)
# plt.plot(values, AG, label='True Accept')
# plt.plot(values, RG, label='False Reject (scrap)')
# plt.plot(values, RB, label='True Reject')
# plt.plot(values, AB, label='False Accept (minimize)')
# plt.xlabel('Sensor Threshold')
# plt.ylabel('Parts Made')
# plt.title('Sensor Threshold Values')
# plt.show()
# fullVals = []
# for k, v in enumerate(partsMissedPcnt):
#     if v > 99:
#         fullVals.append((values[k], v))
plt.plot(values, partsMissedPcnt, label='Dropped Anvils Missed')
# plt.plot(fullVals[0], fullVals[1], color='r')
plt.xlabel('Sensor Threshold')
plt.ylabel('Percent of Theoretical Missing Anvils Caught')
# plt.axis.yaxis.set_major_formatter(PercentFormatter())
plt.title('Missing Anvil Parts Caught')
fname = get_filename('sensorVals', '.png', '')
plt.savefig(fname, bbox_inches='tight')
# plt.legend()
plt.show()

