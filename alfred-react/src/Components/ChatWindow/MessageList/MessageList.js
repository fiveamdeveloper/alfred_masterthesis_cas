import MessageItem from "../MessageItem/MessageItem";

function MessageList({ messages }) {

    return (
        <div>
            {messages.map((message, index) => (
                <MessageItem key={index} message={message} />
            ))}


        </div>
    )
}

export default MessageList;
