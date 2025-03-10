import csv
import statistics
import csv

# Read placement applications CSV
with open("D:\IIT DH\Cdc_pro\placement_applications.csv", mode="r", encoding="utf-8") as file:
    csv_reader = csv.DictReader(file)  
    placement_applications = list(csv_reader)  # Convert reader to a list inside the `with` block

# print(placement_applications[:5])  # Test print

# Read placements CSV
with open("D:\\IIT DH\\Cdc_pro\\placements.csv", mode="r", encoding="utf-8") as file:
    csv_reader = csv.DictReader(file)  
    placements = list(csv_reader)  # Convert inside `with` block

# print(placements[:5])

# Read students CSV
with open("D:\\IIT DH\\Cdc_pro\\students.csv", mode="r", encoding="utf-8") as file:
    csv_reader = csv.DictReader(file)  
    students = list(csv_reader)  # Convert inside `with` block

# print(students[:5])

#{branch1: [ctcs...], branch2: [ctcs....]}


def studentid_to_branch(studentid):
    for i in students:
        if i['rollno'] == studentid :
            return i['branch']
        
for i  in placement_applications:
    i['branch'] = studentid_to_branch(i['studentid'])
# print(placement_applications)

def placementid_to_ctc(placementid):
    for i in placements:
        if i['id'] == placementid:
            return i['ctc']
        
for i  in placement_applications:
    i['ctc'] = placementid_to_ctc(i['placementid'])
# print(placement_applications[:5])
# print()
#{branch: [ctc1, ctc2, ctc3...]}
branch_ctcs = {}

for i in placement_applications:
    if i['branch'] not in branch_ctcs.keys():
        branch_ctcs[i['branch']]=[]
    if i['selected'] == 'True':
        branch_ctcs[i['branch']].append(i['ctc'])
    
# print(branch_ctcs)

output = {"highest_ctc": {}, "median_ctc": {}, "lowest_ctc": {}, "average_ctc": {}, "percentage_placed": {}, "students": []}
 
for i in branch_ctcs.keys():
    for j in range(len(branch_ctcs[i])):
        branch_ctcs[i][j] = int(branch_ctcs[i][j])
        
for i in branch_ctcs.keys():
       output['highest_ctc'][i]=max(branch_ctcs[i])
       output['median_ctc'][i]=statistics.median(branch_ctcs[i])
       output['lowest_ctc'][i]=min(branch_ctcs[i])
       output['average_ctc'][i]=sum(branch_ctcs[i])/len(branch_ctcs[i])
       
# print()   
# print(output)

def selected(studentid):
    for i in placement_applications:
        if i['studentid'] == studentid and i['selected'] == 'True':
            return True  
    return False    


for j in students:
        if selected(j['rollno']):
            j['selected'] = 'True' 
        else:
            j['selected'] = 'False'
            
# print(students[:5])

# print()

for i in branch_ctcs.keys():
    output['percentage_placed'][i] = 0

for j in students:
    if j['selected'] == 'True':
        output['percentage_placed'][j['branch']]+=1

total_students = {}
for i in branch_ctcs.keys():
    total_students[i] = 0

for i in students:
   total_students[i['branch']]+=1

for i in branch_ctcs.keys():
    output['percentage_placed'][i] = (output['percentage_placed'][i]/total_students[i])*100

    
for i in placement_applications:
    for j in placements:
        if i['placementid'] == j['id']:
            i['company'] = j['name']
            break
# print(placement_applications[:5])
# print(students[:5])
# print()
for i in students:
    if i['selected'] == 'True':
        i['companies_selected'] =[]
        i['highest_ctc'] = 0
        for j in placement_applications:
            if j['studentid'] == i['rollno'] and j['selected'] == 'True':
                i['companies_selected'].append(j['company'])
                i['highest_ctc'] = max(int(j['ctc']), i['highest_ctc'])
    else:
        i['companies_selected'] =None
        i['highest_ctc'] = None
    del i['id']
    del i['selected']
# print(students[:5])

output['students'] = students

print(output)

