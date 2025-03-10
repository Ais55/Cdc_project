from django.http import JsonResponse
import csv
import statistics

def load_csv(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        return [row for row in csv.DictReader(file)]

def statistics_view(request):
    students = load_csv("D:\\IIT DH\\Cdc_pro\\students.csv")
    placements = load_csv("D:\\IIT DH\\Cdc_pro\\placements.csv")
    placement_applications = load_csv("D:\\IIT DH\\Cdc_pro\\placement_applications.csv")

    def studentid_to_branch(studentid):
        for student in students:
            if student['rollno'] == studentid:
                return student['branch']
        return "Unknown"

    for application in placement_applications:
        application['branch'] = studentid_to_branch(application['studentid'])

    def placementid_to_ctc(placementid):
        for placement in placements:
            if placement['id'] == placementid:
                return placement['ctc']
        return 0

    for application in placement_applications:
        application['ctc'] = placementid_to_ctc(application['placementid'])

    branch_ctcs = {}
    for application in placement_applications:
        if application['branch'] not in branch_ctcs:
            branch_ctcs[application['branch']] = []
        if application['selected'] == 'True':
            branch_ctcs[application['branch']].append(int(application['ctc']))

    output = {"highest_ctc": {}, "median_ctc": {}, "lowest_ctc": {}, "average_ctc": {}, "percentage_placed": {}, "students": []}

    for branch, ctcs in branch_ctcs.items():
        output['highest_ctc'][branch] = max(ctcs) if ctcs else 0
        output['median_ctc'][branch] = statistics.median(ctcs) if ctcs else 0
        output['lowest_ctc'][branch] = min(ctcs) if ctcs else 0
        output['average_ctc'][branch] = sum(ctcs) / len(ctcs) if ctcs else 0

    branch_total_students = {branch: 0 for branch in branch_ctcs.keys()}
    for student in students:
        branch_total_students[student['branch']] += 1

    branch_placed_students = {branch: 0 for branch in branch_ctcs.keys()}
    for application in placement_applications:
        if application['selected'] == 'True':
            branch_placed_students[application['branch']] += 1

    for branch in branch_ctcs.keys():
        total_students = branch_total_students.get(branch, 1)
        placed_students = branch_placed_students.get(branch, 0)
        output['percentage_placed'][branch] = round((placed_students / total_students) * 100, 2)

    student_placements = {}
    for application in placement_applications:
        if application['selected'] == 'True':
            studentid = application['studentid']
            company_name = next((p['name'] for p in placements if p['id'] == application['placementid']), "Unknown")
            ctc_value = int(application['ctc'])

            if studentid not in student_placements:
                student_placements[studentid] = {
                    "rollno": studentid,
                    "branch": studentid_to_branch(studentid),
                    "batch": 2021,
                    "companies_selected": [],
                    "ctc": 0
                }

            student_placements[studentid]["companies_selected"].append(company_name)
            student_placements[studentid]["ctc"] = max(student_placements[studentid]["ctc"], ctc_value)

    output["students"] = list(student_placements.values())

    return JsonResponse(output)
