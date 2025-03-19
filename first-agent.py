from smolagents import CodeAgent, HfApiModel

model = HfApiModel() 
# you can also specify a particular provider e.g. provider="together" or provider="sambanova"
agent = CodeAgent(tools=[], model=model, add_base_tools=True)

agent.run(
    "Could you give me the 118th number in the Fibonacci sequence?",
)