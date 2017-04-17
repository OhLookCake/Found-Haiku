import sys
import pronouncing
import re

def main():

    if len(sys.argv)>1:
        text = sys.argv[1]
    else:
        text = 'This is a dummy padding sentence. To be or not to be that is the question. This is a testicle. More dummy padding. Cat cat CAT cAt CaT cat cat CAt CAT caT Cat cat cat cat Cat CAT cat!!! Balloon. '

    #pre-preprocess and clean

    specials = '"()-,:;'
    enders = '\.\?\!'

    text = re.sub('([' + specials + '])', ' \\1 ', text)
    text = re.sub('([' + enders + ']+)', ' \\1 ', text)

    text = re.sub('\s',' ',text)
    #text = re.sub('\s+',' ',text) #clean up spaces
    print(text)


    collector = ''
    preceding = ''
    listcollector = []
    listpreceding = []

    counter = 0
    precedingcounter = 0

    for word in text.split(' '):  #not the same as .split()!
        if word == '':
            collector+=' '
            listcollector.append(word)

        elif re.match('^['+enders+']+$', word):
            collector += word
            listcollector.append(word)

            if counter == 17:
                haikufy(collector, listcollector)
            elif precedingcounter + counter == 17:
                haikufy(preceding + ' ' + collector, listpreceding + listcollector)
            elif counter < 17:
                preceding = collector
                listpreceding = listcollector[:] #making a copy
                precedingcounter = counter

            collector = ""
            listcollector = []
            counter = 0


        elif word in specials:
            collector+=word
        else:
            numsyllables = count_syllables_in_word(word)
            if numsyllables == None:
                numsyllables = guess_syllables(word)

            #Now we have a count, irrespective of source
            collector += ' ' + word
            listcollector.append(word)
            counter += numsyllables
            #print(word, numsyllables, counter)
    #for loop ends


def count_syllables_in_word(word):
    word = word.lower()
    phones = pronouncing.phones_for_word(word)[0]
    if len(phones) > 0:
        return sum([pronouncing.syllable_count(p) for p in phones])
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

def haikufy(text, listtext):
    #TODO: Pretty print this.
    text = re.sub('\s+',' ',text) #clean up spaces
    print('HAIKU>', text)


if __name__ == "__main__":
    main()
