import numpy 
class option(object):
    """An option object

    Attributes:
        location: where you are building the factory.
        cost: construction costs.
        yearstocomplere: years to build factory
        discount: the interest rate for NPV calculation
        union: true or false
        costpercar: labor cost for this option
        revenuepercar: not including labor costs
        monthlyoutput: how many cars you build each month
        npv: the calculated net present value
    """

    def __init__(self, location, cost, yearstocomplete, 
                lifetime, discount, union, costpercar, 
                revenuepercar, monthlyoutput):
        """Return an option object 
        with the given parameters initialized
        """
        self.location = location
        self.cost = cost
        self.yearstocomplete = yearstocomplete
        self.lifetime = lifetime
        self.discount = discount
        self.union = union
        self.costpercar = costpercar
        self.revenuepercar = revenuepercar
        self.monthlyoutput = monthlyoutput
        
    def __str__(self):
        return ("#<option location: " + self.location + 
            " cost: " + str(self.cost) + ">")
        
    def get_location(self): return self.location 
    def get_cost(self): return self.cost
    def get_yearstocomplete(self): return self.yearstocomplete
    def get_lifetime(self): return self.lifetime
    def get_discount(self): return self.discount
    def get_union(self): return self.union
    def get_costpercar(self): return self.costpercar
    def get_revenuepercar(self): return self.revenuepercar
    def get_monthlyoutput(self): return self.monthlyoutput            
    
    
class decision(object):
    """A decision object

    Attributes:
        options: a list of option object
        stakeholders: a list of stakeholder
        choice: the selected option
        explanation: the justification for the decision
    """
    def __init__(self, options, stakeholders):
        """Return a decision object 
        with the given option list and stakeholder list
        """
        self.options = options
        self.stakeholders = stakeholders
        self.decision = None
        
    def __str__(self):
        return ("#<decision options: " + str(self.options) + 
            " stakeholders: " + str(self.stakeholders) + ">")
        
    def get_options(self):
        return self.options
    
    def get_stakeholders(self):
        return self.stakeholders

    def get_explanation(self):
    	return self.explanation
    
    
optOH = option("OH", 40000000, 2, 12, .05, True, 6500,
                    10000, 1000)
optSC = option("SC", 20000000, 2, 10, .05, True, 4000,
                    10000, 500)
s = ["stockholders", "unions", "OH", "SC"] # List of stakeholders
opt = [optOH, optSC] # list of options. 
d = decision(opt, s)
print(d)

def npv(option):
    # Yearly Cost to Complete
    yearly_cost_to_complete = -option.get_cost()/option.get_yearstocomplete()
    # Yearly Revenue after completion
    yearly_revenue = 12*option.get_monthlyoutput()*(option.get_revenuepercar()-option.get_costpercar())
    # Discounting rate
    rate = option.get_discount()
    # Initialize list for undiscounted CFs
    undiscounted_cfs = []
    # Append construction years as negative cash flows
    for i in range(option.get_yearstocomplete()):
        undiscounted_cfs.append(yearly_cost_to_complete)
    # Append production years as positive cash flows (no list comp because discrete types)
    for i in range(option.get_yearstocomplete(),option.get_lifetime()):
        undiscounted_cfs.append(yearly_revenue)
    # Discount cash flows
    discounted_cfs = [undiscounted_cfs[i]/(pow((1+rate),(i+1))) for i in range(len(undiscounted_cfs))]
    # Return NPV as sum of discounted cash flows
    npv = float(numpy.sum(discounted_cfs))
    #print npv
    return npv

def decide(option_list):
    npvs = [npv(option_list[i]) for i in range(len(option_list))]
    max_index = (numpy.array(npvs)).argmax()
    return option_list[max_index]

# This function approximates the E[npv] for a given option by varying 
# cost,discount,costpercar,revenuepercar and monthlyoutput by +/- 20%
# each, calculating its npv and taking the mean of those npvs. 
def expected_npv(option):
        npvs = []
        
        original = option.get_cost()
        option.cost = option.get_cost()*1.2
        npvs.append(npv(option))
        option.cost = (option.get_cost()/1.2)*.8
        npvs.append(npv(option))
        option.cost = original
        
        original = option.get_discount()
        option.discount = option.get_discount()*1.2
        npvs.append(npv(option))
        option.discount = (option.get_discount()/1.2)*.8
        npvs.append(npv(option))
        option.discount = original
        
        original = option.get_costpercar()
        option.costpercar = option.get_costpercar()*1.2
        npvs.append(npv(option))
        option.costpercar = (option.get_costpercar()/1.2)*.8
        npvs.append(npv(option))
        option.costpercar = original
        
        original = option.get_revenuepercar()
        option.revenuepercar = option.get_revenuepercar()*1.2
        npvs.append(npv(option))
        option.revenuepercar = (option.get_revenuepercar()/1.2)*.8
        npvs.append(npv(option))
        option.revenuepercar = original
        
        original = option.get_monthlyoutput()
        option.monthlyoutput = option.get_monthlyoutput()*1.2
        npvs.append(npv(option))
        option.monthlyoutput = (option.get_monthlyoutput()/1.2)*.8
        npvs.append(npv(option))
        option.monthlyoutput = original
        
        return numpy.mean(npvs), numpy.max(npvs), numpy.min(npvs)

