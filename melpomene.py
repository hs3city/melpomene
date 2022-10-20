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

def choice_with_scroll(choice_node):
    print_things = []
    print_things.append(("", choice_node['message']))
    for choice in choice_node['choices']:
        print_things.append((choice['next'], choice['message']))

    next_id = ""

    still_chosing = True
    while still_chosing:
        i = 0
        for print_thing in print_things:
            clear_screen()
            if i == 0:
                write_text(print_thing[1], 5, 5, scale=FONT_SCALE)
                write_text('Press down arrow to see choices', 5, 80, scale=FONT_SCALE)
                badger.update()
                while True:
                    if badger.pressed(badger2040.BUTTON_DOWN):
                        break
                    badger.halt()
            else:
                write_text(print_thing[1], 5, 5, scale=FONT_SCALE)
                write_text('Press down arrow to see more choices', 5, 80, scale=FONT_SCALE)
                write_text('Press A to select', 5, 95, scale=FONT_SCALE)
                badger.update()
                while True:
                    if badger.pressed(badger2040.BUTTON_DOWN):
                        break
                    if badger.pressed(badger2040.BUTTON_A):
                        still_chosing = False
                        next_id = print_thing[0]
                        break
                    badger.halt()

            i = (i + 1) % len(print_things)
            

    return next_id


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
            write_text(final_msg, 5, 60, scale=FONT_SCALE)
            badger.update()

            while True:
                if badger.pressed(badger2040.BUTTON_A):
                    break
                badger.halt()

        if current_node['type'] == 'StoryChoice':
            next_node_id = choice_with_scroll(current_node)
            next_current_node = nodes_dict[next_node_id]

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
