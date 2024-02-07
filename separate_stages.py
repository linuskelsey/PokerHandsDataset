import json

stage = input('Which stage of the game would you like to prepare data for? ("p" - preflop, "f" - flop, "r" - river, "t" - turn, or "a" - all stages) ')
while stage not in ['p', 'f', 'r', 't', 'a']:
    stage = input('Please select one of "p", "f", "r", "t" and "a". ')

stages = {'p': ('preflop', 0), 'f': ('flop', 3), 'r': ('river', 4), 't': ('turn', 5)}
total = sum(1 for line in open('encoded_basic.json')) - 2

def separate_stage(stage):
    stage_data_string = 'game_data/encoded_' + stages[stage][0] + '.json'
    fout = open(stage_data_string, 'w')

    foutObj = [[], []]

    with open('encoded_basic.json', 'r') as f:
        curr = 0
        hand_count = 0
        lines = f.readlines()
        idx = 1
        while len(lines[idx]) > 1:
            try:
                obj = json.loads(lines[idx][:-2])
                board = obj['board'][:stages[stage][1]]

                for player in obj['players']:
                    X = []
                    X += player[0]

                    if board:
                        X += board

                    foutObj[0].append(X)
                    foutObj[1].append(player[1])

                    hand_count += 1

                curr += 1
                print('{} out of {} hands processed, with {} data points created. {:.2%} done.'.format(curr, total, hand_count, curr/total), end='\r')
                idx += 1

            except json.JSONDecodeError:
                obj = json.loads(lines[idx][:-1])
                board = obj['board'][:stages[stage][1]]

                for player in obj['players']:
                    X = []
                    X.append(player[0])

                    if board:
                        X.append(board)

                    foutObj[0].append(X)
                    foutObj[1].append(player[1])

                curr += 1
                print('{} out of {} hands processed, with {} data points created. {:.2%} done.\nProcessing complete.'.format(curr, total, hand_count, curr/total))
                break

    print('\nWriting to file...')
    fout.write(json.dumps(foutObj))
    print('Data transferred.')

if stage != 'a':
    separate_stage(stage)

else:
    count = 1
    for stg in stages.keys():
        print('\n ---- {}/4: PROCESSING {} ---- '.format(count, stages[stg][0].upper()))
        separate_stage(stg)
        count +=1