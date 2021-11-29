import numpy as np
from fractions import Fraction

def disp(A, top_list=None, left_list=None, latex_print=False):
	TAB_LEN = 6
	m,n = np.shape(A)
	dash = '-'*(2*(n+1)*TAB_LEN + 1)
	print(dash)
	top_print = dash
	left_print = []
	if top_list!=None:
		top_print = '|\t\t|'
		for i in top_list:
			top_print = top_print + '\t' + 'x' + str(i) + '\t|'
		top_print = top_print + '\t1\t|'
		top_print = top_print + '\n' + dash
	if left_list!=None:
		for i in left_list:
			left_print.append('x'+str(i))
		left_print.append('z')
		if len(left_list) < m-1:
			left_print.append('z0')
	else:
		for i in range(0,m):
			left_print.append('')
	print(top_print.expandtabs(TAB_LEN))
	for i in range(0,m):
		s = '|\t' + left_print[i] + '\t|'
		for j in range(0,n):
			s = s + '\t' + str(Fraction(A[i,j]).limit_denominator(100)) + '\t|'
		print(s.expandtabs(TAB_LEN))
		print(dash)
	if latex_print:
		latex(A, top_list, left_list)
	print("")

def latex(A, top_list=None, left_list=None):
	print('\\begin{center}')
	temp = '\\begin{tabular}{c|'
	temp = temp + 'c'*len(top_list)
	temp = temp + '|c}'
	print(temp)

	m,n = np.shape(A)
	top_print = '&'
	for i in top_list:
		top_print = top_print + '$x_' + str(i) + '$&'
	top_print = top_print + '1\\\\'
	print(top_print)
	print('\hline')

	left_print = []
	for i in left_list:
		left_print.append('$x_'+str(i)+'$')
	left_print.append('$z$')
	if len(left_list) < m-1:
		left_print.append('$z_0$')
	for i in range(0,m):
		s = left_print[i]
		if s == '$z$':
			print('\hline')
		for j in range(0,n):
			s = s + '&' + str(Fraction(A[i,j]).limit_denominator(100))
		s = s + '\\\\'
		print(s)

	print('\\end{tabular}')
	print('\\end{center}')

def ac(A,c,i):
	m,n = np.shape(A)
	if len(c)!=m:
		print("Wrong dimensions")
		return A
	if i==0:
		return np.c_[c,A]
	elif i==n:
		return np.c_[A,c]
	else:
		left = A[:,0:i]
		middle = c
		right = A[:,i:]
		return np.c_[np.c_[left,middle],right]

def ar(A,r,i):
	m,n = np.shape(A)
	if len(r)!=n:
		print("Wrong dimensions")
		return A
	if i==0:
		return np.vstack((r,A))
	elif i==m:
		return np.vstack((A,r))
	else:
		top = A[0:i,:]
		middle = r
		bottom = A[i:,:]
		return np.vstack((np.vstack((top,middle)),bottom))

def ex(A, s, r):
	m,n = np.shape(A)
	B = np.zeros((m,n))
	if (r > m-2) | (s > n-2):
		print("Error: Invalid indices")
	elif A[r,s] == 0:
		print("Error: Element at intersection 0")
	else:
		B[r,s] = 1/A[r,s]
		for j in range(0,n):
			if j == s:
				continue
			B[r,j] = -A[r,j]/A[r,s]
		for i in range(0,m):
			if i == r:
				continue
			else:
				for j in range(0,n):
					if j == s:
						B[i,j] = A[i,j]/A[r,s]
					else:
						B[i,j] = A[i,j] - A[i,s]*A[r,j]/A[r,s]
	return B

