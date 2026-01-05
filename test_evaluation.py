from evaluation.judge import evaluate

agent_reply = "Thank you for your email. I will get back to you."
ideal_reply = "Thank you for your email. I will get back to you."

scores = evaluate(agent_reply, ideal_reply)
print(scores)
