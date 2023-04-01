from lib.abstract import *
import numpy as np

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
    
    def getHeir(self):
        return self.root.data
    
    def getInfo(self):
        if self.root is None:
            return 'empty sequence'
        print(f'{self.getName()} - |', end='')
        this_node = self.root
        print(this_node, end='')
        while this_node.next_node is not None:
            this_node = this_node.next_node
            print(this_node, end='')
        print()

    def getItems(self):
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
    
    def getInfo(self):
        if isinstance(self.data, Component):
            return self.data.getInfo()
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

    def getSize(self):
        return self.size

    def addItem(self, item):
        self.data.append(ContainerNode(item, self.getName()))
        if self.size == 0:
            self.heir = item
        self.size += 1

    def getHeir(self):
        return self.heir.getHeir()

    def get_nodes(self):
        return self.data
    
    def getItems(self):
        array=[]
        for item in self.get_nodes():
            array.append(item.data)
        return array
    
    def getInfo(self):
        print(self.getName())
        for x in self.data: 
            x.getInfo()

    def __iter__(self):
        return ContainerIter(self)
