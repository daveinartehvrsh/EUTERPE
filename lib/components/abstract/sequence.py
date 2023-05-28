from lib.components.abstract.abstract import Component

class SequenceNode():
    def __init__(self, data, next=None, prev=None):
        self.data = data
        self.next_node = next
        self.prev_node = prev
    
    def __str__(self):
        return f'[{self.data.getRepr()}]'
    
class Sequence(Component):
    
    def __init__(self, r=None):
        self.root = r
        self.last = r
        self.size = 0

    def add(self, item):
        if self.size == 0:
            self.root = SequenceNode(item)
            self.last = self.root
        else:
            new_node = SequenceNode(item, prev= self.last)
            self.last.next_node = new_node
            self.last = new_node
        self.size += 1
    
    def find(self, item):
        this_node = self.root
        while this_node is not None:
            if this_node.data == item:
                return item
            elif this_node.next_node == None:
                return False
            else:
                this_node = this_node.next_node

    def remove(self, item):
        this_node = self.root
        while this_node is not None:
            if this_node.data == item:
                if this_node.prev_node is not None:
                    if this_node.next_node is not None:
                        this_node.prev_node.next_node = this_node.next_node
                        this_node.next_node.prev_node = this_node.prev_node
                    else:
                        this_node.prev_node.next_node = None
                        self.last = this_node.prev_node
                else:
                    self.root = this_node.next_node
                    this_node.next_node.prev_node = self.root
                self.size -= 1
                return True
            else:
                this_node = this_node.next_node
        return False
    
    def get_heir(self):
        return self.root.get_data()
    
    def get_info(self):
        if self.root is None:
            return 'empty sequence'
        print(f'{self.get_name()} - |', end='')
        this_node = self.root
        print(this_node, end='')
        while this_node.next_node is not None:
            this_node = this_node.next_node
            print(this_node, end='')
        print()

    def get_items(self):
        this_node = self.root
        array=[]
        while this_node.next_node is not None:           
            array.append(this_node.data)   
            this_node = this_node.next_node
        array.append(this_node.data)  
        return array
