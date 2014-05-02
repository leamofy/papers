import csv
import operator
import codecs

filename = 'Batch_202996_result.csv'
csv_reader = csv.reader(open(filename))

header_index = {}
for i, header in enumerate(csv_reader.next()):
   header_index[header] = i

hits = []
for hit in csv_reader:
   if hit[header_index['AssignmentStatus']] != 'Rejected':
       hits.append(hit)

amount_worked = {}
for hit in hits:
   worker_id = hit[header_index['WorkerId']]
   num_hits = 0
   if worker_id in amount_worked:
      num_hits = amount_worked[worker_id]
   amount_worked[worker_id] = num_hits + 1

#for num_hits, worker_id in sorted(amount_worked.items(), key=operator.itemgetter(1)):
#   print num_hits, worker_id


segments = {}
turkers = {}
for hit in hits:
   for i in range(1, 11):
      seg_id = hit[header_index['Input.seg_id' + str(i)]]
      translation = hit[header_index['Answer.translation' + str(i)]]
      translation = translation.replace('\n', ' ')
      translation = translation.replace('\r', ' ')
      translation = translation.replace('Translation of the first sentence goes here.', '')
      translation = translation.replace('Translation of the second sentence goes here.', '')
      worker = hit[header_index['WorkerId']]
      translations = []
      workers = []
      if seg_id in segments:
         translations = segments[seg_id]
         workers = turkers[seg_id]
      translations.append(translation)
      workers.append(worker)
      segments[seg_id] = translations
      turkers[seg_id] = workers


def read_lines_from_file(filename):
   lines = []
   input_file = codecs.open(filename, encoding='utf-8')
   for line in input_file:
      lines.append(line.rstrip('\n'))
   input_file.close()
   return lines


def write_lines_to_file(output_filename, lines):
    output_file = open(output_filename, 'a')
    for line in lines:
        output_file.write(line.encode('UTF-8'))
        output_file.write('\n'.encode('UTF-8'))            
    output_file.close()



seg_ids = read_lines_from_file('/Users/ccb/Documents/Projects/NIST-MT-Eval-2009/MTurk-Translation-take2/nist09.ur.seg_ids')

lines = []
for seg_id in seg_ids:
   line = unicode('', errors='ignore')
   if seg_id in segments:
      line = unicode(seg_id)
      for translation in segments[seg_id]:
         line = line + unicode('\t', errors='ignore') + unicode(translation, errors='ignore')
   else:
      print seg_id, " not in segments"
   lines.append(line)


write_lines_to_file("output", lines)


lines = []
for seg_id in seg_ids:
   line = unicode('', errors='ignore')
   if seg_id in segments:
      line = unicode(seg_id)
      for worker in turkers[seg_id]:
         line = line + unicode('\t', errors='ignore') + unicode(worker, errors='ignore')
   else:
      print seg_id, " not in segments"
   lines.append(line)


write_lines_to_file("turkers", lines)
