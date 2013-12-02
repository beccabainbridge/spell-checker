with open('word_frequencies.csv') as f:
            f = f.read().split('\n')
            frequencies = {}
            for row in f:
                word, freq = row.split(',')
                frequencies[word] = freq

with open('freqs.csv') as f:
            f = f.read().split('\n')
            for row in f:
                word, freq = row.split(',')
                if word in frequencies:
                    frequencies[word] += freq
                else:
                    frequencies[word] = freq

outputfile = open("combined_freqs.csv", "w")
for word in frequencies:
    outputfile.write("%s,%s\n" %(word, frequencies[word]))
outputfile.close()
