'''
https://www.geeksforgeeks.org/trie-insert-and-search/
+ https://blog.ilkyu.kr/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%97%90%EC%84%9C-Trie-%ED%8A%B8%EB%9D%BC%EC%9D%B4-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0
'''

# Python program for insert and search 
# operation in a Trie 

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

# class Trie: 	
# 	def __init__(self): 
# 		self.root = self.getNode() 

# 	def getNode(self): 
# 		return TrieNode() #root is always ''.

#         ##!!
# 	def _charToIndex(self,ch):  ##_ means private #this index is used in the array		
# 		# private helper function 
# 		# Converts key current character into index 
# 		# use only 'a' through 'z' and lower case 		
# 		return ord(ch)-ord('a') 

# 	def insert(self,key): 		
# 		# If not present, inserts key into trie 
# 		# If the key is prefix of trie node, 
# 		# just marks leaf node 
# 		pCrawl = self.root 
# 		length = len(key) 
# 		for level in range(length): 
# 			index = self._charToIndex(key[level]) 

# 			# if current character is not present 
# 			if not pCrawl.children[index]: 
# 				pCrawl.children[index] = self.getNode() 
# 			pCrawl = pCrawl.children[index] 

# 		# mark last node as leaf 
# 		pCrawl.isEndOfWord = True

# 	def search(self, key): 
		
# 		# Search key in the trie 
# 		# Returns true if key presents 
# 		# in trie, else false 
# 		pCrawl = self.root 
# 		length = len(key) 
# 		for level in range(length): 
# 			index = self._charToIndex(key[level]) 
# 			if not pCrawl.children[index]: 
# 				return False
# 			pCrawl = pCrawl.children[index] 

# 		return pCrawl != None and pCrawl.isEndOfWord 

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

# This code is contributed by Atul Kumar (www.facebook.com/atul.kr.007) 
