
class Empty(Exception):
    pass


class LinkedList:
    class _Node:
        __slots__ = '_element', '_next'
        
        def __init__(self, element, next):
            self._element = element
            self._next = next
            
    
    def __init__(self):
        self._head = None
        self._size = 0
        
    def is_empty(self):
        return self._size == 0
    
    def __len__(self):
        return self._size
    
    def push(self, e):
        self._head = self._Node(e, self._head)
        self._size +=1
        
    def top(self):
        if self.is_empty():
            return Empty
        return self._head._element
        
    def pop(self):
        if self.is_empty():
            return Empty
        ans = self._head._element
        self._head = self._head._next
        self._size -=1
        return ans
    
    def print(self):
        if self.is_empty():
            print('Linked List is empty')
            
        itr = self._head 
        llstr = ''
        
        while itr:
            llstr += str(itr._element) + '--->'
            itr = itr._next
        
        print(llstr)
        
    def remove_at(self, index):
        if self.is_empty():
            print('Linked List is empty')
            
        if index<0 or index>self.__len__():
            raise Exception('Invalid Index')
        
        if index==0:
            self._head = self._head._next
            return
        
        count = 0
        itr = self._head
        while itr:
            if count == index-1:
                itr._next = itr._next._next 
                break
            
            itr = itr._next
            count+=1
            
        self._size-=1
    
    def loop(self, k):
        itr = self._head 
        llstr = ''
        count = 0
        while itr:
            if count == k:
                llstr += str(itr._element) + '--->'
                itr = itr._next    
            else:
                itr = itr._next
                count+=1
        print(llstr)                 
    
    def insert_at_start(self, e):
        self.push(e)

    def insert_at(self, index, e):
        if index < 0 or index > self._size:
            raise Exception('Invalid Index')
        if index == 0:
            self.push(e)
            return
        count = 0
        itr = self._head
        while itr:
            if count == index - 1:
                node = self._Node(e, itr._next)
                itr._next = node
                self._size += 1
                return
            itr = itr._next
            count 
        self._size +=1
        
    
if __name__ == "__main__":
    """lists = LinkedList()
    lists.push(1)
    lists.push(2)
    lists.push(3)
    print(lists.__len__())
#    lists.insert_at(, 10)
#    print(lists.__len__())
    lists.print()
    lists.remove_at(2)
    lists.print()
#    print(lists.top())"""
    
    ll = LinkedList()

    # Test pushing elements
    ll.push(10)
    ll.push(20)
    ll.push(30)
    print('List after pushing 30, 20, 10:')
    ll.print()

    # Test top element
    print('Top element:', ll.top())

    # Test popping elements
    print('Popped element:', ll.pop())
    print('List after popping top element:')
    ll.print()

    # Test inserting at start
    ll.insert_at_start(40)
    print('List after inserting 40 at start:')
    ll.print()

    # Test inserting at specific index
    ll.insert_at(1, 50)
    print('List after inserting 50 at index 1:')
    ll.print()

    # Test removing from specific index
    ll.remove_at(2)
    print('List after removing element at index 2:')
    ll.print()

    # Test length of list
    ll.push(20)
    ll.push(204)
    ll.push(207)
    
    print('Final List:')
    ll.print()
    print('Current size of list:', len(ll))
    
    ll.loop(k=3)


        