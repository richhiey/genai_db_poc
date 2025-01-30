"""Chainlit UI for assistant with rag."""

import chainlit as cl
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

# from askdata.chatbot import react_graph
# from askdata.backend.langchain.agents.db_agent import db_agent as react_graph
from db_agent import db_agent as react_graph

# @cl.on_message
# async def main(message: cl.Message):
#     # Your custom logic goes here...

#     # Send a response back to the user
#     await cl.Message(
#         content=f"Received: {message.content}",
#     ).send()


@cl.on_message
async def on_message(msg: cl.Message) -> cl.Message:
    """Message handeler.

    Args:
        msg (cl.Message): Input human message

    Returns:
        cl.Message: Final answer message
    """
    config = {"configurable": {"thread_id": cl.context.session.id}}
    cb = cl.LangchainCallbackHandler()
    final_answer = cl.Message(content="")

    for m, metadata in react_graph.stream({"messages": msg.content}, stream_mode="messages", config=RunnableConfig(callbacks=[cb], **config)):
        if (
            m.content
            and not isinstance(m, HumanMessage)
            and metadata["langgraph_node"] ==  "agent"#"assistant_with_rag"
        ):
            await final_answer.stream_token(m.content)

    await final_answer.send()
