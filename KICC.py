import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET
import csv
import os

#SELECT XML FILE
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])

if not file_path:
    exit()

try:
    # PARSE XML
    xml = ET.parse(file_path)
except Exception as e:
    print(f"Error while parsing XML file: {e}")
    exit()

base_file_name, _ = os.path.splitext(os.path.basename(file_path))
csv_file_path = f"{base_file_name}_parsed.csv"

try:
    # CREATE CSV FILE
    with open(csv_file_path, 'w', encoding='utf-8') as csvfile:
        csvfile_writer = csv.writer(csvfile)

        # ADD THE HEADER TO CSV FILE
        csvfile_writer.writerow(["Date","Start Time","Media ID","Duration","SOM","Start Type","Type"])

        # FOR EACH EVENT
        for i, Event in enumerate(xml.findall("Event"), start=1):

            if Event:
                # EXTRACT PARSER DETAILS  
                Date = Event.find("OnAirDate")
                StartTime = Event.find("OnAirTime")
                MediaID = Event.find("MaterialID")
                Duration = Event.find("Duration")
                SOM = Event.find("Timecode_In")
                Type = "MEDIA"
                if i == 1:
                    StartType = ""
                else:
                    StartType = "SEQ"
                csv_line = [Date.text, StartTime.text, MediaID.text, Duration.text, SOM.text, StartType, Type]

                # ADD A NEW ROW TO CSV FILE
                csvfile_writer.writerow(csv_line)
except Exception as e:
    print(f"Error while writing to CSV file: {e}")

