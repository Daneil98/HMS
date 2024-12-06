class Queue:
    
    DEFAULT_CAPACITY = 20
    
    def __init__(self):
        #'create an empty queue'
        self._data = [None] * Queue.DEFAULT_CAPACITY
        self._size = 0          #size of queue
        self._front = 0         #front of the queue
        
    def __len__(self):
        return self._size
    
    def is_empty(self):
        return self._size == 0
    
    def first(self):
        #'return but dont remoce the element at the front of the queue and raise an exception if empty'
        if self.is_empty():
            raise Exception('Queue is empty')
        return self._data[self._front]
    
    def dequeue(self):
        #remove the first element in the queue
        if self.is_empty():
            raise Exception('Queue is empty')
        answer = self._data[self._front]
        self._data[self._front] = None
        self.front = (self._front + 1) % len(self._data)
        self._size -= 1
        return answer
    
    def enqueue(self, e):
        #add an element to the back of the queue
        if self._size == len(self._data):
            self._resize(2*len(self._data))
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = e
        self._size += 1
        
    def _resize(self, cap):
        old = self._data
        self._data = [None] * cap
        walk = self._front
        for k in range(self._size):
            self._data[k] = old[walk]
            walk = (1 + walk) % len(old)
        self._front = 0
            