#!/usr/bin/env python

"""
Module implementing haggling between two users.

"""

import copy
import yaml

class Offer:

	"""
	Offer class
	
	When an action is taken, an Offer is created by both parties.
	
	Offer is added to each users history using addOfferHistory method of User
	
	Attributes:
	    action (string): the action that user_action took for this version
	    buyer (string): user id of the buyer
	    price (int): price of one unit of product
	    private_info (dict): private meta data
	    product (string): name of product
	    quantity (int): number of units of product
	    seller (string): user id of seller
	    state (string): state of user who owns this Offer instance
	    user_action (string): identity of user who took action
	    user_id (string): identity of user who owns this Offer instance
	    version (int): the iteration of this offer in the offer history
	"""

	def __init__(self, product, price, quantity):
		"""
		init for Offer class
		
		Args:
		    product (string): name of the product
		    price (int): price of one unit of the product
		    quantity (int): number of units of product being offered
		
		Deleted Parameters:
		    action (string): the action that user_action took for this version
		    user_action (string): the identity of the user who took action
		    buyer (string): user id of the buyer
		    seller (string): user id of the seller
		"""
		self.user_id = None # set when added to a Users offer_history
		self.version = None # set when added to a Users offer_history
		self.action = None # set on action
		self.user_action = None # set on action
		self.state = None  # set when added to a Users offer_history
		self.buyer = None # set on submit
		self.seller = None # set on submit
		self.product = product
		self.price = price
		self.quantity = quantity
		self.private_info = None  # set when added to a Users offer_history

	def pretty(self):
		"""Summary
		"""
		print(yaml.dump(vars(self)))

class User:

    """
    User Class
    
    Can be buyer or seller (role).
    
    Contains information on user_id, role, state, action/offer history.
    
    Attributes:
        curr_version (int): count to keep track of current version for offer history
        current_offer (Offer): the most recent Offer created 
        end (bool): whether offer has been accepted or cancelled
        offer_history (list): list of Offer instances
        other (string): the id of the other user in the transaction
        private_info (dict): private meta data
        role (string): is seller buyer or seller?
        state (string): state of this user
        user_id (string): id of this user
    """

    def __init__(self, user_id):
    	"""
    	Initialises User. Called by Haggler.__init__ method.
    	Other attributes defined when Haggler.submit is called.
    	
    	Args:
    	    user_id (string): id of this user
    	"""
    	self.user_id = user_id
    	self.role = None
    	self.state = None
    	self.offer_history = []
    	self.private_info = {}
    	self.curr_version = 1
    	self.end = False # set to true on Accept or Cancel
    	self.current_offer = None
    	self.other = None

    def addOfferHistory(self, offer):
    	"""
    	Adds User specific info to Offer instance then adds it to the 
    	offer history, updates the current offer and increments the current version.
    	
    	Args:
    	    offer (Offer): Offer instance being added to the history
    	"""
    	offer = copy.deepcopy(offer)
    	# set the state to this users state at time of version/action
    	offer.state = self.state
    	# update private info if user has it
    	offer.private_info = copy.deepcopy(self.private_info)
    	# set the user_id of Offer to this users id
    	offer.user_id = self.user_id
    	# set offer version to current version then increment curr_version
    	offer.version = self.curr_version
    	
    	self.offer_history.append(offer)
    	self.current_offer = offer
    	self.curr_version += 1

    def setRole(self, role):
    	"""
    	Set the role (buyer or seller) of this User
    	
    	Args:
    	    role (string): buyer or seller?
    	"""
    	self.role = role

    def updatePrivateInfo(self, private_info):
    	"""
    	Updates the private meta data of this user.
		Data only visible to this User.
		Preserves previous data unless explicitly replaced
    	
    	Args:
    	    private_info (dict): private meta data
    	"""
    	for k, v in private_info.items():

    		self.private_info[k] = v

    def setEnd(self):
    	"""
    	If offer accepted or cancelled, set end to True
    	"""
    	self.end = True

    def setState(self, state):
    	"""
    	update/set the state of this User
    	
    	Args:
    	    state (string): new state of User
    	"""
    	self.state = state

    def setOther(self, other):
    	"""
    	Set the user id of the other User in the transaction
    	
    	Args:
    	    other (string): id of partner User in transaction
    	"""
    	self.other = other


