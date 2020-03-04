#!/usr/bin/env python3
from datetime import date


class CardOccurance:

    def __init__(self, card, event, occ, date=None):
        self.card = card
        self.event = event
        self.occ = occ
        if not date==None:
            self.date = date
        else:
            self.date = event.date
        self.id = str(card.echo_id)+ ":" + str(event.id)+ ":" + str(self.date)

        self.price = self.card.price.loc[self.date]['price']

    def __eq__(self, o):
        isinstance(o, CardOccurance) and self.card == o.card and self.event == o.event

    def getCard(self):
        return self.card

    def getEvent(self):
        return self.event

    def getOcc(self):
        return self.occ

    def getPrice(self):
        return self.card.getPrice().loc[self.getDate()]['price']

    def getDate(self):
        return self.date
