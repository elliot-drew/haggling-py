# Haggling module

Python module to allow haggling between two users.

In depth documentation from docstrings can be seen in `index.html`.

Requires Python3.

## Usage

Start by creating an instance of Haggler class. You must supply the names/ids of the two Users involved in the transaction as strings
to Haggler.

```
seller = "Batman"
buyer = "Superman"

haggler = Haggler(seller, buyer)
```

Note that until you have used the `submit` method of Haggler the seller and buyer roles have not actually been defined - the variable names above are just to make this example clearer.

Next, create the initial Offer. Below an Offer is created for a Batmobile with price 500 and quantity 5.

```
init_offer = Offer("Batmobile", 500, 5)
```

To start the haggling, use the submit method of Haggler to define who the buyer and seller is, and pass in the initial offer.

```
haggler.submit(buyer, seller, init_offer)
``` 

All actions are implemented as methods of the Haggler class. See `index.html` for more info.


You can print the history for a user as follows:

```
haggler.printHistory(user_id)
```

You can print a specific offer version from the history of a user as follows, or return the Offer instance for that specific version:

```
haggler.printVersion(user_id, version)
version_offer = haggler.returnVersion(user_id, version)
```

You can get a dict showing the differences between two offer versions for a user:

```
# differences for user_id from version 1 to version 3
diffs = haggler.versionDifferences(user_id, 1, 3)
```

`tests.py` contains a number of tests corresponding to the difference examples in the problem statement, and can be run using 

```
python tests.py -v 
```
