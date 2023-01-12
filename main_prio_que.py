import copy
from graphviz import Digraph

class Node(object): # 定义类用大写字母开头,继承object类
    """单链表的结点"""
    def __init__(self, key = None,next = None):
        # key存放数据元素
        self.key = key
        # next是下一个节点的标识
        self.next = next


class treeNode:
    """树节点"""
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinaryTree:

    def __init__(self, data=None):
        self.head = None   #链表开始节点
        self.root = None   #二叉树的根节点
        self.size = 0

    def push(self, new_data):    #加入链表

        new_node = Node(new_data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def convertList2Binary(self):   #基于链表构造二叉树

        q = []
        head = copy.copy(self.head)
        if head is None:
            self.root = None
            return

        self.root = treeNode(head.key)
        q.append(self.root)

        head = head.next

        while head:

            parent = q.pop(0)
            rightChild = None
            leftChild = treeNode(head.key)
            q.append(leftChild)
            head = head.next
            if head:
                rightChild = treeNode(head.key)
                q.append(rightChild)
                head = head.next
            parent.left = leftChild
            parent.right = rightChild

    def BFS_print(self):      #层序遍历
        if self.root == None:
            return None
        t_root = self.root
        queue = []
        queue.append(t_root)
        while queue:
            now_node = queue.pop(0)
            print(now_node.data,end=' ')
            if now_node.left != None:
                queue.append(now_node.left)
            if now_node.right != None:
                queue.append(now_node.right)
        print()
        return None

    def BFS(self,i):     #层序遍历获取第i个节点
        if self.root == None:
            return None
        t_root = self.root
        queue = []
        queue.append(t_root)
        while queue:
            now_node = queue.pop(0)
            if i == 0:
                return now_node
            i -= 1
            if now_node.left != None:
                queue.append(now_node.left)
            if now_node.right != None:
                queue.append(now_node.right)
        return None

    def get_cur_node(self,i):
        return self.BFS(i)

    def get_parent(self,i):    #parent Node index is (i-1)//2
        i = (i-1)//2
        return self.BFS(i)

    def get_left_child(self,i):  #left child Node index is 2*i+1
        i = 2*i + 1
        return self.BFS(i)

    def get_right_child(self,i):  #left child Node index is 2*i+2
        i = 2*i + 2
        return self.BFS(i)


# 「最小堆」的实现
class BinHeap:
    def __init__(self,binary_tree:BinaryTree):
        self.heapList = binary_tree
        self.binary_tree = binary_tree
        self.currentSize = binary_tree.size

    def percUp(self, i):     #向上调整
        while (i-1) // 2 >= 0:
            curNode = self.binary_tree.get_cur_node(i)    #获取当前节点
            parentNode = self.binary_tree.get_parent(i)   #获取父亲节点
            if curNode.data < parentNode.data:   #当前节点的值小于父亲节点，则交换两个节点的值
                tmp = parentNode.data
                parentNode.data = curNode.data
                curNode.data = tmp
            i = (i-1) // 2   #继续调整上一层

    def insert(self, key):
        new_node = treeNode(key)     #构造新节点
        self.currentSize += 1        #更新节点个数
        self.binary_tree.size += 1
        parent_new_node = self.binary_tree.get_parent(self.currentSize-1)#将新节点插入树的最后，获取新节点的父节点
        #将新节点插入树中
        if parent_new_node.left == None:
            parent_new_node.left = new_node
        else:
            parent_new_node.right = new_node

        self.percUp(self.currentSize-1)    #从当前节点向上进行调整

    def percDown(self, i):     #向下调整
        while (i * 2 + 1) <= self.currentSize-1:
            mc = self.minChild(i)   #获取孩子节点中的值较小的那一个
            iNode = self.binary_tree.get_cur_node(i)
            mcNode = self.binary_tree.get_cur_node(mc)
            if iNode.data > mcNode.data:   #当前节点的值小于孩子节点，则交换两个节点的值
                tmp = iNode.data
                iNode.data = mcNode.data
                mcNode.data = tmp
            i = mc   #继续调整下一层

    #获取孩子节点中值较小的那一个
    def minChild(self, i):
        if i * 2 + 2 >= self.currentSize:
            return i * 2 + 1
        else:
            if self.binary_tree.get_left_child(i).data < self.binary_tree.get_right_child(i).data:
                return i * 2 + 1
            else:
                return i * 2 + 2

    def delMin(self):
        retval = copy.copy(self.binary_tree.root)   #返回根节点
        root = self.binary_tree.root
        last_node = self.binary_tree.get_cur_node(self.currentSize-1)   #最后一个节点
        #交换最后一个节点和根节点的值
        tmp = root.data
        root.data = last_node.data
        last_node.data = tmp

        # 去掉最后一个节点
        parent_last_node = self.binary_tree.get_parent(self.currentSize - 1)
        if (self.currentSize - 1) % 2 == 0:
            parent_last_node.right = None
        else:
            parent_last_node.left = None
        #更新节点个数
        self.currentSize-=1
        self.binary_tree.size -= 1
        self.percDown(0)   #从根节点向下调整
        return retval


    def buildHeap(self):
        i = self.currentSize // 2
        while i>=0:
            self.percDown(i)
            i -= 1

class PriorityQueue:
    def __init__(self,min_heap:BinHeap):
        self.min_heap = min_heap

    def pop(self):
        if self.empty():
            raise '队列为空!'
        return self.min_heap.delMin().data

    def put(self,key):
        self.min_heap.insert(key)

    def get(self):
        return self.min_heap.binary_tree.root.data

    def empty(self):
        if self.min_heap.currentSize == 0:
            return True
        return False


#获取每一层的值，用于打印，.表示空白
def treeArray(root):
    pRoot = root
    if not pRoot:
        return []
    resultList = []
    curLayer = [pRoot]
    while curLayer:
        curList = []
        nextLayer = []
        for node in curLayer:
            if node == '.':
                curList.append('.')
            else:
                curList.append(node.data)
                if node.left:
                    nextLayer.append(node.left)
                else:
                    nextLayer.append('.')
                if node.right:
                    nextLayer.append(node.right)
                else:
                    nextLayer.append('.')
        resultList.append(curList)
        curLayer = nextLayer
    return resultList

#可视化二叉树节点 深度为3
def visual_result(root):
    t = treeArray(root)

    n = len(t) - 1
    for i in range(1, n - 1):
        for j in range(2 * i):
            if t[i][j] == '.':
                t[i + 1].insert(j + 1, '.')
                t[i + 1].insert(j + 1, '.')
    result = []
    result.append('    {}   '.format(t[0][0]))
    result.append('   /  \\  ')
    result.append('  {}   {} '.format(t[1][0], t[1][1]))
    result.append(' / \\  / \\')
    result.append('{} {} {} {}'.format(*t[2]))
    for i in result[:2 * n - 1]:
        print(i)


#使用graphviz可视化二叉树
def visual_graph(root,savepath):

    dot = Digraph(comment='堆',format='png')

    if root == None:
        return None
    t_root = root
    queue = []
    queue.append(t_root)
    index = 0
    while queue:
        now_node = queue.pop(0)
        dot.node(f'{index}', f'{now_node.data}')  #构造节点
        index += 1
        if now_node.left != None:
            queue.append(now_node.left)
        if now_node.right != None:
            queue.append(now_node.right)
    edges = []
    #构造边
    for i in range(index):
        if 2*i+1 < index:
            edges.append(f'{i}{2*i+1}')
        if 2*i+2< index:
            edges.append(f'{i}{2 * i + 2}')


    dot.edges(edges)
    # dot.render('round-table.gv',view=True)
    dot.render(savepath, view=True)   #保存为图片


#测试数据
def test1():
    bt = BinaryTree()
    nums = [12, 32, 15, 13, 24, 27, 30]
    nums.reverse()
    for num in nums:   #构建链表
        bt.push(num)
    linked_list = bt.head   #获取构建的链表
    #打印链表
    print('构建的单向链表为:')
    print(linked_list.key,end='')
    linked_list = linked_list.next
    while linked_list:
        print(f' -> {linked_list.key}',end='')
        linked_list = linked_list.next
    print()
    bt.convertList2Binary()    #转换为二叉树
    #打印出二叉树
    visual_result(bt.root)

    #获取15的父节点和子节点
    print(f'节点值为15的父节点的值为：{bt.get_parent(2).data}')
    print(f'节点值为15的左孩子节点的值为：{bt.get_left_child(2).data}')
    print(f'节点值为15的右孩子节点的值为：{bt.get_right_child(2).data}')

    print('********************构建优先队列*******************')
    bh = BinHeap(bt)
    bh.buildHeap()
    p = PriorityQueue(bh)
    print('当前最小堆为:')
    visual_result(p.min_heap.binary_tree.root)

    # graphviz可视化
    visual_graph(bh.binary_tree.root, '最小堆图片.gv')

    print(f'出队：最小值为{p.pop()}')
    print('当前最小堆为:')
    visual_result(p.min_heap.binary_tree.root)

    print(f'入队：将3入队')
    p.put(3)
    print('当前最小堆为:')
    visual_result(p.min_heap.binary_tree.root)




if __name__ == '__main__':
    test1()






