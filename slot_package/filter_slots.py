from datetime import datetime, timedelta
import csv
import difflib


def view_slots(day, file):
    list_of_times = []
    base_time = datetime(int(datetime.today().strftime("%Y")), int(
        datetime.today().strftime("%m")), int(datetime.today().strftime("%d")), 8, 30)
    list_of_times = [{"Date": day, "Time": (base_time + timedelta(minutes=i)).strftime(
        r'%H:%M:%S'), "Description": "----"} for i in range(0, 481, 30)]

    list_of_slots = []
    with open(f'{file}.csv', 'r') as combined_calendar_list:
        student_csv_reader = (csv.DictReader(combined_calendar_list))
        for item in student_csv_reader:
            if day == item['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION'].split('\t')[0].strip():
                list_of_slots.append({"Date": item['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION'].split('\t')[0].strip(),
                                      "Time": item['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION'].split('\t')[1].strip(),
                                      "Description": item['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION'].split('\t')[2].strip()})
    av_slots = []
    print("Slots")
    for i in list_of_slots:
        for j in list_of_times:
            if i["Time"].split('-')[0].strip() == j['Time'] and i["Date"] == j['Date']:
                list_of_times.pop(list_of_times.index(j))

    print(*list_of_times, sep='\n')


# print(datetime.today().date())
view_slots(str(datetime.today().date()), 'combined_calendar_list')
