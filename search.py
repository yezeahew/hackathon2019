def search(query, file_name):
    file = open(file_name, 'r')
    texts = []

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
                    if word.lower() == query.lower():
                        print(line[0])
                        break

# search('jim','/Users/megano/Desktop/u/a.txt')
