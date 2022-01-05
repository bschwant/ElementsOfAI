''' Simple script to get rid of the POS tagging in train-text from part1, store changes to newtext'''

fn = open("newText.txt", 'w')

with open("train-text.txt") as f:
    for line in f:
        line2 = ""
        for i,word in enumerate(line.split()):
            if (i % 2 == 0):
                line2 += word
                line2 += " "
        fn.write(f"{line2}\n")

fn.close()