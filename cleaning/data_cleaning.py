import csv
from encodings import utf_8
from tracemalloc import start

file = open("clean_data.csv", encoding="utf8", mode = "w")
file = open("raw_data.txt", "r")

filel = open("sbdloi", "r")
sbdl = filel.read().split(",0")
sbdli = []
for i in range(len(sbdl)):
  sbdli.append(int(sbdl[i]))


#Read the information of 1 student
datas = file.read().split("\n")

#write header to csv
with open("clean_data.csv", encoding="utf8", mode="w", newline = '') as file_csv:
  header = ["sbd", "tên", "dd", "mm", "yy", "toán", "ngữ văn", "khxh", "khtn", "lịch sử", "địa lí", "gdcd", "sinh học", "vật lí", "hóa học", "tiếng anh"]
  writer = csv.writer(file_csv)
  writer.writerow(header)
sbd = 2000000
for data in datas:
  sbd += 1
  if sbd in sbdli:
    continue

  
  sbd_str = "0" + str(sbd)
  #Make data becomes a list
  data = data.split("\\n")

  #Remove \r, \t in HTML file
  for i in range(len(data)):
    data[i] = data[i].replace("\\r", "")
    data[i] = data[i].replace("\\t", "")

  #Remove tag
  for i in range(len(data)):

    tags = []
    for j in range(len(data[i])):
      if data[i][j] == "<":
        start = j
      if data[i][j] == ">":
        end = j
        tags.append(data[i][start:end+1])
    for tag in tags:
      data[i] = data[i].replace(tag, "")


  #Remove leading whitespace and empty lines
  unempty_lines = []
  for i in range(len(data)):
    data[i] = data[i].strip()
    if data[i] != "":
      unempty_lines.append(data[i])
  data = unempty_lines

  #Keep name, dob and score
  name = data[7]
  dob = data[8]
  scores = data[9]


  #load unicode table
  chars = []
  codes = []


  #Open file utf8 decode
  file = open("unicode.txt",encoding = "utf8")
  unicode_table = file.read().split("\n")

  for code in unicode_table:
    x = code.split(" ")
    chars.append(x[0])
    codes.append(x[1])

  #Replace special characters in name and scores
  for i in range(len(chars)):
    name = name.replace(codes[i], chars[i])
    scores = scores.replace(codes[i], chars[i])

  #The left over special characters
  for i in range(len(name)):
    if name[i:i+2] == "&#":
      name = name[:i] + chr(int(name[i+2:i+5])) +  name[i+6:]

  for i in range(len(scores)):
    if scores[i:i+2] == "&#":
      scores = scores[:i] + chr(int(scores[i+2:i+5])) +  scores[i+6:]

  #lower case
  name = name.lower()
  scores = scores.lower()

  dob_list = dob.split("/")
  dd = int(dob_list[0])
  mm = int(dob_list[1])
  yy = int(dob_list[2])

  #Remove :
  scores = scores.replace(":", "")
  scores = scores.replace("khxh ", "khxh   ")
  scores = scores.replace("khtn ", "khtn   ")
  scores_list = scores.split("   ")




  data = [sbd_str, name.title(), str(dd), str(mm), str(yy)]

  #add score to data
  for subject in ["toán", "ngữ văn", "khxh", "khtn", "lịch sử", "địa lí", "gdcd", "sinh học", "vật lí", "hóa học", "tiếng anh"]:
    if subject in scores_list:
      data.append(str(float(scores_list[scores_list.index(subject)+1])))
    else:
      data.append("-1")

  # #Write to test.txt
  # file = open("test.txt", encoding="utf8", mode = "a")
  # for i in range(len(data)):
  #   file.write(data[i] + ",")
  # file.write("\n")

  #write to csv instead of text
  with open("clean_data.csv1", "a", encoding="utf-8", newline = '') as file_csv:
    writer = csv.writer(file_csv)
    writer.writerow(data)