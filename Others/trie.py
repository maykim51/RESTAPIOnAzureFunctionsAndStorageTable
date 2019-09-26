class TrieNode: 
	def __init__(self): 
		self.children = [None]*26 ##!!! array size == alphabet size
		self.isEndOfWord = False

class Trie:
    def __init__(self):
        self.root = self.getNode()
        
    def getNode(self):
        return TrieNode()
    
    def _charToIndex(self, ch):
        return ord(ch) - ord('a')
    
    def insert(self, key):
        curr = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if not curr.children[index]:
                curr.children[index] = self.getNode()                
            curr = curr.children[index]   
        
        curr.isEndOfWord = True
    
    def search(self, key):
        curr = self.root #FYI root of trie is always null
        for level in range(len(key)):
            index = self._charToIndex(key[level])
            if not curr.children[index]:
                return False
            curr = curr.children[index]
        
        if curr != None and curr.isEndOfWord:
            return True
        return False


# driver function 
def main(): 

	# Input keys (use only 'a' through 'z' and lower case) 
	keys = ["the","a","there","anaswe","any", 
			"by","their"] 
	output = ["Not present in trie", 
			"Present in trie"] 

	# Trie object 
	t = Trie() 

	# Construct trie 
	for key in keys: 
		t.insert(key) 

	# Search for different keys 
	print("{} ---- {}".format("the",output[t.search("the")])) 
	print("{} ---- {}".format("these",output[t.search("these")])) 
	print("{} ---- {}".format("their",output[t.search("their")])) 
	print("{} ---- {}".format("thaw",output[t.search("thaw")])) 

if __name__ == '__main__': 
	main() 