# Sensitivity takes in a list of options. It returns the option with
# the largest expected npv given the possible variations in expected_npv()
def sensitivity(option_list):
    npvs = [expected_npv(option_list[i])[0] for i in range(len(option_list))]
    max_index = (numpy.array(npvs)).argmax()
    return option_list[max_index]

# Explain function takes in list of options and a designated
# shareholder. It creates a decision object and returns it. 
def explain(option_list, stakeholder = "stockholders"):
	best_option = sensitivity(option_list)
	explanation = '''
	THIS IS MY DECISION
	'''
	my_decision = decision(option_list,stakeholder)
	my_decision.explanation = explanation
	return my_decision

# Explain function takes in list of options and a designated
# shareholder. It creates a decision object and returns it. 
def explain(option_list, stakeholder = "stockholders"):
    best_option = sensitivity(option_list)
    e_npv, max_npv, min_npv = expected_npv(best_option)
    
    # Get list of locations
    locations = ", ".join(str(e) for e in [option_list[i].get_location() for i in range(len(option_list))])
    
    general_explanation = '''

##########################################################

The options presented were to build a plant in one of the 
following states:

{0}

I decided that the best option would be to build the plant 
in {1}. This decision was not made lightly and it is the 
one which represents the best value for this company.

This option was decided after performing an extensive 
sensitivty analysis on different potential construction 
costs, interest rates, labor costs, revenue per unit 
produced as well as total monthly production. 

Some key factors for this decision are:

Expected Net Present Value: ${2:,.2f}
Worst case Net Present Value: ${3:,.2f}
Best case Net Present Value: ${4:,.2f}
    '''.format(locations,best_option.get_location(),e_npv,max_npv,min_npv)
    
    stockholder_explanation = '''
To our shareholders:

As shareholders in this company, we expect that you will 
find this decision the rational choice. We value your 
tenacity to this company and look forward to continue to
grow on your behalf. 
    '''.format(e_npv,max_npv,min_npv)
    if(best_option.get_union()):
    	union_explanation = '''
To the members of the union:

We are incredibly excited that the hardworking members of
your union will be helping us in the expansion of our 
company. We have long been an institution which supports
your cause and we could not be more happy that we will be
continuing to strengthen our bonds.  
    '''
    else:
    	union_explanation = '''
To the members of the union:

This news may come as a surprise to your union and we 
hope that you are willing to understand our reasons in
this choice. 
    '''

    if(best_option.get_location()!="OH"):
    	ohio_community_explanation = '''
To the Ohio Community

We are very excited to be building our plant in your 
community and we look forward to building a strong relatio-
nship with you all. 
    '''
    else:
    	ohio_community_explanation = '''
To the Ohio Community:

We understand that this news may not be particularly 
welcome, but we hope you understand that it was necessary
for the health of the company. We will continue to consider
your community in the future as our company expands and we
hope that we can find ourselves working with you all soon.
    '''
    
    if(best_option.get_location()!="SC"):
    	sc_community_explanation = '''
To the South Carolina Community:

We are very excited to be building our plant in your 
community and we look forward to building a strong relatio-
nship with you all. 
    '''
    else:
    	sc_community_explanation = '''
To the South Carolina Community:

We understand that this news may not be particularly 
welcome, but we hope you understand that it was necessary
for the health of the company. We will continue to consider
your community in the future as our company expands and we
hope that we can find ourselves working with you all soon.
    '''

    tail = '''

##########################################################

    '''

    explanation = general_explanation
    if "stockholders" in stakeholder:
    	explanation = explanation + stockholder_explanation
    if "unions" in stakeholder:
    	explanation = explanation + union_explanation
    if "SC" in stakeholder:
    	explanation = explanation + sc_community_explanation
    if "OH" in stakeholder:
    	explanation = explanation + ohio_community_explanation
    explanation = explanation + tail

    my_decision = decision(option_list,stakeholder)
    my_decision.explanation = explanation
    print my_decision.get_explanation()
    return my_decision

explain([optSC,optOH],stakeholder = ["shareholders","unions"])





