# Simplex for 236A

Python script to solve LP using simplex by Jordan exchanges taught in 236A.

You will need python installed along with the 'numpy' and 'fractions' libraries for this. Most probably you'll already having both of these installed by default.

## How to run?

**Step 0:** Run the script in 'interactive mode' using the below command:
```
python -i jordan.py
```

**Step 1:** Define your initial tableau (doesn't need to be feasible, doesn't need to be at the desired start point). It's as simple as writing the LP in the form:
<p align="center">
  <img src="https://i.ibb.co/HTtp10f/Code-Cogs-Eqn-1.png" />
</p>
<p align="center">
  <img src="https://i.ibb.co/VmsLZ5X/Code-Cogs-Eqn.png" />
</p>

And the convert this into a numpy 2D array. For example, if the given LP is:
<p align="center">
  <img src="https://i.ibb.co/kyF3g28/Screenshot-2021-11-29-at-2-42-43-PM.png" />
</p>

Then the tableau will look like this:
<p align="center">
  <img src="https://i.ibb.co/2s2N6cg/Screenshot-2021-11-29-at-2-42-48-PM.png" />
</p>

So in the shell, define the tableau like this:
```
P3=np.array([[-1,0,0,0.5],[0,-1,0,0.5],[0,0,-1,0.5],[1,1,1,-1],[-1,-1,-1,1],[1,-1,0,0]])
```

**Step 2:** Next, just run the below command to solve the LP:
```
ans,top,left=run(P3)
```

Here, the run function returns the final tableau in 'ans', and top/left can be used to display the final result if needed:
```
disp(ans,top,left)
```

## Additional Features

**Active Set:** If you need to start at a certain vertex (instead of all 0 vertex - irrespective of feasibility), then you can mention the subscripts of those variables (which are 0 in the desired vertex) in the argument `I` as shown:
```
ans,top,left=run(P3,[3,4,5])
```

This will start the tableau from all-0 point and forcibly reach the desired vertex (mentioned as 'Phase 1.5' in prints). And then it starts the actual algorithm from that point.

**Latex Format:** If you need to get all the tables in Latex format, just set the `lyx` flag to True as shown:
```
ans,top,left=run(P3,[3,4,5],lyx=True)
```
This will print the tableau in latex format which you can directly paste in your latex workbook. Example:

![example](https://i.ibb.co/55gMDvw/Screenshot-2021-11-29-at-2-56-31-PM.png)

The table in latex would look like this:

![latex](https://i.ibb.co/RY7fzj6/Screenshot-2021-11-29-at-3-10-00-PM.png)

## Miscellaneous

Note: The algo uses the Bland's pivoting rule everytime.

If you wanna perform Jordan exchange manually step by step yourself, just use the function `ex(A,s,r)` as shown below:
```
A = np.array([[-1,1,4],[-1,-1,6],[1,-1,0]]) # your tableau
s = 1 # index of the pivot column
r = 2 # index of the pivot row
A_new = ex(A,s,r)
```

## That's all Folks!

If this helped you, you're welcome! If you have any modifications or corrections in the code, feel free to initiate a pull-request. K bye!