def run(A,I=None,lyx=False):

	m,n = np.shape(A)
	success = 1

	top_list = list(range(1,n))
	left_list = list(range(n,n+m-1))
	print("Given Array:")
	disp(A,top_list,left_list,lyx)

	if np.any(A[:-1,-1]<0):
		#PHASE1
		x_0 = np.zeros(m)
		x_0[A[:,-1]<0] = 1
		A = ac(A,x_0,n-1)

		z_0 = np.zeros(n+1)
		z_0[-2] = 1
		A = ar(A,z_0,m)

		top_list.append(0)
		print("Phase 1 Array:")
		disp(A,top_list,left_list,lyx)

		#TRACKING FOR x_0
		roc = 0 # 0 if currently col, 1 if currently row
		pos = n-1

		#SPECIAL EXCHANGE
		s = n-1
		r = np.where(A[:-1,-1]<0)[0][0]
		temp_s = top_list[s]
		temp_r = left_list[r]
		top_list[s] = temp_r
		left_list[r] = temp_s
		A = ex(A,s,r)
		print("Phase1: Special Jordan Exchange between x"+str(temp_s)+" and x"+str(temp_r)+"\n")
		disp(A,top_list,left_list,lyx)
		roc = roc^1
		pos = r

		while 1:
			if np.all(A[-1,:-1]>0):
				#DONE
				print("Phase1: Optimum reached")
				break
			if np.all(A[-1,:-1]>=0):
				#DONE BUT NOT UNIQUE
				print("Phase1: Optimum reached, but not unique")
				break

			s = np.where(A[-1,:-1]<0)[0][0]
			#BLANDS RULE
			for v in np.where(A[-1,:-1]<0)[0]:
				s = v if top_list[v]<top_list[s] else s

			h_i  = A[:-2,-1].copy()
			H_is = A[:-2,s].copy()

			if np.all(H_is>=0):
				#UNBOUNDED
				print("Phase1: Unbounded")
				break

			H_is[H_is==0] = 1 # avoid divide by zero
			h_i = np.where(H_is < 0, h_i, -np.inf)
			temp = -h_i/H_is
			temp_min = temp.min()
			r = np.argmin(temp)
			#BLANDS RULE
			for i,v in enumerate(temp):
				if v == temp_min:
					r = i if left_list[i]<left_list[r] else r

			temp_s = top_list[s]
			temp_r = left_list[r]
			top_list[s] = temp_r
			left_list[r] = temp_s

			A = ex(A,s,r)
			print("Phase1: Jordan Exchange between x"+str(temp_s)+" and x"+str(temp_r)+"\n")
			disp(A,top_list,left_list,lyx)

			if (roc) & (r==pos):
				pos = s
				roc = roc^1
			elif (roc^1) & (s==pos):
				pos = r
				roc = roc^1

		if A[-1,-1]!=0:
			#INFEASIBLE
			print("Given LP is infeasible")
			success = 0
		else:
			A = np.delete(A,(pos),axis=roc^1)
			A = A[:-1,:]
			if roc:
				left_list.remove(0)
			else:
				top_list.remove(0)
			print("Phase 1 Completed:")
			disp(A,top_list,left_list,lyx)
	
	if success:
		#START ACTIVE SET
		if I != None:
			print("Phase 1.5: Converting to Active Set\n")
			#FIND IDX IN LEFT_LIST
			swap_list = []
			for i,v in enumerate(left_list):
				if v in I:
					swap_list.append(i)
			while swap_list != []:
				for i,v in enumerate(top_list):
					if v not in I:
						if A[swap_list[-1],i] != 0:
							s = i
							r = swap_list.pop()
							temp_s = top_list[s]
							temp_r = left_list[r]
							top_list[s] = temp_r
							left_list[r] = temp_s
							A = ex(A,s,r)
			print("Active Set Tableau:")
			disp(A,top_list,left_list,lyx)

		while 1:
			#PHASE2
			if np.all(A[-1,:-1]>0):
				#DONE
				print("Phase2: Optimum reached")
				break
			if np.all(A[-1,:-1]>=0):
				#DONE BUT NOT UNIQUE
				print("Phase2: Optimum reached, but not unique")
				break

			s = np.where(A[-1,:-1]<0)[0][0]
			#BLANDS RULE
			for v in np.where(A[-1,:-1]<0)[0]:
				s = v if top_list[v]<top_list[s] else s

			h_i  = A[:-1,-1].copy()
			H_is = A[:-1,s].copy()

			if np.all(H_is>=0):
				#UNBOUNDED
				print("Phase2: Unbounded")
				break

			H_is[H_is==0] = 1 # avoid divide by zero
			h_i = np.where(H_is < 0, h_i, -np.inf)
			temp = -h_i/H_is
			temp_min = temp.min()
			r = np.argmin(temp)
			#BLANDS RULE
			for i,v in enumerate(temp):
				if v == temp_min:
					r = i if left_list[i]<left_list[r] else r

			temp_s = top_list[s]
			temp_r = left_list[r]
			top_list[s] = temp_r
			left_list[r] = temp_s

			A = ex(A,s,r)
			print("Phase2: Jordan Exchange between x"+str(temp_s)+" and x"+str(temp_r)+"\n")
			disp(A,top_list,left_list,lyx)
	
	return A,top_list,left_list
			
P2A=np.array([[-1,1,4],[-1,-1,6],[1,-1,0]])
P2C=np.array([[-1,1,4],[-1,-1,6],[-1,1,0]])
P2D=np.array([[2,-1,2],[-1,1,1],[-1,-1,0]])
P3=np.array([[-1,0,0,0.5],[0,-1,0,0.5],[0,0,-1,0.5],[1,1,1,-1],[-1,-1,-1,1],[1,-1,0,0]])
P4A=np.array([[-1,-1,1],[-2,1,-2],[-3,4,0]])
P4B=np.array([[2,-1,-1],[1,2,-2],[-2,1,0]])
P5=np.array([[-1,0,0,2],[0,-1,0,2],[0,0,-1,2],[-1,-1,-1,4],[1,1,-1,0]])