'''inpu: aaabbca
   output: a4b2c1'''

def char_count(s):
   v=[]
   for i in range(0,len(s)):
      if(s[i] not in v):
         f=1
         for j in range(i+1,len(s)):
            if(s[i]==s[j]):
               f+=1
         print(s[i],f,sep="",end="")
         v.append(s[i])

s=input("Enter the string:")
char_count(s)