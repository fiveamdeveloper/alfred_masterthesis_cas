import MessageItem from "../MessageItem/MessageItem";

function MessageList() {

    var messages = [
        {
            "role": "user",
            "response": "Ist der Fertigungsauftrag 4711 freigegeben?"
        },
        {
            "role": "assistant",
            "response": "Ja, Auftrag 4711 ist freigegeben. Die Komponenten befinden sich in der Bereitstellung."
        },
        {
            "role": "user",
            "response": "Welche Komponenten sind dem ersten Vorgang zugeordnet?"
        },
        {
            "role": "assistant",
            "response": "Vorgang 0010 sind die Materialien 8020 und 5566 zugeordnet."
        },
    ]

    return (
        <div>
            {messages.map((message, index) => (
                <MessageItem key={index} message={message} />
            ))}
        </div>
    )
}

export default MessageList;
