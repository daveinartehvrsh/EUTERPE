from lib.components.abstract.abstract import Component

class ContainerNode(Component):
    def __init__(self, data=None, parent=None):
        self.data = data
        self.parent = parent

    def __str__(self):  
        return f'({self.data})'
    
    def get_heir(self):
        if isinstance(self.data, Component):
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
