import json
import time
import badger2040
badger = badger2040.Badger2040()

FONT_SCALE=0.5

def clear_screen():
    badger.pen(15)
    badger.clear()
    badger.pen(0)

def write_text(text, x, y, scale):
    badger.text(text, x, y, scale)
    print(text)


def read_scenario():
    f = open("scenario.json","r")
    data = json.load(f)
    f.close()

    start_node_id = ""
    nodes_list = []
    for node in data['nodes']:
        nodes_list.append((node['id'], node))
        if node['type'] == 'Start':
            start_node_id = node['id']

    nodes_dict = dict(nodes_list)

    start_node = nodes_dict[start_node_id]

    still_playing = True
    next_current_node = start_node

    while still_playing:
        clear_screen()

        current_node = next_current_node

        if current_node['type'] == 'Start' or current_node['type'] == 'Message':
            write_text(current_node['message'], 5, 5, scale=FONT_SCALE)
            write_text('Press A to continue', 5, 95, scale=FONT_SCALE)
            badger.update()

            next_current_node = nodes_dict[current_node['next']]

            while True:
                if badger.pressed(badger2040.BUTTON_A):
                    break
                badger.halt()

        if current_node['type'] == 'End':
            final_msg = 'You lost. Press A to continue' if current_node['kind'] == 'Defeat' else 'You won! Congratulations!'

            still_playing = False
            write_text(current_node['message'], 5, 5, scale=FONT_SCALE)
            write_text(final_msg, 5, 20, scale=FONT_SCALE)
            badger.update()

            while True:
                if badger.pressed(badger2040.BUTTON_A):
                    break
                badger.halt()

        if current_node['type'] == 'StoryChoice':
            choices = current_node['choices']
            write_text(current_node['message'], 5, 5, scale=FONT_SCALE)
            i = 1
            for choice in choices:
                write_text('{}. {}'.format(i, choice['message']), 5, 20+i*20, scale=FONT_SCALE)
                i = i + 1

            ans = 0
            while True:
                if badger.pressed(badger2040.BUTTON_A):
                    ans = 1
                    break
                if badger.pressed(badger2040.BUTTON_B):
                    ans = 2
                    break
                if badger.pressed(badger2040.BUTTON_C):
                    ans = 3
                    break

            if ans > len(choices):
                next_current_node = current_node
                continue

            next_current_node = nodes_dict[choices[ans - 1]['next']]

def main_menu():
    clear_screen()
    write_text('Welcome to HS3 Adventure Game!', 5, 20, scale=FONT_SCALE)
    write_text('Please pick', 5, 45, scale=FONT_SCALE)
    write_text('A. Start a new game', 5, 90, scale=FONT_SCALE)
    write_text('B. Exit', 5, 110, scale=FONT_SCALE)
    badger.update()
    while True:
        if badger.pressed(badger2040.BUTTON_A):
            read_scenario()
            break
        if badger.pressed(badger2040.BUTTON_B):
            return False

        badger.halt()
    return True

def main():
    next_round = True
    while next_round:
        next_round = main_menu()

if __name__ == "__main__":
    main()

