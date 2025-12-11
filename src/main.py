from graph import graph_create

workflow=graph_create()

output=workflow.invoke({"messages":[], "mail":{ "subject":"Meeting tomorrow?","body":"Hi, can we meet at 3pm tomorrow? Thanks!"}})

print(output)