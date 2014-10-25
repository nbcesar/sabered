import logging

# Define the Student Details Grid
def studentDetails(num_students):
    data = []
    data.append([" ","Student","Period", "Group"])
    for x in range(1, num_students + 1):
        data.append([x,"","",""])
    return data

# Define the Multiple Choice Grid
def mcDetails(num_mc, mc_answers):
    data = []
    # First Row
    data.append(["Multiple Choice", "Point Value", "Answer"])
    for x in range (1,num_mc + 1):
        row = [x, 1, ""]
        data.append(row)        
    return data

# Define the Open Response Grid
def orDetails(num_mc, num_or):
    data = []
    data.append(["Open Response", "Point Value"])
    for x in range(num_mc + 1, num_mc + num_or + 1):
        row = [x,1]
        data.append(row)
    return data

# Define updated Analysis Grid
def analysisGrid(num_mc, num_or, mc_data, or_data, mc_answers, student_data):
    fixedRows = 4
    answerRows = 0
    # Find maximum OR point value
    or_pt_value_list = []
    for x in range(1, len(or_data)):
        or_pt_value_list.append(or_data[x][1])
    max_pts = int(max(or_pt_value_list))
    if max_pts >= mc_answers:
        fixedRows += max_pts
        answerRows = max_pts
    else:
        fixedRows += mc_answers
        answerRows = mc_answers
    
    # Find unique Periods
    periods = []
    for x in range(1, len(student_data)):
        periods.append(student_data[x][2])
    unique_periods_set = set(periods)
    unique_periods = list(unique_periods_set)
    unique_periods.sort()
    periods = []
    for x in unique_periods:
        if x != '':
            periods.append(x)
    if len(periods) > 0:
        fixedRows += len(periods)
    

    # Find unique groups
    groups = []
    for x in range(1, len(student_data)):
        groups.append(student_data[x][3])
    unique_groups_set = set(groups)
    unique_groups = list(unique_groups_set)
    unique_groups.sort()
    groups = []
    for x in unique_groups:
        if x != '':
            groups.append(x)
    if len(groups) > 0:
        fixedRows += len(groups)    
    # Student Data

    
    data = []
    
    # Row 0
    row = ["","","Question"]
    for x in range(1, num_mc + 1):
        row.append(x)
    row.append("MC Avg")
    row.append("MC Pts")
    row.append("Questions")
    for x in range(num_mc + 1, num_mc + num_or + 1):
        row.append(x)
    row.append("OR Avg") 
    row.append("OR Pts") 
    row.append("")
    row.append("Average")
    row.append("Points")
    
    data.append(row)
    
    # Row 1
    row = ["","","Answer"]
    for x in range(1, num_mc + 1):
        answer = mc_data[x][2]
        row.append(answer)
    row.append("")
    row.append("")
    row.append("Pt Value")
    for x in range(1, num_or + 1):
        value = or_data[x][1]
        row.append(value)
    row.append("")
    row.append("")
    row.append("")
    row.append("")
    row.append("")
    
    data.append(row)

    # Row 2 
    row = ["","QA"]
    row.append(1)
    for x in range(1, num_mc + 1):
        row.append("")
    row.append("")
    row.append("")
    row.append(0)
    for x in range(1, num_or + 1):
        row.append("")
    row.append("")
    row.append("")
    row.append("")
    row.append("")
    row.append("")

    data.append(row)

    # Row 3 -> Max OR Pts
    for x in range(1, answerRows + 1):
        row = ["",""]
        if x < mc_answers:
            # Create MC & OR Question Analysis Columns
            row.append(x + 1)
            for y in range(1, num_mc + 1):
                row.append("")
            row.append("")
            row.append("")
            if x <= max_pts:
                row.append(x)
            else:
                row.append("")
            for z in range(1, num_or + 1):
                row.append("")
            row.append("")
            row.append("")
            row.append("")
            row.append("")
            row.append("")
        else:
            # Create only OR Question Analysis Columns
            for y in range(0, num_mc + 1):
                row.append("")
            row.append("")
            row.append("")
            if x <= max_pts:
                row.append(x)
            else:
                row.append("")
            for z in range(1, num_or + 1):
                row.append("")
            row.append("")
            row.append("")
            row.append("")
            row.append("")
            row.append("")    

        data.append(row)

    # Row Avg by Group -> Max Groups 
    if len(groups) > 0:
        row = ["","Group Avg"]
        # group 1
        row.append(groups[0])
        for y in range(1, num_mc + 1):
                row.append("")
        row.append("")
        row.append("")
        row.append(groups[0])
        for z in range(1, num_or + 1):
            row.append("")
        row.append("")
        row.append("")
        row.append(groups[0])
        row.append("")
        row.append("")

        data.append(row)

        for x in range(1, len(groups)):
            row = ["","",groups[x]]
            for y in range(1, num_mc + 1):
                row.append("")
            row.append("")
            row.append("")
            row.append(groups[x])
            for z in range(1, num_or + 1):
                row.append("")
            row.append("")
            row.append("")
            row.append(groups[x])
            row.append("")
            row.append("")

            data.append(row)

