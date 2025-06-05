import json





def get_workbook():
    json_data = open('static/data.json')
    print(type(json_data))
    data1 = json.load(json_data)  # deserialises it
    for subject, workbook in data1['subjects'].items():
        print(f"Subject: {subject}")
        for workbook, chapters in workbook.items():
            print(f"  id: {workbook}")
            for chapter, exercises in chapters.items():
                str_exercises="  | ".join(exercises)
                print(chapter+" "+str_exercises)

    # print(data1["data"])
    # for i in data1["data"]["subjects"]:
    #     print(i)
    #     print(i["hindi"])
    # print(data1["data"]["subjects"])


def get_assignment():
    json_data = open('/static/data.json')
    print(json_data)


get_workbook()


