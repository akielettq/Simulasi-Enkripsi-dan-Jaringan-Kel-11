class ServerNode:
    def __init__(self, server_name):
        self.server_name = server_name
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def add_server(self, server_name):
        new_node = ServerNode(server_name)
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
            new_node.next = self.head 
        else:
            self.tail.next = new_node
            self.tail = new_node
            self.tail.next = self.head 

    def get_next_server(self):
        if self.head is None:
            return None
            
        selected_server = self.current.server_name
        self.current = self.current.next 
        return selected_server