
from __future__ import annotations
from typing import List, Union


class Article:
    name: str
    loc: int
    box_parent: Box
    amount: int
    def __init__(self, name, amount=1, loc=-1, box=None):
        '''
        Name of article, amount of units (int), location on the map (int), the box it is inside of (Box).
        '''
        self.name = name  # Inicializa el atributo 'name'
        self.loc = loc    # Inicializa el atributo 'loc'
        self.amount = amount   # Inicializa el atributo 'amount'
        self.box_parent = box  # Inicializa el atributo 'box'

    def set_name(self, new_name: str):
        '''
        Overwrites the name of the article to the specified string.
        '''
        self.name = new_name  # Método para cambiar el atributo 'name'

    def set_amount(self, new_amount: int):
        '''
        Sets the amount (int) of these items which are together.
        '''
        self.amount = new_amount

    def set_loc(self, new_loc: int):
        '''
        Sets its location (int).
        '''
        self.loc = new_loc  # Método para cambiar el atributo 'loc'

    def box_in(self, parent: Box):
        '''
        Boxes itself into an existing box (Box).
        '''
        self.is_boxed = True  
        self.box_parent.append(parent)
        parent.box_sons.append(self)

# Getters
    def get_name(self):
        return self.name  # Retorna el atributo 'name'

    def get_loc(self):
        return self.loc  # Retorna el atributo 'loc'


class Box:
    loc: int
    box_sons: List[Union[Box, Article]]
    box_parent: Box
    is_boxed: bool
    box_id: str
    amount: int
    def __init__(self, box_id, loc=-1, amount=1, box_sons=[], box_parent=None):
        '''
        Box ID, location on the map, amount (int), list of sons, parent box (Box).
        '''
        self.box_id = box_id            # Identificador único para la caja
        self.loc = loc
        self.box_sons = box_sons         # Referencia al "hijo" de la caja, puede ser otra caja u objeto
        self.box_parent = box_parent    # Referencia a la "caja padre", si está anidada dentro de otra caja
        if box_parent != None:
            self.is_boxed = True       # Indica si está embalada (True o False)
        else:
            self.is_boxed = False

    def set_box_id(self, new_id):
        '''
        New ID (str)
        '''
        self.box_id = new_id  # Método para cambiar el 'box_id'

    def set_location(self, location):
        '''
        New location (int)
        '''
        self.loc = int(location)

    def unbox(self):
        '''
        You take out this box from its parent box
        '''
        self.is_boxed = False  
        self.box_parent = None

    def box_in(self, parent: Box):
        '''
        New parent (Box)
        This removes the current parent and sets a new one.
        '''
        self.is_boxed = True  
        self.box_parent = parent
        parent.box_sons.append(self)


# Getters
    def get_box_id(self):
        return self.box_id  # Retorna el 'box_id'

    def get_is_boxed(self):
        return self.is_boxed  # Retorna el estado de 'is_boxed'

    def get_box_sons(self):
        return self.box_sons  # Retorna el contenido del 'box_son'

    def get_box_parent(self):
        return self.box_parent  # Retorna el contenido del 'box_parent'








