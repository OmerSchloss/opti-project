# Branch-and-Bound and Cutting plane algorithms for the TSP

**Author** : Omer Schloss, Sapir Vered.

**Language** : `Python 3.7`

**Dependencies** : `numpy`, `networkx`, `pulp`, `tsplib95`


---

## Usage

Clone the repository :
```
git clone 
```
### Option 1 :
Go into the folder :
```
cd TSP-BnB-CP
```
Run one of the following commands depending on the wanted solving method :
```
python cuttingplanes.py <dataset> <maxtime> 
python branchandbound.py <dataset> <maxtime> 
```
where `<maxtime>` is expressed in seconds.

### Option 2 :
Download the files and run `main.py`.

## Datasets

TSP datasets can be found in the [TSPLIB](http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/) website.