class Haggler:

	"""
	Haggler Class - This class stores the two Users in the transaction in a 
	self.users dict. Has all methods related to taking actions and retrieving/printing
	data.
	
	Attributes:
	    users (TYPE): Description
	"""
	
	def __init__(self, user_id_1, user_id_2):
		"""
		Initialise the Haggler. Two Users are created and attached to the Haggler
		instance.
		
		Args:
		    user_id_1 (string): id of first User to be created
		    user_id_2 (string): id of second User to be created
		
		Raises:
		    TypeError: If the user ids supplied are not str, exception is raised.
		"""
		# check ids are both strings

		str_chk1 = isinstance(user_id_1, str)
		str_chk2 = isinstance(user_id_2, str)

		if str_chk1 and str_chk2:

			# init each user

			user_1 = User(user_id_1)
			user_2 = User(user_id_2)

			self.users = {
				user_id_1: user_1,
				user_id_2: user_2,
			}
		else:
			try:
				raise TypeError("User IDs must be type string")
			except TypeError as error:
				print(error)
			return


	def submit(self, user_id, other_id, offer):
		"""
		Submits the first offer. This establishes who the seller and buyer are and their
		relationship to each other, what the first offer is etc.
		
		Args:
		    user_id (string): user id of user performing the action
		    other_id (string): user id of recipient of action
		    offer (Offer): Offer instance containing info on current offer
		
		Raises:
		    ValueError: if the user ids supplied are not present in the Haggler.users dict
		"""
		if user_id in self.users.keys() and other_id in self.users.keys():
			seller = self.users[user_id]
			buyer = self.users[other_id]

			# check if endpoint has been reached already
			if seller.end:
				try:
					raise ValueError("Offer has been {0} - no more actions possible.".format(u1.state))
				except ValueError as error:
					print(error)
				return

			# set up relationship for other actions
			seller.setOther(buyer)
			buyer.setOther(seller)

			# add info to offer

			offer.action = "Submit"
			offer.user_action = user_id
			offer.seller = user_id
			offer.buyer = other_id

			# update roles and states
			seller.setRole("seller")
			seller.setState("AwaitingTheirAcceptance")

			buyer.setRole("buyer")
			buyer.setState("AwaitingMyAcceptance")

			# add the offer to respective histories
			seller.addOfferHistory(offer)
			buyer.addOfferHistory(offer)
			return

		else:
			try:
				raise ValueError("Error: {0} or {1} is not a valid user in this Haggler.".format(user_id,  other_id))
			except ValueError as error:
				print(error)
			return

	def accept(self, user_id):
		"""
		Accepts the current offer. user_id must be in state "AwaitingMyAcceptance".
		Results in an end state.
		
		Args:
		    user_id (string): user id of user performing the action
		
		Raises:
		    ValueError: if the user id supplied is not present in the Haggler.users dict
		"""
		if user_id in self.users.keys():
			u1 = self.users[user_id]
			u2 = u1.other

			# check if endpoint has been reached already
			if u1.end:
				try:
					raise ValueError("Offer has been {0} - no more actions possible.".format(u1.state))
				except ValueError as error:
					print(error)
				return

			# check state of u1

			if u1.state == "AwaitingMyAcceptance":

				offer = copy.deepcopy(u1.current_offer)
				offer.action = "Accept"
				offer.user_action = user_id

				# update states
				u1.setState("Accepted")
				u2.setState("Accepted")

				u1.setEnd()
				u2.setEnd()

				# add the offer to respective histories
				u1.addOfferHistory(offer)
				u2.addOfferHistory(offer)
				return
			else:
				try:
					raise ValueError("Error: State {0} invalid for Accept by {1}.".format(u1.state, user_id))
				except ValueError as error:
					print(error)
				return

		else:
			try:
				raise ValueError("Error: {0} is not a valid user in this Haggler.".format(user_id))
			except ValueError as error:
				print(error)
			return

	def cancel(self, user_id):
		"""
		Cancels the current offer. user_id can be in any state that isn't an end state.
		Results in an end state.
		
		Args:
		    user_id (string): user id of user performing the action
		
		Raises:
		    ValueError: if the user id supplied is not present in the Haggler.users dict
		"""
		if user_id in self.users.keys():
			u1 = self.users[user_id]
			u2 = u1.other

			# check if endpoint has been reached already
			if u1.end:
				try:
					raise ValueError("Offer has been {0} - no more actions possible.".format(u1.state))
				except ValueError as error:
					print(error)
				return

			offer = copy.deepcopy(u1.current_offer)
			offer.action = "Cancel"
			offer.user_action = user_id

			# update states
			u1.setState("Cancelled")
			u2.setState("Cancelled")

			u1.setEnd()
			u2.setEnd()

			# add the offer to respective histories
			u1.addOfferHistory(offer)
			u2.addOfferHistory(offer)
			return

		else:
			try:
				raise ValueError("Error: {0} is not a valid user in this Haggler.".format(user_id))
			except ValueError as error:
				print(error)
			return

	def withdraw(self, user_id):
		"""
		Withdraws the current offer. user_id must be in "AwaitingTheirAcceptance" state.
		
		Args:
		    user_id (string): user id of user performing the action
		
		Raises:
		    ValueError: if the user id supplied is not present in the Haggler.users dict
		"""
		if user_id in self.users.keys():
			u1 = self.users[user_id]
			u2 = u1.other

			# check if endpoint has been reached already
			if u1.end:
				try:
					raise ValueError("Offer has been {0} - no more actions possible.".format(u1.state))
				except ValueError as error:
					print(error)
				return

			# check if u1 state
			if u1.state == "AwaitingTheirAcceptance":
				
				offer = copy.deepcopy(u1.current_offer)
				offer.action = "Withdraw"
				offer.user_action = user_id

				# update states
				u1.setState("WithdrawnByMe")
				u2.setState("WithdrawnByThem")

				# add the offer to respective histories
				u1.addOfferHistory(offer)
				u2.addOfferHistory(offer)
				return
			else:
				try:
					raise ValueError("Error: State {0} invalid for Withdraw by {1}.".format(u1.state, user_id))
				except ValueError as error:
					print(error)
				return
		else:
			try:
				raise ValueError("Error: {0} is not a valid user in this Haggler.".format(user_id))
			except ValueError as error:
				print(error)
			return

	def proposeUpdate(self, user_id, offer):
		"""
		Proposes an update to the offer. user_id must be in "WithdrawnByMe" or "AwaitingMyAcceptance"
		state.
		
		Args:
		    user_id (string): user id of user performing the action
		    offer (Offer): new Offer instance containing info on updated offer
		
		Raises:
		    ValueError: if the user ids supplied are not present in the Haggler.users dict
		"""
		if user_id in self.users.keys():
			u1 = self.users[user_id]
			u2 = u1.other

			# check if endpoint has been reached already
			if u1.end:
				try:
					raise ValueError("Offer has been {0} - no more actions possible.".format(u1.state))
				except ValueError as error:
					print(error)
				return

			# check if u1 state
			if u1.state in ["WithdrawnByMe", "AwaitingMyAcceptance"]:
				# update states
				u1.setState("AwaitingTheirAcceptance")
				u2.setState("AwaitingMyAcceptance")

				# add the offer to respective histories
				#offer = copy.deepcopy(offer)
				offer.action = "ProposeUpdate"
				offer.user_action = user_id
				offer.seller = u1.current_offer.seller
				offer.buyer = u1.current_offer.buyer
				u1.addOfferHistory(offer)
				u2.addOfferHistory(offer)
				return
			else:
				try:
					raise ValueError("Error: State {0} invalid for ProposeUpdate by {1}.".format(u1.state, user_id))
				except ValueError as error:
					print(error)
				return
		else:
			try:
				raise ValueError("Error: {0} is not a valid user in this Haggler.".format(user_id))
			except ValueError as error:
				print(error)
			return


	def updatePrivateData(self, user_id, private_info):
		"""
		Updates private data of user_id. Can be in any state including end state. Update is only visible in
		history of User with user_id. Preserves current private info unless explicitly overridden with key->val pair.
		
		Args:
		    user_id (string): user id of user performing the action
		    private_info (dict): private_info meta data
		
		Raises:
		    ValueError: if the user ids supplied are not present in the Haggler.users dict
		    AttributeError/TypeError: if private_info not a dict
		"""
		if user_id in self.users.keys():
			# want to check if private_info is actually a dict
			try:
				private_info.keys()
			except(AttributeError, TypeError) as error:
				print(error)
			else:

				# private data update one sided - no need for u2/other
				u1 = self.users[user_id]

				# dont care about endpoint or current state

				offer = copy.deepcopy(u1.current_offer)
				offer.action = "UpdatePrivateData"
				offer.user_action = user_id

				u1.updatePrivateInfo(private_info)

				u1.addOfferHistory(offer)
				return
		else:
			try:
				raise ValueError("Error: {0} is not a valid user in this Haggler.".format(user_id))
			except ValueError as error:
				print(error)
			return

	def printHistory(self, user_id):
		"""
		Prints offer history for user_id in vaguely formatted table. 
		Full price is printed == price * quantity
		
		Args:
		    user_id (string): user id of user whose offer history is being tabulated
		
		Raises:
		    ValueError: if the user id supplied is not present in the Haggler.users dict
		"""
		if user_id in self.users.keys():
			# private data update one sided - no need for u2/other
			u1 = self.users[user_id]

			table_text = "{0:>10}{1:>20}{2:>15}{3:>24}{4:>10}{5:>15}{6:>15}{7:>15}" \
			              .format("Version","Action","User ID","State","Product","Buyer","Seller","Full Price")
			table_text += "\n"

			for o in u1.offer_history:
				line_text = []
				line_text.append("{0:>10}".format(str(o.version)))
				line_text.append("{0:>20}".format(o.action))
				line_text.append("{0:>15}".format(o.user_action))
				line_text.append("{0:>24}".format(o.state))
				line_text.append("{0:>10}".format(o.product))
				line_text.append("{0:>15}".format(o.buyer))
				line_text.append("{0:>15}".format(o.seller))
				full_price = o.quantity * o.price
				line_text.append("{0:>15}".format(str(full_price)))

				table_text += "".join(line_text) + "\n"

			print(table_text)
			return
		else:
			try:
				raise ValueError("Error: {0} is not a valid user in this Haggler.".format(user_id))
			except ValueError as error:
				print(error)
			return

	def printVersion(self, user_id, version):
		"""
		Prints offer version from offer history for user_id as a YAML formatted object. 
		
		Args:
		    user_id (string): user id of user whose offer history is being queried
		    version (int): the version number of the offer requested
		
		Raises:
			ValueError: if the version supplied is not in the offer history
		    ValueError: if the user id supplied is not present in the Haggler.users dict
		"""
		if user_id in self.users.keys():
			# private data update one sided - no need for u2/other
			u1 = self.users[user_id]

			# check if version <= length of offer_history
			if(version <= len(u1.offer_history) and version > 0):
				u1.offer_history[version-1].pretty()
				return
			else:
				try:
					raise ValueError("Error: Version {0} not in {1} order history.".format(version, user_id))
				except ValueError as error:
					print(error)
				return
		else:
			try:
				raise ValueError("Error: {0} is not a valid user in this Haggler.".format(user_id))
			except ValueError as error:
				print(error)
			return

	def returnVersion(self, user_id, version):
		"""
		Prints offer version from offer history for user_id as a YAML formatted object. 
		
		Args:
		    user_id (string): user id of user whose offer history is being queried
		    version (int): the version number of the offer requested

		Returns:
			Offer: the Offer instance corresponding to the version number in  offer history
		
		Raises:
			ValueError: if the version supplied is not in the offer history
		    ValueError: if the user id supplied is not present in the Haggler.users dict
		"""
		if user_id in self.users.keys():
			# private data update one sided - no need for u2/other
			u1 = self.users[user_id]

			# check if version <= length of offer_history
			if(version <= len(u1.offer_history) and version > 0):
				return(u1.offer_history[version-1])
			else:
				print("Error: Version {0} not in {1} order history.".format(version, user_id))
				try:
					raise ValueError("Error: Version {0} not in {1} order history.".format(version, user_id))
				except ValueError as error:
					print(error)
				return
		else:
			try:
				raise ValueError("Error: {0} is not a valid user in this Haggler.".format(user_id))
			except ValueError as error:
				print(error)
			return

	def versionDifferences(self, user_id, v1, v2):
		"""
		Identifies and returns dictionary with all differences between v1 and v2 where
		v1 and v2 are version numbers. For each attribute where a difference is found a list
		with two values is returned. First value is v1 value, second value is v2 value.
		
		Args:
		    user_id (string): user_id of user whose offer history is being queried
		    v1 (int): comparing differences from version v1... 
		    v2 (int): ... to version v2
		
		Returns:
		    dict: Description
		
		Raises:
		    ValueError: if the version supplied is not in the offer history
		    ValueError: if the user id supplied is not present in the Haggler.users dict
		"""
		if user_id in self.users.keys():
			# private data update one sided - no need for u2/other
			u1 = self.users[user_id]

			# check if v1 and v2 <= length of offer_history
			l_history = len(u1.offer_history)
			if(v1 <= l_history and v2 <= l_history and v1 > 0 and v2 > 0):
				if(v1 == v2):
					return({})

				v1_offer = vars(u1.offer_history[v1-1])
				v2_offer = vars(u1.offer_history[v2-1])

				#
				diffs = {}
				for k in v1_offer.keys():
					if(v1_offer[k] != v2_offer[k]):
						diffs[k]=[v1_offer[k], v2_offer[k]]

				return(diffs)
			else:
				try:
					raise ValueError("Error: Version {0} or {1} not in {2} order history.".format(v1, v2, user_id))
				except ValueError as error:
					print(error)
				return({})
		else:
			try:
				raise ValueError("Error: {0} is not a valid user in this Haggler.".format(user_id))
			except ValueError as error:
				print(error)
			return({})



