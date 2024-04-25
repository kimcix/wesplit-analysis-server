"""
    Classes for setting up Observer pattern for Users

    Wow! No imports :)
"""

class User():
    def __init__(self, username):
        self.username = username
        self.connection_lost = False

        self._single_queue = False

    def set_queue(self):
        self._single_queue = True
    
    def notify_client(self):
        if (self._single_queue):
            self._single_queue = False
            return True
        else:
            return False
    
    def mark_connection_lost(self):
        self.connection_lost = True


class SubInbox():
    def __init__(self):
        self.subscribers = set()
    
    def addSubscriber(self, user: User):
        self.subscribers.add(user)
        print(f"Added subscriber {user} to Set({self.subscribers})\n")
    
    def removeSubscriber(self, user: User):
        self.subscribers.remove(user)
        print(f"Removed subscriber {user} from Set({self.subscribers})\n")
    
    def findSubscriberByName(self, username):
        for subscriber in self.subscribers:
            if username == subscriber.username:
                return subscriber

        return None

    def notify(self, username):
        for subscriber in self.subscribers:
            if username == subscriber.username:
                print(f"Will notify {username} on new entry\n")
                subscriber.set_queue()
                break