# Row Avg by Period -> Max Periods 
    if len(periods) > 0:
        row = ["","Period Avg"]
        # group 1
        row.append(periods[0])
        for y in range(1, num_mc + 1):
                row.append("")
        row.append("")
        row.append("")
        row.append(periods[0])
        for z in range(1, num_or + 1):
            row.append("")
        row.append("")
        row.append("")
        row.append(periods[0])
        row.append("")
        row.append("")

        data.append(row)

        for x in range(1, len(periods)):
            row = ["","",periods[x]]
            for y in range(1, num_mc + 1):
                row.append("")
            row.append("")
            row.append("")
            row.append(periods[x])
            for z in range(1, num_or + 1):
                row.append("")
            row.append("")
            row.append("")
            row.append(periods[x])
            row.append("")
            row.append("")

            data.append(row)

# Student Header Row
    row = ["Name", "Period", "Group"]
    for y in range(1, num_mc + 1):
        row.append("")
    row.append("")
    row.append("")
    row.append("")
    for z in range(1, num_or + 1):
        row.append("")
    row.append("")
    row.append("")
    row.append("")
    row.append("")
    row.append("")

# Student Rows
    for x in range(0, len(student_data)):
        if student_data[x][1] != "":
            row = [student_data[x][1], student_data[x][2], student_data[x][3]]
            for y in range(1, num_mc + 1):
                row.append("")
            row.append("")
            row.append("")
            row.append("")
            for z in range(1, num_or + 1):
                row.append("")
            row.append("")
            row.append("")
            row.append("")
            row.append("")
            row.append("")
            data.append(row)

    return data, fixedRows, num_mc, num_or, len(groups), len(periods)

'''
# define default grid data -> OLD GRID, BEFORE PT VALUE UPDATE
def defaultGrid(num_mc, mc_answers, num_or,or_points, num_students):
    data = []
    num_mc = num_mc
    mc_answers = mc_answers
    num_or = num_or
    or_points = or_points
    num_students = num_students
    total_questions = num_mc + num_or
    
    #add answers row
    row = ["Answers","",""]
    for x in range (0,num_mc):
        row.append("")
    row.append("")
    for x in range (0,num_or):
        row.append("")
    row.append("")
    data.append(row)
    
    #add pt value row
    row = ["Pt Value","",""]
    for x in range (0,num_mc):
        row.append("1")
    row.append("")
    for x in range (0,num_or):
        row.append(or_points)
    row.append("")
    data.append(row)
    
    #add row for each possible OR value
    rows = max([or_points,mc_answers])
    logging.error(type(or_points))
    logging.error(type(mc_answers))
    logging.error(rows)
    for x in range(0, rows + 1):
        row = ["","",x]
        for z in range(0, num_mc):
            row.append("")
        row.append("")
        for z in range(0, num_or):
            row.append("")
        row.append("")
        data.append(row)
    
    #add percent row
    row = ["%","",""]
    for x in range (0,num_mc):
        row.append("")
    row.append("")
    for x in range (0,num_or):
        row.append("")
    row.append("")
    data.append(row)

    #add a row for each student
    for x in range (1, num_students + 1):
        row = ["Student " + str(x), "S" + str(x), ""]
        for x in range (0,num_mc):
            row.append("")
        row.append("")
        for x in range (0,num_or):
            row.append("")
        row.append("")
        data.append(row)         
    logging.error(data)
    return data
'''