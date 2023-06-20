# file = open("Datesheet.txt", "r")
# contents = file.read()

# words = contents.split('\n')

# new_lst = []
# for word in words:
#     new = word.split(' ')    
#     i = 0
#     while i < len(new) - 1:
#         if new[i] == 'Wednesday':            
#             new[i-1] = new[i]
#             new[i] = ''
#         elif new[i] != "" and i < len(new) - 2 and new[i+1] != "" :
#             new[i] = new[i] + " " + new[i+1]
#             new.pop(i+1)
            
#         else:
#             i += 1
#     final = [x for x in new if x != ""]
#     new_lst.append(final)

# print(new_lst)



file_stu = open("SeatingPlan.txt", "r")
lines = file_stu.read()
words = lines.split('\n')
new_lst = []
for word in words:
    new = word.split(' ')    
    i = 0
    while i < len(new) - 1:
        if new[i] != "" and i < len(new) - 2 and new[i+1] != "" :
            new[i] = new[i] + " " + new[i+1]
            new.pop(i+1)
            
        else:
            i += 1
    final = [x for x in new if x != ""]
    new_lst.append(final)

print(new_lst)