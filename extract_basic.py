import json

fout = open('hands_basic.json', 'w')
fout.write('[\n')
total = sum(1 for line in open('hands_valid.json'))
with open('hands_valid.json', 'r') as f:
    # Running total for number of rounds processed
    curr = 0
    line = f.readline()
    while line:
        hand = json.loads(line)
        # Clean to only include whether players won or not
        for player in hand['players']:
            player['won'] = 0
            if player['winnings'] > 0:
                player['won'] = 1

            del player['user'], player['bets'], player['bankroll'], player['action'], player['pos'], player['winnings']

        del hand['game'], hand['dealer'], hand['pots'], hand['time']

        curr += 1
        fout.write(json.dumps(hand) + ',\n')
        print('{} out of {} processed. {:.2%} done.'.format(curr, total, curr/total), end='\r')
        line = f.readline()

fout.write('\n]')
print('\n     NOTE: Remove trailing comma in hands_basic.json.')