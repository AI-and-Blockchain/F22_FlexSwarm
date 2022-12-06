import syft as sy

from syft.core.adp.data_subject import DataSubject
# %%

# %%
def login(email_, password_,port_=8081):
    try:
        domain_node = sy.login(email=email_, password=password_, port=port_)
    except:
        print("incorrect password or email")
    return domain_node

def displayuser (domain_node):
    print(domain_node.users)
def createuser(domain_node,name,email,password,budget=100):
    domain_node.users.create(
        **{
            "name": name,
            "email": email,
            "password": password,
            "budget": budget
        }
    )

# %%
def upload(domain_node, keys, data,structure):
    dataset = {}
    for i in keys:
        name_ = i
        data_subject = DataSubject(name=name_)
        dataset[name_] = sy.Tensor(data[i]).private(min_val=-1, max_val=1,data_subjects=[data_subject] * len(data[i]))

    domain_node.load_dataset(
        assets=dataset,
        name="model parameter",
        description=structure,
        metadata="Any metadata you'd like to include goes here"
    )

def  acceptrequest(domain):
    for i in domain.requests:
        i.accept()

