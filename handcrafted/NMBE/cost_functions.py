import scipy
import numpy as np
from scipy.spatial.distance import pdist,squareform,euclidean
from sklearn.preprocessing import scale

def mad(descriptor_params,descriptor_function):

	db = descriptor_function(descriptor_params=descriptor_params)

	name_arr = db.keys()
	#data = scipy.array([scipy.fromstring(db[nome],sep=' ') for nome in name_arr])
	data = scipy.array([db[nome] for nome in name_arr])

	cIDX = data[:,0].astype(int)
	cIDX=cIDX-min(cIDX)

	#X = scale(data[:,1:])
	X = data[:,1:]

	Nclasses = max(cIDX)+1

	nfigs_classe=np.zeros(int(Nclasses))
	for i in range(int(Nclasses)):
		nfigs_classe[i]=sum((cIDX==i).astype(int))

	N = X.shape[0]              # number of instances
	K = len(np.unique(cIDX))    # number of clusters

	# compute pairwise distance matrix
	D = squareform(pdist(X))

	# indices belonging to each cluster
	kIndices = [np.flatnonzero(cIDX==k) for k in range(K)]

	# compute a,b,s for each instance
	a = np.zeros(N)
	b = np.zeros(N)
	for i in range(N):
		# instances in same cluster other than instance itself
		a[i] = np.mean( [D[i][ind] for ind in kIndices[cIDX[i]] if ind!=i] )
		# instances in other clusters, one cluster at a time
		b[i] = np.min( [np.mean(D[i][ind])
						for k,ind in enumerate(kIndices) if cIDX[i]!=k] )
	s = (b-a)/np.maximum(a,b)

	return np.median(np.absolute(s-1))

def silhouette(descriptor_params,descriptor_function):

	db = descriptor_function(descriptor_params=descriptor_params)

	name_arr = db.keys()
	#data = scipy.array([scipy.fromstring(db[nome],sep=' ') for nome in name_arr])
	data = scipy.array([db[nome] for nome in name_arr])

	cIDX = data[:,0].astype(int)
	cIDX=cIDX-min(cIDX)

	#X = scale(data[:,1:])
	X = data[:,1:]

	Nclasses = max(cIDX)+1

	nfigs_classe=np.zeros(int(Nclasses))
	for i in range(int(Nclasses)):
		nfigs_classe[i]=sum((cIDX==i).astype(int))

	N = X.shape[0]              # number of instances
	K = len(np.unique(cIDX))    # number of clusters

	# compute pairwise distance matrix
	D = squareform(pdist(X))

	# indices belonging to each cluster
	kIndices = [np.flatnonzero(cIDX==k) for k in range(K)]

	# compute a,b,s for each instance
	a = np.zeros(N)
	b = np.zeros(N)
	for i in range(N):
		# instances in same cluster other than instance itself
		a[i] = np.mean( [D[i][ind] for ind in kIndices[cIDX[i]] if ind!=i] )
		# instances in other clusters, one cluster at a time
		b[i] = np.min( [np.mean(D[i][ind]) 
						for k,ind in enumerate(kIndices) if cIDX[i]!=k] )
	s = (b-a)/np.maximum(a,b)

	return -s.mean()

def db(descriptor_params,descriptor_function,distance = 'euclidean',q=1):

	db = descriptor_function(descriptor_params=descriptor_params)

	name_arr = db.keys()
	#data = scipy.array([scipy.fromstring(db[nome],sep=' ') for nome in name_arr])
	data = scipy.array([db[nome] for nome in name_arr])

	cIDX = data[:,0].astype(int)
	cIDX=cIDX-min(cIDX)

	X = data[:,1:]
 	#X = scale(data[:,1:])
	
	Nclusters = cIDX.max()+1
	# Clusters
	A = np.array([ X[np.where(cIDX == i)] for i in range(Nclusters)])
	# Centroids
	v = np.array([ np.sum(Ai,axis = 0)/float(Ai.shape[0])  for Ai in A])
     
	s = []
	for Ai,vi in zip(A,v):
         s.append((np.array([euclidean(x,vi)**float(q)  for x in Ai]).sum()/float(Ai.shape[0]))**(1/float(q))) 
     
	d = squareform(pdist(v,distance))
     
	R = []
	for i in range(Nclusters):
         R.append(np.array([(s[i] + s[j])/d[i,j] for j in range(Nclusters) if j != i]).max())
   
	return np.array(R).sum()/float(Nclusters)
 
def ch(descriptor_params,descriptor_function,dist='euclidean'):
 db = descriptor_function(descriptor_params=descriptor_params)

 name_arr = db.keys()
 #data = scipy.array([scipy.fromstring(db[nome],sep=' ') for nome in name_arr])
 data = scipy.array([db[nome] for nome in name_arr])

 cIDX = data[:,0].astype(int)
 cIDX=cIDX-min(cIDX)
 
 X = data[:,1:]
 #X = scale(data[:,1:])
 
 Nclusters = cIDX.max()+1
 Npoints=len(X)

 n = np.ndarray(shape = (Nclusters),dtype = float)

 j=0
 for i in range(cIDX.min(),cIDX.max()+1):
  aux=np.asarray([float(b) for b in (cIDX==i)])  
  n[j]=aux.sum()
  j=j+1


# Clusters
 A = np.array([ X[np.where(cIDX == i)] for i in range(Nclusters)])
# Centroids
 v = np.array([ np.sum(Ai,axis = 0)/float(Ai.shape[0])  for Ai in A])

 ssb=0

 for i in range(Nclusters):
  ssb=n[i]*(euclidean(v[i],np.mean(X,axis=0))**2)+ssb

 z = np.ndarray(shape = (Nclusters),dtype = float)

 for i in range(cIDX.min(),cIDX.max()+1):
  aux=np.array([(euclidean(x,v[i])**2) for x in X[cIDX==i]])
  z[i]=aux.sum()
   
 ssw=z.sum()

 return(-(ssb/(Nclusters-1))/(ssw/(Npoints-Nclusters)))