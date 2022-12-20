import docker
import time


client = docker.from_env()
client.swarm.leave(force=True)
start = time.time()

try:
    # -------------------------------------------
    # SECTION 1 

    #Part A: Starting Swarm
    print("Starting swarm...")
    client.swarm.init()

    time.sleep(5)
    #Part B: Printing Swarm Attributes
    print("Swarm ID: ", client.swarm.attrs['ID'])
    print("Swarm Name: ", client.swarm.attrs['Spec']['Name'])
    print("Swarm Creation Date: ", client.swarm.attrs['CreatedAt'])

    #Part C: Creating The Network
    print("\nCreating network...")
    client.networks.create("se443_test_net", driver = "overlay", scope ="global", 
    ipam = docker.types.IPAMConfig(pool_configs = [docker.types.IPAMPool(subnet = "10.10.10.0/24")]))

    time.sleep(5)
    #Part D: Printing Network Attributes
    for net in client.networks.list():
        if net.name == "se443_test_net":
            print("Network ID: ", net.id)
            print("Network Name: ", net.name)
            print("Network Creation Date: ", net.attrs['Created'])

    #Part E & I: Creating Broker Service (Always Restart)...
    print("\nCreating Broker Service...")
    client.services.create("eclipse-mosquitto", name = "Broker", 
    restart_policy = docker.types.RestartPolicy(condition = "any")).scale(3)

    time.sleep(5)
    #Printing Out Attributes Of Service
    print("Service ID: ", client.services.list()[0].id)
    print("Service Name: ", client.services.list()[0].name)
    print("Service Creation Date: ", client.services.list()[0].attrs['CreatedAt'])
    print("Service Num Of Replicas: ", 
    client.services.list()[0].attrs['Spec']['Mode']['Replicated']['Replicas'])

    # -------------------------------------------

    # -------------------------------------------
    # SECTION 2

    #Part B, C, D, E: Creating Publisher Service...
    print("\nCreating Publisher Service...")
    client.services.create("efrecon/mqtt-client", name="Publisher",  restart_policy=docker.types.RestartPolicy(
            condition="any"), networks=["se443_test_net"], command='pub -h host.docker.internal -t Alfaisal_Uni -m "<201255 - Dalal - Aldossary>"').scale(3)
    time.sleep(5)
    print("Publisher ID: ", client.services.list()[0].id)
    print("Publisher Name: ", client.services.list()[0].name)
    print("Publisher Creation Date: ", client.services.list()[0].attrs['CreatedAt'])
    print("Publisher Num Of Replicas: ", 
    client.services.list()[0].attrs['Spec']['Mode']['Replicated']['Replicas'])

    #Part A, C, D, E: Creating Subscriber Service...
    print("\nCreating Subscriber Service...")
    client.services.create("efrecon/mqtt-client", name="Subscriber",  
            restart_policy=docker.types.RestartPolicy(
            condition="any"), 
            networks=["se443_test_net"], 
            command='sub -h host.docker.internal -t Alfaisal_Uni -v').scale(3)
    time.sleep(5)
    print("Subscriber ID: ", client.services.list()[0].id)
    print("Subscriber Name: ", client.services.list()[0].name)
    print("Subscriber Creation Date: ", client.services.list()[0].attrs['CreatedAt'])
    print("Subscriber Num Of Replicas: ", 
    client.services.list()[0].attrs['Spec']['Mode']['Replicated']['Replicas'])

    # -------------------------------------------

    # -------------------------------------------
    # SECTION 3

    print("\nRunning Services for 5 minutes...")
    time.sleep(300)

    print("\nRemoving Services...")

    #Removing Broker 
    print("Removing Broker...", end="")
    time.sleep(2)
    client.services.get("Broker").remove()
    print("Done!")

    #Removing Subscriber
    print("Removing Subscriber...", end="")
    time.sleep(2)
    client.services.get("Subscriber").remove()
    print("Done!")

    #Removing Publisher 
    print("Removing Publisher...", end="")
    client.services.get("Publisher").remove()
    print("Done!")

    #Removing Network
    print("Removing Network...", end="")
    time.sleep(2)
    client.networks.get("se443_test_net").remove()
    print("Done!")

    #Removing Swarm
    print("Removing Swarm...", end="")
    time.sleep(2)
    client.swarm.leave(force=True)
    print("Done!")

except Exception as e:
    print("Error occured...")
    print(e)