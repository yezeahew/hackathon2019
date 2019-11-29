def search(query, file_name):
    file = open(file_name, 'r')
    query_words = query.split()
    return_lines = []

    for line in file:
        line = line.split('\n')
        
        if line != '':
            for words in line:
                words = ' '.join(words.split("/"))
                words = ' '.join(words.split('.'))
                words = ' '.join(words.split(')'))
                words = ' '.join(words.split('('))
                words = ' '.join(words.split('$'))
                words = ' '.join(words.split('!'))
                words = ' '.join(words.split('?'))
                words = ' '.join(words.split(':'))
                words = ' '.join(words.split(','))
                words = ' '.join(words.split('-'))
                words = words.split()
                for word in words:
                    for q in query_words:
                        if word.lower() == q.lower():
                            return_lines.append(line[0])
                            break

    return return_lines

# print(search('who is jim','/Users/megano/Desktop/u/a.txt'))
