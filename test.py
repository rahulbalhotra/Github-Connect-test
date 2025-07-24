class Node:
    """
    A node in a singly linked list.
    """
    def __init__(self, data=None):
        """
        Initializes a Node.
        Args:
            data: The data to be stored in the node.
        """
        self.data = data
        self.next = None

class LinkedList:
    """
    A singly linked list implementation.
    """
    def __init__(self):
        """
        Initializes an empty LinkedList.
        """
        self.head = None

    def append(self, data):
        """
        Appends a new node with the given data to the end of the list.
        Args:
            data: The data for the new node.
        """
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def prepend(self, data):
        """
        Prepends a new node with the given data to the beginning of the list.
        Args:
            data: The data for the new node.
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, data):
        """
        Deletes the first node containing the specified data.
        Args:
            data: The data of the node to delete.
        """
        current_node = self.head

        # If the head node itself holds the data to be deleted
        if current_node and current_node.data == data:
            self.head = current_node.next
            current_node = None
            return

        prev_node = None
        # Search for the node to be deleted, keep track of the previous node
        while current_node and current_node.data != data:
            prev_node = current_node
            current_node = current_node.next

        # If data was not present in the linked list
        if not current_node:
            print(f"Data '{data}' not found in the list.")
            return

        # Unlink the node from the linked list
        if prev_node:
            prev_node.next = current_node.next
        current_node = None

    def __str__(self):
        """
        Returns a string representation of the linked list.
        """
        nodes = []
        current_node = self.head
        while current_node:
            nodes.append(str(current_node.data))
            current_node = current_node.next
        return " -> ".join(nodes) + " -> None"

if __name__ == "__main__":
    # Create a new linked list
    ll = LinkedList()
    print(f"Initial empty list: {ll}")

    # Append some elements
    ll.append("A")
    ll.append("B")
    ll.append("C")
    print(f"After appending A, B, C: {ll}")

    # Prepend an element
    ll.prepend("Start")
    print(f"After prepending 'Start': {ll}")

    # Delete an element from the middle
    ll.delete("B")
    print(f"After deleting 'B': {ll}")

    # Delete the head element
    ll.delete("Start")
    print(f"After deleting 'Start': {ll}")

    # Delete the tail element
    ll.delete("C")
    print(f"After deleting 'C': {ll}")

    # Try to delete an element that doesn't exist
    ll.delete("Z")
    print(f"After trying to delete 'Z': {ll}")