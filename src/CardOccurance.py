#!/usr/bin/env python3
from datetime import date


class CardOccurance:

    def __init__(self, card, event, occ, date=None):
        self.card = card
        self.event = event
        self.occ = occ
        self.date = date

    def __eq__(self, o):
        isinstance(o, CardOccurance) and self.card == o.getCard() and self.event == o.getEvent()

    def getCard(self):
        return self.card

    def getEvent(self):
        return self.event

    def getOcc(self):
        return self.occ

    def getDate(self):
        if self.date == None:
            return event.getDate()
        return self.date
