class LogNode:
    def __init__(self, event):
        self.event = event
        self.prev = None
        self.next = None

class DoublyLinkedList: 
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def append_log(self, event):
        new_node = LogNode(event)
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
            self.current = new_node