i = 0
with open('test.txt','r') as file:
  data = file.readlines()
  for dat in data:
    if 'Sending Request from Client' in dat:
      i = i + 1
      if i == 100:
        print "100th Request",dat

