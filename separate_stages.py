import json

stage = input('Which stage of the game would you like to prepare data for? ("p" - preflop, "f" - flop, "r" - river, "t" - turn) ')
while stage not in ['p', 'f', 'r', 't']:
    stage = input('Please select one of "p", "f", "r" and "t". ')

stages = {'p': ('preflop', 0), 'f': ('flop', 3), 'r': ('river', 4), 't': ('turn', 5)}
stage_data_string = 'game_data/encoded_' + stages[stage][0] + '.json'
fout = open(stage_data_string, 'w')

foutObj = [[], []]

total = sum(1 for line in open('encoded_basic.json')) - 2

with open('encoded_basic.json', 'r') as f:
    curr = 0
    lines = f.readlines()
    idx = 1
    while len(lines[idx]) > 1:
        try:
            obj = json.loads(lines[idx][:-2])
            board = obj['board'][:stages[stage][1]]

            for player in obj['players']:
                X = []
                X.append(player[0])

                if board:
                    X.append(board)

                foutObj[0].append(X)
                foutObj[1].append(player[1])

            curr += 1
            print('{} out of {} hands processed. {:.2%} done.'.format(curr, total, curr/total), end='\r')
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
            print('{} out of {} hands processed. {:.2%} done.\nProcessing complete.'.format(curr, total, curr/total))
            break

print('Writing to file...')
fout.write(json.dumps(foutObj))
print('Data transferred.')