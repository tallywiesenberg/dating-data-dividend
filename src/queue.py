import random

from flask import render_template
import keyboard

from model import User, Swipe

class SwipeQueue:
    
    def __init__(self, user, queue):
        self.user = user
        self.queue = User.query.all().remove(user)

    def add_user_to_queue(self, user):
        random.shuffle(self.queue)
        self.queue.append(user)
    
    def swipe(self):
        #if the user has no more people in the radius, relay message to user with template
        if not self.queue:
            return render_template('no_more_users.html')
        #else, show next user

        #elif user swipes left
        #   append to left-swipe data structure 
        #   show next user

        #elif user swipes right
        #   if match
        #       alert both users
        #       disperse funds to both users
        #   show next user
        pass
    def process_key_input(self):
        if keyboard.is_pressed('p'):
            return render_template('profile_editor.html', user=self.user)
        elif keyboard.is_pressed('left'):
            return 'left'
        elif keyboard.is_pressed('right'):
            return 'right'
        else:
            pass
            

# user = self.queue.pop(0)

