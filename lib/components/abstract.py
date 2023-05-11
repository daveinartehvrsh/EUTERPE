from abc import ABC, abstractmethod

import logging
logger = logging.getLogger('my_logger')

class Component(ABC):

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name
    
    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data
    
    def get_len(self):
        return len(self.data)
    
    def __len__(self):
        return self.get_len(self)

    @abstractmethod
    def get_info(self):
        ...

class AudioComponent(Component):
    ...

class ValueComponent(Component):
    ...

class Algorithm(Component):
    ...

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

class ContainerNode(Component):
    def __init__(self, data=None, parent=None):
        self.data = data
        self.parent = parent

    def __str__(self):  
        return f'({self.data})'
    
    def get_heir(self):
        if isinstance(self.data, (Container, Sequence)):
            return self.data.get_heir()
        else:
            return self.data

    def get_info(self):
        if isinstance(self.data, Component):
            return self.data.get_info()
        else:
            print('(audio)')
            
class ContainerIter():
    def __init__(self, container):
        self.data = container.data
        self.size = container.size
        self.index = 1

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index <= self.size:
            item = self.data[self.index - 1]
            self.index += 1
            return item
        raise StopIteration

class Container(Component):
    def __init__(self, name='container'):
        self.name = name
        self.size = 0
        self.data = []

    def get_size(self):
        return self.size

    def add_item(self, item):
        self.data.append(ContainerNode(item, self.get_name()))
        if self.size == 0:
            self.heir = item
        self.size += 1
        if isinstance(item, Component):
            logger.debug(f'     added item: "{item.get_name()}" to "{self.get_name()}" Container')

    def get_heir(self):
        return self.get_data()[0].get_heir()

    def get_nodes(self):
        return self.data
    
    def get_items(self):
        array=[]
        for item in self.get_nodes():
            array.append(item.data)
        return array
    
    def get_info(self):
        print(self.get_name())
        for x in self.data: 
            x.get_info()

    def __iter__(self):
        return ContainerIter(self)
    
    def remove(self, item):
        for x in self.get_data():
            if x.get_data() == item:
                self.data.remove(x)
                self.size -= 1
                return True
        return False

class BeatMaker(Algorithm):
    def create_section(self, name):
        ...

class AudioSelectionSystem(Algorithm):
    def create_dataset(self, name):
        ...
