from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re
with open("phonebook_raw.csv", encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
#pprint(contacts_list)

#ДЗ
def phone_detector(phone_raw):
  pattern = r"(7|8)?(\d{3})(\d{3})(\d{2})(\d{2})(\d{4})?"
  phone = ''.join(re.findall("\d", phone_raw))
  if len(phone) in [10, 11]:
    subst = r"+7(\2)\3-\4-\5"
    return re.sub(pattern, subst, phone)
  elif len(phone) in [14, 15]:
    subst = r"+7(\2)\3-\4-\5 доб.\6"
    return re.sub(pattern, subst, phone)
  else:
    return "Не определен"

if __name__ == '__main__':
  memory_dict = {}
  for row in contacts_list:
    row = [elem.strip() for elem in row] # удаление возможных лишних пробелов в начале и конце строк
    full_name = ' '.join(row[0:3]).split() #[Ф,И,О] или [Ф,И]
    if len(full_name) == 2:
      full_name.append('')
    if (full_name[0],full_name[1]) not in memory_dict:
      phone_raw = row[5]
      if phone_raw:
        phone = phone_detector(phone_raw)
      else:
        phone = "Не задан"
      memory_dict.update({(full_name[0],full_name[1]):
                          {'surname': full_name[2], 'organization': row[3],
                          'position': row[4],'phone': phone,'email': row[6]}
                          })
    else:
      if full_name[2]:
         memory_dict[(full_name[0], full_name[1])]['surname'] = full_name[2]
      if row[3]:
         memory_dict[(full_name[0], full_name[1])]['organization'] = row[3]
      if row[4]:
         memory_dict[(full_name[0], full_name[1])]['position'] = row[4]
      if row[5]:
         phone = phone_detector(row[5])
         if phone != "Не определен":
            memory_dict[(full_name[0], full_name[1])]['phone'] = phone
      if row[6]:
         memory_dict[(full_name[0], full_name[1])]['email'] = row[6]
  pprint(memory_dict)

  contacts_list = []
  for person in memory_dict:
    contacts_list.append([person[0], person[1], memory_dict[person]['surname'],
                          memory_dict[person]['organization'],memory_dict[person]['position'],
                          memory_dict[person]['phone'],memory_dict[person]['email']])
  #код для записи файла в формате CSV
  with open("phonebook.csv", "w", newline='', encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)