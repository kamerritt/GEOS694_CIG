import sys,math,random,os
DATA=[5,3,9,1,4,8,2,7,6]

def calcStuff(nums,DoSort=False,scale =1,total=0,out=[]):
 for i in range(len(nums)):
  n=nums[i]*scale
  total+=n;out.append(n)
 if DoSort==True: out.sort()
 avg= total/len(nums)
 return out,avg

def findExtremes(values):
 minV=9999999;maxV=-9999999
 for v in values:
  if(v<minV):minV=v
  if(v>maxV):maxV=v
 return minV,maxV

def normalize(values , targetMax = 1):
 m,M=findExtremes(values)
 rng=M-m
 norm=[]
 for i in range(0,len(values)):
  if rng==0:
   norm.append(0)
  else:
   norm.append((values[i]-m)/rng*targetMax)
 return norm

def weirdHelper(a,b,store=[]):
 if a<b:
  for i in range(a):store.append(i*b)
  return store
 else:
  return [math.sqrt(a),math.sqrt(b)]

def generateRandomList(n ,maxVal=10):
 out=[]
 for i in range(n): out.append(random.random()*maxVal)
 return out

def filterAboveThreshold(vals,thresh=5):
 out=[]
 for v in vals:
  if v>thresh: out.append(v)
 return out

def computeVariance(vals):
 avg=sum(vals)/len(vals)
 total=0
 for v in vals:
  total+=(v-avg)*(v-avg)
 return total/len(vals)

def printReport(vals,avg,minv,maxv):
 print("Report")
 print("------")
 print("Values:",vals)
 print("Average:",avg)
 print("Min:",minv,"Max:",maxv)

def stringMaker(n):
 s=""
 for i in range(n):
  s+=str(i)+","
 return s

def takeEveryOther(vals):
 out=[]
 for i in range(len(vals)):
  if i%2==0: out.append(vals[i])
 return out

def computeMedian(vals):
 s=sorted(vals)
 mid=len(s)//2
 if len(s)%2==0:
  return (s[mid-1]+s[mid])/2
 else:
  return s[mid]

def sumOfSquares(vals):
 total=0
 for v in vals: total+=v*v
 return total

def clipValues(vals,lo,hi):
 out=[]
 for v in vals:
  if v<lo: out.append(lo)
  elif v>hi: out.append(hi)
  else: out.append(v)
 return out

def checkEnv():
 if "HOME" in os.environ:
  print("Home exists")
 else:
  print("No home?")

def main():
 print("Starting program")
 scaled,avg=calcStuff(DATA,DoSort=True,scale=2)
 minv,maxv=findExtremes(scaled)
 norm=normalize(scaled, targetMax=10)
 extra=weirdHelper(3,5)
 printReport(norm,avg,minv,maxv)
 print("Extra data:",extra)

 rand=generateRandomList(10,20)
 filtered=filterAboveThreshold(rand,10)
 var=computeVariance(filtered)
 print("Variance:",var)

 s=stringMaker(12)
 print("String:",s)

 evens=takeEveryOther(range(10))
 print("Every other:",evens)

 print("Median:",computeMedian([5,1,9,3,7]))
 print("Sum squares:",sumOfSquares([1,2,3]))
 print("Clipped:",clipValues([1,5,10,15],3,12))

 checkEnv()

 if len(sys.argv)>1:
  print("CLI args found ->",sys.argv)

if __name__=="__main__":
 main()
