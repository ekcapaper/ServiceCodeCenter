from prefect import flow, task

@task
def say_hello():
    """Task: Print Hello, World!"""
    print("Hello, World!")

@flow(log_prints=True)
def hello_world_flow():
    """Flow: Run the hello task"""
    say_hello()

if __name__ == "__main__":
    hello_world_flow()
