import random as rnd
import spacy
sp = spacy.load('en_core_web_sm')
from transformers import pipeline, set_seed
generator = pipeline('text-generation', model='distilgpt2')
question_answerer = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')

prohibited_words = ['topic', 'game', 'I', 'the project', 'number', 'things', 'thing', 'fields']
prohibited_parts_of_speech = ['PRON']

# generator = pipeline('text-generation', model='distilgpt2')
# question_answerer = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')

# prohibited_words = ['topic', 'game', 'I', 'the project', 'number', 'things', 'thing', 'fields']
# prohibited_parts_of_speech = ['PRON']

def create_list ():
    my_sent = generator('I am', max_length = 30, num_return_sequences=1)
    my_sent = my_sent[0]['generated_text']
    return my_sent

def activity_finder():
        activity = 'not found'
        while activity == 'not found':
                useful_sentences = [
                        'write a book about',
                        'read a book about',
                        'I will study the', 'I will try to', 'I will write about the', 'I will do a drawing of',
                        'I will do a drawing of a', 'I will design the', 'I will design',
                        'Explain everything about why',
                        'Explain everything about the',
                        'Explain everything about',
                        'Tell me everything about how',
                        'I will explain everything about',
                        'What is the science of',
                        'I will study the behavior of']

                lenght_of_starters = len(useful_sentences) -1
                index = rnd.randint(0, lenght_of_starters)
                sentence_starter = useful_sentences[index]

                separated_context = generator(sentence_starter, max_length = 30, num_return_sequences=3)

                context = ''
                for dictionary in separated_context:
                        context += str(dictionary['generated_text']) + '/n '

                result = question_answerer(question="What do I have to do today?",     context=context)
                
                # elaborating the todo
                to_do = result['answer']
                doc = sp(to_do)
                all_pos = []
                all_morph = []
                for token in doc:
                        all_pos.append(token.pos_)
                        all_morph.append(token.morph)

                ### PROHIBITED WORDS
                splitted_to_do = to_do.split(' ')
                prohibited_words = ['topic', 'game', 'I', 'the project']
                if any(word in prohibited_words for word in splitted_to_do) or 'PRON' in all_pos:
                        # print('prohibited word')
                        # print(to_do)
                        pass

                ### LOOP 1
                elif all_pos[0:3] == ['VERB', 'DET', 'NOUN'] or all_pos[0:3] == ['VERB', 'DET', 'PROPN'] and 'VerbForm=Inf' in str(all_morph[0]):
                        to_do = to_do.split(' ')
                        # 1.a
                        if len(all_pos) == 3:
                                act = context.split(sentence_starter + ' ')[1].split('.')[0]
                                to_do = ' '.join([to_do[0], act])
                                #     print('loop1a')
                                activity = 'found'
                        else:
                                to_do[1] = 'the'
                                # print('loop1')
                                to_do = ' '.join(to_do)
                                activity = 'found'

                ### LOOP 2
                elif all_pos[0] == 'NOUN' or all_pos[0] == 'PRON':
                        # print('loop2')
                        # print(to_do)
                        pass
                
                ### LOOP 3
                elif all_pos[0] == 'DET': ## unless it starts with a drawing
                        # print('loop3')
                        starter = ['read a book about', 'draw', 'write about', 'observe the details of a', 'study the mathematics behind', 'explain everything about',
                        'design', 'study the science of']

                        lenght_of_sub_starter = len(starter) -1
                        index = rnd.randint(0, lenght_of_sub_starter)
                        selected_starter = starter[index]

                        to_do = ' '.join([selected_starter, to_do])
                        activity = 'found'
                

                ### LOOP 4  
                elif len(to_do.split(sentence_starter+' ')) >1:
                        to_do = to_do.split(sentence_starter+' ')[-1]
                        doc = sp(to_do)     
                        if len([word for word in to_do.split(' ') if len(word) > 3]) >3 or 'PROPN' in [token.pos_ for token in doc]:
                                starter = ['read a book about', 'draw', 'write about', 'observe', 'study the mathematics behind', 'explain everything about',
                                        'design', 'study the science of']
                                lenght_of_sub_starter = len(starter) -1
                                index = rnd.randint(0, lenght_of_sub_starter)
                                selected_starter = starter[index]
                                to_do = ' '.join([selected_starter, to_do])
                                #     print('loop4')
                                activity = 'found' 
                        
                elif len(to_do.split(' ')) > 7 and 'VerbForm=Inf' in str(all_morph[0]):
                        # print('loop5')
                        activity = 'found'
                ### LOOP 5
                else:
                        # print('loop6')
                        # print(to_do)
                        pass

                
                

        return(to_do)

def time_generator():
    number = rnd.randint(8,22)
    if number > 12:
        number -= 12
        hour = f'{str(number)} PM'
    elif number < 12:
        hour = f'{str(number)} AM'
    else:
        hour = f'{str(number)} PM'
    return hour