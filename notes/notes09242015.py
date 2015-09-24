# Differential evolution -> better than maxwalksat and SA, 90s idea, this is where it's at, Code7

# Compartmental models are visual ways to express first order linear equations, can tell if they will converge or diverge
# Copy over the items in payload that weren't updated
# Keep background knowledge of the constraints on all the payloads
# step updates the payload
# have is once before the model starts running and step is once for each step in the model
# state is the background knowledge

# Support Utilities:
# dots sumbolize a repeat of the same values
# zip runs every column as one row, pulls out each column for formatting
# ditto is the dot printer
# enumerate = zipWithIndex

# Debugging Compartmental Models:
# never underestimate the effort associated with commissioning a model
# stay away from globals and have hierarchical modeling
# team up with domain experts

# Writing Compartmental Models:
# feedback loop from verbal cues
# Business users typically repeat a small number of cliches, submodules are useful(ex. for accounts receivable)
# 2 papers about linguistic clues

# Causal Model Refinement:
# Different business experts fixate on different parts of the process
# Can translate diagrams into models, pathway from scrolling on the whiteboard and then getting somethign that runs
# Process of Classic Activism, forces that resist change and forces that favor change are affected by the same variables
# UML is not business user friendly

# Drop subgraphs in submodels to analyze them

# Hans Gosling - Social theorist with WHO


# When you write a model, you spend a good proportion of your time debugging your model because if something unexpected happends you need to ensure it's the result of a valid model
# Should break models into submodels and verify microexpectations

# Brooks effect/law, adding programmers to a project delays release but there are also circumstances where it doesn't make it quicker just more exppensive


# Hofstadter, french poem translatation

# One way to build a domain specific language is to look at what pepople use and talk to them. Define domain idioms.

# @staticmethod is unique to class(1000 instances, 1 class)

