from langgraph.graph import StateGraph,START,END
from state import AgentState
from node import triage_node,check_route,ignore,notify_human,respond_act

#initilized graph
def graph_create()->StateGraph:
    graph=StateGraph(AgentState)

    #adding node
    graph.add_node("triage_node",triage_node)
    graph.add_node("ignore",ignore)
    graph.add_node("notify-human",notify_human)
    graph.add_node("respond-act",respond_act)

    #adding edge
    graph.add_edge(START,"triage_node")
    #adding route edge/conditional edge
    graph.add_conditional_edges("triage_node",check_route)
    graph.add_edge("ignore",END)
    graph.add_edge("notify-human",END)
    graph.add_edge("notify-human",END)

    

    return graph.compile()