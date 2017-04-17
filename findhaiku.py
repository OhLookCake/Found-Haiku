import sys
import pronouncing
import re

def main():

    text = ' '.join(sys.stdin.readlines())
    #Pre-preprocess and clean

    specials = '"()-,:'
    enders = '\.\?\!;'

    text = re.sub('([' + specials + '])', ' \\1 ', text)
    text = re.sub('([' + enders + ']+)', ' \\1 ', text)

    text = re.sub('\s',' ',text)
    #text = re.sub('\s+',' ',text) #clean up spaces


    collector = ''
    preceding = ''

    counter = 0
    precedingcounter = 0

    checkpoints = 0 #keeps track of if the counter ever reached 6 (checkpoints++) and 12 (checkpoints++) syllable counts
    checkpointswithpreceding = 0

    for word in text.split(' '):  #not the same as .split()!
        if word == '':
            collector+='  '

        elif re.match('^['+enders+']+$', word):
            collector += ' ' + word

            if counter == 17 and checkpoints == 2:
                haikufy(collector)
                collector = ''
                preceding = ''
                checkpoints = 0
                checkpointswithpreceding = 0
            elif precedingcounter + counter == 17 and checkpointswithpreceding == 2:
                haikufy(preceding + ' ' + collector)
                collector = ''
                preceding = ''
                checkpoints = 0
                checkpointswithpreceding = 0
            elif counter < 17:
                preceding = collector
                collector = ''
                precedingcounter = counter
                checkpointswithpreceding = checkpoints
                checkpoints = 0
            elif counter > 17:
                preceding = ''
                collector = ''
                counter = 0
                precedingcounter = 0
                checkpoints = 0

            collector = ''
            counter = 0
            checkpoints = 0

        elif re.match('^['+specials+']+$', word):
            collector+= ' ' + word
        else:
            numsyllables = count_syllables_in_word(word)
            if numsyllables == None:
                numsyllables = guess_syllables(word)

            #Now we have a count, irrespective of source
            collector += ' ' + word
            counter += numsyllables
            if counter == 5 or counter == 12:
                checkpoints += 1
            if precedingcounter + counter == 5 or precedingcounter + counter == 12:
                checkpointswithpreceding += 1

    #for loop ends


def count_syllables_in_word(word):
    word = word.lower()

    if not re.match('.*[a-z]',word): #contains only non-alpha characters
        return 0
    phones = pronouncing.phones_for_word(word)
    if len(phones) > 0:
        return sum([pronouncing.syllable_count(p) for p in phones[0]])
    else:
        return None


def guess_syllables(word):
    count = 0
    vowels = 'aeiouy'
    word = word.lower().strip('.:;?!')
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count+=1
    if count == 0:
        count +=1
    return count

def haikufy(text):
    haiku=''
    specials = '"()-,:;'
    enders = '\.\?\!'
    counter = 0

    for word in text.split(' '):  #not the same as .split()!
        if word == '':
            haiku+=' '

        elif re.match('^['+enders+']+$', word) or re.match('^['+specials+']+$', word):
            haiku += word

        else:
            numsyllables = count_syllables_in_word(word)
            if numsyllables == None:
                numsyllables = guess_syllables(word)

            #Now we have a count, irrespective of source
            haiku += ' ' + word
            counter += numsyllables
            #print(word, counter)

            if counter == 5 or counter == 12:
                haiku+='\r\n'

    #Fix puntuation as much as possible
    haiku = re.sub('(\w) +([' + enders + '])','\1\2',haiku) #clean up spaces
    for e in '.!?;,:':
        haiku = re.sub('([\r\n]+)\\' + e, e +'\r\n',haiku) #clean up spaces
    # Do not try to regexify this for loop. It won't work.


    haiku = re.sub(' +',' ',haiku) #clean up spaces
    print(haiku,'\n----------------')


if __name__ == "__main__":
    main()
