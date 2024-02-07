import json
from encoding import encode_hand

fout = open("encoded_basic.json", "w")
fout.write('[\n')
total = sum(1 for line in open('hands_valid.json'))

with open('hands_basic.json', 'r') as f:
    curr = 0
    lines = f.readlines()
    idx = 1
    while len(lines[idx]) > 1:
        try:
            obj = json.loads(lines[idx][:-2])
            obj['board'] = encode_hand(obj['board'])
            players = []
            for player in obj['players']:
                players.append(
                    (
                        encode_hand(player['pocket_cards']), 
                        player['won']
                    )
                )
                obj['players'] = players
                
            
            fout.write(json.dumps(obj) + ',\n')
            curr += 1
            print('{} out of {} processed. {:.2%} done.'.format(curr, total, curr/total), end='\r')
            idx += 1
            
        except json.JSONDecodeError:
            obj = json.loads(lines[idx][:-1])
            obj['board'] = encode_hand(obj['board'])
            players = []
            for player in obj['players']:
                players.append(
                    (
                        encode_hand(player['pocket_cards']), 
                        player['won']
                    )
                )
                obj['players'] = players
                
            
            fout.write(json.dumps(obj))
            curr += 1
            print('{} out of {} processed. {:.2%} done.'.format(curr, total, curr/total))
            break

fout.write('\n]')