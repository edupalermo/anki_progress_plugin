from aqt import mw, gui_hooks
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
from . import MainWindow


def testFunction() -> None:
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.cardCount()
    # show a message box
    showInfo("Card count: %d" % cardCount)


def reviewer_did_answer_card(reviewer, card, easy) -> None:
    update_progress()


def aaa(a) -> None:
    # showInfo("overview_did_refresh")
    pass


def state_did_change(new_state, old_State) -> None:
    if new_state == 'review':
        update_progress()
        window.show()
        mw.setFocus()
    elif new_state != 'review':
        window.hide()


def update_progress():
    deck_id = mw.col.decks.current()['id']
    config = mw.col.decks.get_config(1)
    card_to_be_done = len(mw.col.find_cards('did:%d and is:due' % deck_id))
    window.update_current_deck({
        'done': len(mw.col.find_cards('did:%d and rated:1' % deck_id)),
        'total': min(config['rev']['perDay'], card_to_be_done)
    })
    window.update_current_accumulated_deck({
        'done': len(mw.col.find_cards('did:%d and rated:1' % deck_id)),
        'total': card_to_be_done
    })

    card_to_be_done = 0
    for deck in mw.col.decks.all():
        card_to_be_done = card_to_be_done + min(config['rev']['perDay'],
                                                len(mw.col.find_cards('did:%d and is:due' % deck['id'])))

    len(mw.col.find_cards('is:due'))
    window.update_all_decks({
        'done': len(mw.col.find_cards('rated:1')),
        'total': card_to_be_done
    })
    window.update_all_accumulated_decks({
        'done': len(mw.col.find_cards('rated:1')),
        'total': len(mw.col.find_cards('is:due'))
    })

    data = [None] * 61
    for i in range(61):
        data[i] = len(mw.col.find_cards('did:%d and prop:due=%d' % (deck_id, i)))
    window.update_future_due_chart(data)


# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)

gui_hooks.reviewer_did_answer_card.append(reviewer_did_answer_card)
gui_hooks.overview_did_refresh.append(aaa)
gui_hooks.state_did_change.append(state_did_change)

window = MainWindow.MainWindow()




